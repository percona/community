"""Windows Python controller; two existing container psql clients, no pip packages."""
import json
import os
import queue
import subprocess
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IDENTITY = json.loads((ROOT / 'evidence/lab-identity.json').read_text(encoding='utf-8-sig'))
CID = IDENTITY['container_id']
QTY = 3
WAIT = 15
PORT = int(os.environ.get('LU_LAB_CONTAINER_PORT', '5432'))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def verify_target():
    label = subprocess.run(
        ['docker', '--context', 'desktop-linux', 'inspect', CID, '--format',
         '{{index .Config.Labels "codex.percona.task"}}'],
        capture_output=True, text=True, check=True, timeout=15).stdout.strip()
    require(label == IDENTITY['owner_label'] == 'percona-snowwolf-20261015-pg18',
            'Unexpected container ownership')


class Client:
    def __init__(self):
        require(1 <= PORT <= 65535, 'Invalid container port')
        self.lines = queue.Queue()
        self.process = subprocess.Popen(
            ['docker', '--context', 'desktop-linux', 'exec', '-i', '-e', 'PGPASSWORD=lab-only-disposable',
             '-e', 'PGOPTIONS=-c statement_timeout=30000 -c client_min_messages=warning',
             CID, 'psql', '-X', '-q', '-A', '-t', '-w',
             '-v', 'ON_ERROR_STOP=1', '-h', '127.0.0.1', '-p', str(PORT),
             '-U', 'postgres', '-d', 'lost_updates'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, encoding='utf-8', bufsize=1)
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()
        try:
            self.pid = int(self.scalar('SELECT pg_backend_pid()'))
            require(self.scalar('SELECT current_database()') == 'lost_updates',
                    'Unexpected database')
        except BaseException:
            self.close()
            raise

    def _read(self):
        try:
            for line in self.process.stdout:
                self.lines.put(line.rstrip('\r\n'))
        finally:
            self.lines.put(None)

    def execute(self, sql):
        marker = 'END_' + uuid.uuid4().hex
        self.process.stdin.write(sql.rstrip(';') + ';\n\\echo ' + marker + '\n')
        self.process.stdin.flush()
        rows = []
        deadline = time.monotonic() + 40
        while True:
            left = deadline - time.monotonic()
            require(left > 0, 'psql response deadline expired')
            try:
                line = self.lines.get(timeout=left)
            except queue.Empty as exc:
                raise TimeoutError('psql response deadline expired') from exc
            if line is None:
                raise RuntimeError('psql exited before completing SQL: ' + '\n'.join(rows))
            if line == marker:
                return rows
            if line:
                rows.append(line)

    def scalar(self, sql):
        rows = self.execute(sql)
        require(len(rows) == 1, f'Expected one scalar row, got {rows!r}')
        return rows[0]

    def close(self):
        if self.process.poll() is None:
            try:
                self.process.stdin.write('\\q\n')
                self.process.stdin.flush()
                self.process.wait(timeout=5)
            except (BrokenPipeError, OSError, subprocess.TimeoutExpired):
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.process.wait(timeout=5)
        self.reader.join(timeout=2)
        for stream in (self.process.stdin, self.process.stdout):
            try:
                stream.close()
            except (BrokenPipeError, OSError):
                # A failed psql can leave a Windows pipe unflushable.
                # Preserve the original database error during cleanup.
                pass

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()


def prepare(c, stock):
    require(type(stock) is int and stock >= 0, 'Invalid starting stock')
    c.execute('CREATE SCHEMA IF NOT EXISTS lu_lab')
    c.execute('''CREATE TABLE IF NOT EXISTS lu_lab.inventory (
        sku integer PRIMARY KEY, stock integer NOT NULL CHECK (stock >= 0))''')
    c.execute(f'''INSERT INTO lu_lab.inventory VALUES (1, {stock})
        ON CONFLICT (sku) DO UPDATE SET stock = EXCLUDED.stock''')


def reserve(c, mode, old, qty):
    # SQL values in this fixture are strictly validated integer literals.
    require(type(qty) is int and qty > 0, 'Quantity must be positive')
    require(type(old) is int and old >= 0, 'Invalid old stock')
    require(mode in ('unsafe', 'atomic'), 'Unknown mode')
    if mode == 'unsafe':
        sql = f'UPDATE lu_lab.inventory SET stock = {old - qty} WHERE sku = 1 RETURNING stock'
    else:
        sql = f'''UPDATE lu_lab.inventory SET stock = stock - {qty}
            WHERE sku = 1 AND stock >= {qty} RETURNING stock'''
    rows = c.execute(sql)
    require(len(rows) <= 1, 'Unexpected reservation result')
    if rows:
        int(rows[0])
    return bool(rows)


def pair(controller, mode, start, rollback_a=False):
    prepare(controller, start)
    reads_done = threading.Barrier(2, timeout=WAIT)
    a_updated = threading.Event()
    pids = [None, None]

    def worker(index):
        with Client() as c:
            pids[index] = c.pid
            c.execute('BEGIN ISOLATION LEVEL READ COMMITTED')
            old = int(c.scalar('SELECT stock FROM lu_lab.inventory WHERE sku = 1'))
            require(old == start, 'Unexpected initial read')
            reads_done.wait()
            if index == 1:
                require(a_updated.wait(WAIT), 'A did not update')
            changed = reserve(c, mode, old, QTY)
            rolled_back = index == 0 and rollback_a
            if index == 0:
                require(changed, 'A must reserve')
                a_updated.set()
                deadline = time.monotonic() + WAIT
                while True:
                    blocked = c.scalar(f'SELECT {pids[0]} = ANY(pg_blocking_pids({pids[1]}))')
                    if blocked == 't':
                        require(pids[0] != pids[1], 'Workers must own distinct sessions')
                        print(f'BLOCKING mode={mode} start={start} rollback_a={rolled_back} '
                              f'a_pid={pids[0]} b_pid={pids[1]} initial_reads={start},{start}',
                              flush=True)
                        break
                    require(time.monotonic() < deadline, 'B was not observed blocked by A')
                    time.sleep(0.02)
            c.execute('ROLLBACK' if rolled_back else 'COMMIT')
            return changed and not rolled_back

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(worker, i) for i in range(2)]
        committed = sum(f.result() for f in futures)
    return committed, int(controller.scalar('SELECT stock FROM lu_lab.inventory WHERE sku = 1'))


def main():
    verify_target()
    with Client() as c:
        version_num = int(c.scalar('SHOW server_version_num'))
        require(180000 <= version_num < 190000, 'Use the isolated PostgreSQL 18 server')
        print('SERVER_VERSION_NUM', version_num, flush=True)
        print('SERVER', c.scalar('SELECT version()'), flush=True)
        print('TRANSPORT existing container psql; Windows Python standard library', flush=True)
        count, stock = pair(c, 'unsafe', 10)
        require((count, stock) == (2, 7), 'Negative control did not reproduce')
        require(stock != 10 - QTY * count, 'Lost update was not observed')
        print('BUG_REPRODUCED unsafe start=10 committed=2 stock=7')
        for start, expected in [(10, (2, 4)), (4, (1, 1))]:
            count, stock = pair(c, 'atomic', start)
            require((count, stock) == expected, 'Atomic result mismatch')
            require(stock == start - QTY * count, 'Inventory invariant failed')
            print(f'PASS atomic start={start} committed={count} stock={stock}')
        count, stock = pair(c, 'atomic', 4, rollback_a=True)
        require((count, stock) == (1, 1), 'Rollback result mismatch')
        require(stock == 4 - QTY * count, 'Rollback invariant failed')
        print('PASS rollback start=4 committed=1 stock=1')
        prepare(c, 2)
        c.execute('BEGIN ISOLATION LEVEL READ COMMITTED')
        changed = reserve(c, 'atomic', 2, QTY)
        c.execute('COMMIT')
        require(not changed and int(c.scalar('SELECT stock FROM lu_lab.inventory WHERE sku = 1')) == 2,
                'Insufficient stock changed inventory')
        print('PASS insufficient start=2 committed=0 stock=2')
        print('ALL EXPECTED CONDITIONS MET')


if __name__ == '__main__':
    main()

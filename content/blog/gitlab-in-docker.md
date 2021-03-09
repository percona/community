---
title: 'Gitlab in Docker'
date: 
draft: true
tags: ['MySQL', 'Open Source Databases', 'Tools']
---

These installation notes are mostly a note to myself, documenting the installation process of a Gitlab Omnibus Container in Docker, plus Gitlab Runners.

OS Setup
--------

We are installing into `/export/gitlab`, a 10G xfs slice from the local flash pool:

```
#  lvcreate -n gitlab -L 10G data
#  mkfs -t xfs /dev/data/gitlab
#  mkdir /export/gitlab
#  mount /dev/data/gitlab /export/gitlab
#  echo "/dev/data/gitlabt/export/gitlabtxfstbsdgroups,usrquota,grpquota,attr2,nofail,noatime 1 2" >> /etc/fstab
  #  mkdir /export/gitlab/{gitlab,gitlab-runner}
#  mkdir /export/gitlab/gitlab/{config,data,logs} 
```

Docker
------

We are using `docker-compose` to run this, with a `.env` (dotenv) like so:

```
#  cat .env
GITLAB_HOME=/export/gitlab/gitlab
GITLAB_DOMAIN=gitlab.home.koehntopp.de
GITLAB_HTTP_PORT=81
GITLAB_HTTPS_PORT=444
GITLAB_SSH_PORT=2222 
```

And a `docker-compose.yaml` like so:

```
---
version: "3"

services:
  web:
    container_name: "gitlab"
    hostname: "gitlab"
    image: "gitlab/gitlab-ce:latest"
    restart: always
    hostname: "${GITLAB_DOMAIN}"
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url "https://gitlab.home.koehntopp.de"
    ports:
      - '${GITLAB_HTTP_PORT}:80'
      - '${GITLAB_HTTPS_PORT}:443'
      - '${GITLAB_SSH_PORT}:22'
    volumes:
      - '${GITLAB_HOME}/config:/etc/gitlab'
      - '${GITLAB_HOME}/logs:/var/log/gitlab'
      - '${GITLAB_HOME}/data:/var/opt/gitlab'

## vim: syntax=yaml ts=2 sw=2 sts=2 sr et ai 
```

When starting this with `docker-compose up`, we can follow the full horribleness of the installation process in the console: The Gitlab Omnibus container collects a large number of processes internally, including a postgres, puma, nginx and a number of additional components, and configures itself internally using Chef. It is the Anti-Container.

gitlab.rb
---------

The initial run will produce a `gitlab.rb` config file in `/export/gitlab/gitlab/config/gitlab.rb`. The file is over 100KB in size, and will contain deactivated config.

A very minimal, runnable base config for me looks like this:

```
# grep -v "^#" gitlab.rb | uniq

external_url 'http://gitlab.home.koehntopp.de'

gitlab_rails['smtp_enable'] = false

gitlab_rails['gitlab_email_enabled'] = false

gitlab_rails['gitlab_default_can_create_group'] = false
gitlab_rails['gitlab_username_changing_enabled'] = false

gitlab_rails['gitlab_shell_ssh_port'] = 2222

gitlab_kas['enable'] = false 
```

TLS Forwarding from host to container
-------------------------------------

The internal ports need to be exported to the home network, so we need an Apache TLS forwarding config.

We are using this:

```
<VirtualHost *:80>
    ServerName gitlab.home.koehntopp.de

    ErrorLog ${APACHE_LOG_DIR}/gitlab-error.log
    CustomLog ${APACHE_LOG_DIR}/gitlab-access.log combined

    Alias /.well-known/acme-challenge /var/lib/dehydrated/acme-challenges
    <Directory /var/lib/dehydrated>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
    <If "!-f '%{REQUEST_FILENAME}'">
        RedirectMatch permanent ^/(.*) "https://gitlab.home.koehntopp.de/$1"
    </If>
</VirtualHost> 
<VirtualHost *:443>
    ServerName gitlab.home.koehntopp.de

    ErrorLog ${APACHE_LOG_DIR}/gitlab-ssl-error.log
    CustomLog ${APACHE_LOG_DIR}/gitlab-ssl-access.log combined

    SSLEngine on
    SSLCertificateFile /var/lib/dehydrated/certs/home.koehntopp.de/cert.pem
    SSLCertificateKeyFile /var/lib/dehydrated/certs/home.koehntopp.de/privkey.pem
    SSLCertificateChainFile /var/lib/dehydrated/certs/home.koehntopp.de/chain.pem

#   SSLProxyEngine on
    ProxyPreserveHost On
    ProxyPass "/" "http://127.0.0.1:81/" nocanon
    ProxyPassReverse "/" "http://127.0.0.1:81/"
    AllowEncodedSlashes NoDecode

    DocumentRoot /var/www/gitlab.home.koehntopp.de
</VirtualHost> 
# vim: syntax=apache ts=4 sw=4 sts=4 sr noet 
```

We are terminating the TLS at the Apache and forward plaintext to the nginx, which then forwards to the internal Ruby. This is silly, but I was not feeling like pulling that ball of string apart.

The `ProxyPass ... nocanon` and `AllowEncodedSlashes NoDecode` are necessary to avoid internal Error on various URLs that require passing on of `//` and `/-/` URL fragments (several issues, for example [here](https://gitlab.com/gitlab-org/gitlab/-/issues/211500#note_381651793)).

Basic Setup
-----------

Admin Login is with “root”, and will guide you through a password change and some basic setup.

I created users for the family, and groups for my work and for the little one.

Once you have groups, pushing existing repositories into gitlab is quickly done with

```
#  git push --set-upstream ssh://git@gitlab.home.koehntopp.de:2222/kris/$(git rev-parse --show-toplevel | xargs basename).git $(git rev-parse --abbrev-ref HEAD) 
```

This will create a repo for the user or group (here: `kris`) that has a name identical to the current directory. The `xargs basename` expression can be replaced with the desired literal name instead.

Afterwards, it may be useful to `git remote remove origin`, `git remote add origin ...`. A quick `git pull --rebase` and `git branch --set-upstream-to=origin/master master` will exercise and config the local push and pull operations, too.

A “hello-ci” project
--------------------

We are creating a basic Python project for gitlab-runner, for testing, `kk/probe`.

```
# cat probe.py
#! /usr/bin/env python3 
import src

if __name__ == '__main__':
    print(f'Hi, {src.my_name()}!') 
```

and

```
# cat src/__init__.py from src.main import my_name  # noqa 
```

and

```
# cat src/main.py
def my_name():
    return "Kris" 
```

In a `src/tests/` directory, we are running `pytest`:

```
#! /usr/bin/env python3 
import src

def test_my_name():
    assert src.my_name() == "Kris" 
```

At the toplevel, we put our `requirements.txt`:

```
flake8
pytest 
```

and a `tox.ini`:

```
[flake8]
exclude=.git,__pycache__,docs,*venv

[pytest]
addopts = -ra -q 
```

We can now build a `.gitlab-ci.yml`, also at the toplevel:

```
default:
  image: python:3.8

before_script:
  - python --version
  - pip install -r requirements.txt

stages:
  - Test

flake8:
  stage: Test
  script:
    - flake8

pytest:
  stage: Test
  script:
  - pwd
  - ls -l
  - export PYTHONPATH="$PYTHONPATH:."
  - python -c "import sys;print(sys.path)"
  - pytest src 
```

Yes, the testing cruft in the pytest setup can later go away…

Now, to make this work, we need to install gitlab-runner in a docker variant, and config it.

Gitlab Runner
-------------

At this point, the runner still needs to be `docker-compose`‘ed. I hacked it for testing like this:

```
#  mkdir -p /export/gitlab/gitlab-runner
#  cd !$
#  mkdir config
#  cat doit
docker run -d --name gitlab-runner 
  --restart always 
  -v /export/gitlab/gitlab-runner/config:/etc/gitlab-runner 
  -v /var/run/docker.sock:/var/run/docker.sock 
  gitlab/gitlab-runner:latest 
```

This will create a `config.toml` in the config directory. We can

```
#  docker exec -it gitlab-runner bash
root@ffd124dab4aa:/#  gitlab-runner register
#  gitlab-runner  register
Runtime platform                                    arch=amd64 os=linux pid=47 revision=8fa89735 version=13.6.0
Running in system-mode.

Enter the GitLab instance URL (for example, https://gitlab.com/):
https://gitlab.home.koehntopp.de/
Enter the registration token:
TheToken
Enter a description for the runner:
[ffd124dab4aa]: A test runner
Enter tags for the runner (comma-separated):
test 
```

The token required for registration can be obtained as described [here](https://docs.gitlab.com/runner/register/).

I registered group runners for each of my two internal groups, and a shared runner for the (empty) rest.

All of this will rewrite the `config.toml`. I then upped the concurrency to 6 (8 threads available in the hardware).

Later on, it will turn out that the docker images in my Ubuntu are not writeable as needed, a helper image needs to be added.

The `helper_image` line has been added manually below, according to [this note](https://gitlab.com/gitlab-org/gitlab-runner/-/issues/26618):

```
# cat /export/gitlab/gitlab-runner/config/config.toml
concurrent = 6
check_interval = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "JX_Snack (Docker)"
  url = "https://gitlab.home.koehntopp.de"
  token = "TheToken   executor = "docker"
  [runners.custom_build_dir]
  [runners.cache]
    [runners.cache.s3]
    [runners.cache.gcs]
    [runners.cache.azure]
  [runners.docker]
    helper_image = "gitlab/gitlab-runner-helper:x86_64-6fbc7474"
    tls_verify = false
    image = "python:3"
    privileged = false
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache"]
    shm_size = 0
... 
```

For easier testing, it may be useful to allow CI runs on untagged commits. This can be set up as `root` in `https://.../admin/runners` for the desired test runner.

![](https://isotopp.github.io/uploads/2020/11/gitlab-untagged.png)

_Allowing the runner to pick up untagged jobs can be useful for testing. It needs to be disabled later._

With some random committing we can now trigger and debug the pipeline we defined earlier above. Eventually it will actually do something.

![](https://isotopp.github.io/uploads/2020/11/gitlab-runner.png)

_Eventually, a testing success._

Having a gitlab and a CI/CD pipeline allows us to package the Python Discord Bot development process for the little one in a way that allows him to focus on the various stages of the development process sequentially. For now, testing and deployment can happen magically, we will visit that only later.
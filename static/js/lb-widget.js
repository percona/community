import { h, render, Fragment } from 'https://esm.sh/preact@10';
import { useState, useEffect, useRef } from 'https://esm.sh/preact@10/hooks';
import htm from 'https://esm.sh/htm@3';
import {
  BASE,
  LoadingStatus,
  Avatar,
  UserDetailModal,
  fmtNum,
  fmtDate,
  handleOf,
  initials,
  nameColor,
} from './lb-shared.js';

const html = htm.bind(h);

const ICONS = {
  global: html`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18"/></svg>`,
  github: html`<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2C6.48 2 2 6.58 2 12.26c0 4.52 2.87 8.35 6.84 9.7.5.1.68-.22.68-.48 0-.24-.01-.87-.01-1.7-2.78.62-3.37-1.37-3.37-1.37-.45-1.18-1.11-1.5-1.11-1.5-.91-.64.07-.63.07-.63 1 .07 1.53 1.06 1.53 1.06.89 1.57 2.34 1.12 2.91.86.09-.66.35-1.12.63-1.37-2.22-.26-4.56-1.14-4.56-5.07 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.3.1-2.7 0 0 .84-.27 2.75 1.05A9.2 9.2 0 0 1 12 6.8c.85 0 1.7.12 2.5.34 1.9-1.32 2.74-1.05 2.74-1.05.55 1.4.2 2.44.1 2.7.64.72 1.03 1.63 1.03 2.75 0 3.94-2.34 4.8-4.57 5.06.36.32.68.94.68 1.9 0 1.37-.01 2.48-.01 2.81 0 .27.18.59.69.48A10.03 10.03 0 0 0 22 12.26C22 6.58 17.52 2 12 2z"/></svg>`,
  content: html`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4 11.5-11.5z"/></svg>`,
  forum: html`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M21 12a8 8 0 0 1-8 8H7l-4 3V12a8 8 0 0 1 8-8h2a8 8 0 0 1 8 8z"/></svg>`,
};

const CATS = [
  { key: 'global',  label: 'Global'  },
  { key: 'github',  label: 'GitHub'  },
  // { key: 'content', label: 'Content' }, // hidden for now — sparse data
  { key: 'forum',   label: 'Forum'   },
];

const CAT_COLS = {
  global: [
    { key: 'points_total',   label: 'Points', pts: true },
    { key: 'issues_created', label: 'Issues'    },
    { key: 'prs_created',    label: 'PRs'       },
    { key: 'prs_merged',     label: 'Merged'    },
    { key: 'blog_posts',     label: 'Posts'     },
    { key: 'topics_created', label: 'Topics'    },
    { key: 'replies',        label: 'Replies'   },
    { key: 'solutions',      label: 'Solutions' },
  ],
  github: [
    { key: 'points_github',  label: 'Points', pts: true },
    { key: 'issues_created', label: 'Issues'  },
    { key: 'prs_created',    label: 'PRs'     },
    { key: 'prs_merged',     label: 'Merged'  },
  ],
  content: [
    { key: 'points_content', label: 'Points', pts: true },
    { key: 'blog_posts',     label: 'Posts'  },
  ],
  forum: [
    { key: 'points_forum',   label: 'Points', pts: true },
    { key: 'topics_created', label: 'Topics'    },
    { key: 'replies',        label: 'Replies'   },
    { key: 'solutions',      label: 'Solutions' },
  ],
};

const TYPE_LABELS = { 'all-time': 'All Time', year: 'Year', quarter: 'Quarter', month: 'Month' };
const TYPE_ORDER = ['year', 'quarter', 'month', 'all-time'];

function PeriodSelect({ periods, value, onChange }) {
  const [open, setOpen] = useState(false);
  const rootRef = useRef(null);

  const grouped = {};
  for (const p of periods) {
    if (!grouped[p.type]) grouped[p.type] = [];
    grouped[p.type].push(p);
  }

  const current = periods.find(p => p.key === value);
  const label = current?.label || value;

  useEffect(() => {
    if (!open) return;
    const onDoc = (e) => {
      if (!rootRef.current?.contains(e.target)) setOpen(false);
    };
    const onKey = (e) => {
      if (e.key === 'Escape') setOpen(false);
    };
    document.addEventListener('mousedown', onDoc);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onDoc);
      document.removeEventListener('keydown', onKey);
    };
  }, [open]);

  const orderedTypes = [
    ...TYPE_ORDER.filter(t => grouped[t]?.length),
    ...Object.keys(grouped).filter(t => !TYPE_ORDER.includes(t)),
  ];

  return html`
    <div class=${'lb-period' + (open ? ' is-open' : '')} ref=${rootRef}>
      <button
        type="button"
        class="lb-period__btn"
        aria-haspopup="listbox"
        aria-expanded=${open}
        aria-label="Period"
        onClick=${() => setOpen(v => !v)}
      >
        <span class="lb-period__label">${label}</span>
        <svg class="lb-period__chevron" viewBox="0 0 12 8" width="12" height="8" aria-hidden="true" focusable="false">
          <path d="M1 1l5 5 5-5" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round"/>
        </svg>
      </button>
      ${open ? html`
        <div class="lb-period__menu" role="listbox" aria-label="Select period">
          ${orderedTypes.map(type => html`
            <div class="lb-period__group" key=${type}>
              <div class="lb-period__group-label">${TYPE_LABELS[type] || type}</div>
              ${grouped[type].map(p => html`
                <button
                  type="button"
                  role="option"
                  aria-selected=${p.key === value}
                  class=${'lb-period__option' + (p.key === value ? ' is-active' : '')}
                  key=${p.key}
                  onClick=${() => { onChange(p.key); setOpen(false); }}
                >${p.label}</button>
              `)}
            </div>
          `)}
        </div>
      ` : null}
    </div>
  `;
}

// ---- Top-3 Leader Card (mountaineer-card style) ----
function LeaderCard({ user, rank, cols, onClick }) {
  const handle = handleOf(user);
  const statCols = cols.filter(c => !c.pts).slice(0, 4);
  const bg = nameColor(user.display_name);

  return html`
    <article
      class=${'lb-leader-card rank-' + rank}
      onClick=${() => onClick(user)}
    >
      <div class="lb-leader-media">
        <div class="lb-leader-photo-wrap">
          ${user.avatar_url
            ? html`<${Fragment}>
                <img src=${user.avatar_url} alt=${user.display_name}
                     onError=${e => {
                       e.target.style.display = 'none';
                       e.target.nextSibling.style.display = 'flex';
                     }} />
                <div class="lb-photo-fallback" style=${{ background: bg, display: 'none' }}>${initials(user.display_name)}</div>
              </${Fragment}>`
            : html`<div class="lb-photo-fallback" style=${{ background: bg }}>${initials(user.display_name)}</div>`
          }
        </div>
        <svg class="lb-leader-triangle" xmlns="http://www.w3.org/2000/svg" width="92" height="158" viewBox="0 0 70 121" fill="none" aria-hidden="true" focusable="false">
          <path d="M70 121L0 0L70 0L70 121Z" fill="#282727"/>
        </svg>
        <span class=${'lb-rank-badge rank-' + rank}>#${rank}</span>
      </div>
      <div class="lb-leader-body">
        <div class="lb-leader-name">${user.display_name}</div>
        <div class="lb-leader-handle">${handle ? '@' + handle : '\u00a0'}</div>
        <div class="lb-stat-pills">
          ${statCols.map(c => html`
            <span class="lb-stat-pill">${fmtNum(user[c.key] || 0)} ${c.label.toLowerCase()}</span>
          `)}
        </div>
      </div>
    </article>
  `;
}

// ---- Main App ----
function LeaderboardApp({ meta }) {
  const [period, setPeriod] = useState(meta.default_period || String(new Date().getFullYear()));
  const [cat, setCat] = useState('global');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true); setData(null); setError(null); setSelected(null);
    fetch(`${BASE}/${cat}/${period}.json`)
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then(d => { if (!cancelled) { setData(d); setLoading(false); } })
      .catch(e => { if (!cancelled) { setError(e.message); setLoading(false); } });
    return () => { cancelled = true; };
  }, [period, cat]);

  const cols = CAT_COLS[cat] || CAT_COLS.global;
  const top3 = data?.top30?.slice(0, 3) || [];
  const rest = data?.top30?.slice(3, 30) || [];

  const openProfile = (user) => {
    setSelected(user);
  };

  return html`
    <div>
      <div class="lb-toolbar">
        ${CATS.map(c => html`
          <button type="button"
                  class=${'lb-cat-btn' + (c.key === cat ? ' active' : '')}
                  onClick=${() => setCat(c.key)}>
            ${ICONS[c.key]} ${c.label}
          </button>
        `)}
        <${PeriodSelect}
          periods=${meta.periods || []}
          value=${period}
          onChange=${setPeriod}
        />
      </div>

      <div style="min-height:280px">
        ${loading ? html`<${LoadingStatus} active=${true} />` : null}
        ${error ? html`<div class="lb-state lb-state-error">Error: ${error}</div>` : null}

        ${!loading && !error && data ? html`<${Fragment}>
          ${top3.length ? html`
            <div class="lb-leaders">
              ${top3.map((user, i) => html`
                <${LeaderCard}
                  user=${user}
                  rank=${i + 1}
                  cols=${cols}
                  onClick=${openProfile}
                />
              `)}
            </div>
          ` : html`<div class="lb-state">No contributors for this period.</div>`}

          ${rest.length ? html`
            <div class="lb-table-wrap">
              <table class="lb-table">
                <thead>
                  <tr>
                    <th class="col-rank">#</th>
                    <th class="col-user">Contributor</th>
                    ${cols.map(c => html`<th>${c.label}</th>`)}
                  </tr>
                </thead>
                <tbody>
                  ${rest.map(user => html`
                    <tr onClick=${() => openProfile(user)}>
                      <td class="col-rank">#${user.rank}</td>
                      <td class="col-user">
                        <div class="lb-user-cell">
                          <${Avatar} url=${user.avatar_url} name=${user.display_name} size="lb-avatar-md" />
                          <div>
                            <div class="lb-user-name">${user.display_name}</div>
                            ${handleOf(user)
                              ? html`<div class="lb-user-handle">@${handleOf(user)}</div>`
                              : null}
                          </div>
                        </div>
                      </td>
                      ${cols.map(c => {
                        const val = user[c.key] ?? 0;
                        return html`<td class=${c.pts ? 'lb-pts-col' : (val === 0 ? 'lb-zero' : '')}>${fmtNum(val)}</td>`;
                      })}
                    </tr>
                  `)}
                </tbody>
              </table>
            </div>
          ` : null}

          <div class="lb-updated">Updated: ${data.generated_at?.slice(0, 10) || '—'}</div>
        </${Fragment}>` : null}
      </div>

      ${selected ? html`
        <${UserDetailModal} user=${selected} period=${period} onClose=${() => setSelected(null)} />
      ` : null}
    </div>
  `;
}

async function init() {
  const el = document.getElementById('lb-widget');
  if (!el) return;
  try {
    const meta = await fetch(`${BASE}/meta.json`).then(r => r.json());
    render(html`<${LeaderboardApp} meta=${meta} />`, el);
  } catch (e) {
    el.innerHTML = '<p class="lb-state">Leaderboard data is not available yet.</p>';
  }
}
init();

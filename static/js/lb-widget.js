import { h, render, Fragment } from 'https://esm.sh/preact@10';
import { useState, useEffect } from 'https://esm.sh/preact@10/hooks';
import htm from 'https://esm.sh/htm@3';
const html = htm.bind(h);

const BASE = window.LB_BASE || 'https://raw.githubusercontent.com/dbazhenov/community-website-leaderboard-data/main';

const CATS = [
  { key:'global',  label:'Global',  icon:'🌐' },
  { key:'github',  label:'GitHub',  icon:'🐙' },
  { key:'content', label:'Content', icon:'✍️'  },
  { key:'forum',   label:'Forum',   icon:'💬' },
];

const RANK_MEDAL = ['', '🥇', '🥈', '🥉'];

const CAT_COLS = {
  global: [
    { key:'issues_created', label:'Issues'    },
    { key:'prs_created',    label:'PRs'       },
    { key:'prs_merged',     label:'Merged'    },
    { key:'blog_posts',     label:'Posts'     },
    { key:'topics_created', label:'Topics'    },
    { key:'replies',        label:'Replies'   },
    { key:'solutions',      label:'Solutions' },
    { key:'points_total',   label:'Points', pts:true },
  ],
  github: [
    { key:'issues_created', label:'Issues'  },
    { key:'prs_created',    label:'PRs'     },
    { key:'prs_merged',     label:'Merged'  },
    { key:'points_github',  label:'Points', pts:true },
  ],
  content: [
    { key:'blog_posts',     label:'Posts'  },
    { key:'points_content', label:'Points', pts:true },
  ],
  forum: [
    { key:'topics_created', label:'Topics'    },
    { key:'replies',        label:'Replies'   },
    { key:'solutions',      label:'Solutions' },
    { key:'points_forum',   label:'Points', pts:true },
  ],
};

const TYPE_LABELS = { 'all-time':'All Time', year:'Year', quarter:'Quarter', month:'Month' };
const PALETTE = ['#4e79a7','#f28e2b','#e15759','#76b7b2','#59a14f','#edc948','#b07aa1','#9c755f'];

function initials(name) {
  return (name||'?').split(/[\s._-]/).map(w=>w[0]||'').join('').slice(0,2).toUpperCase() || '?';
}
function nameColor(name) {
  let h = 0;
  for (let i = 0; i < (name||'').length; i++) h = name.charCodeAt(i) + ((h << 5) - h);
  return PALETTE[Math.abs(h) % PALETTE.length];
}
function fmtNum(n) { return (n||0).toLocaleString(); }
function fmtDate(s) {
  if (!s) return '';
  const d = new Date(s);
  return d.toLocaleDateString('en-US', { month:'short', day:'numeric', year:'numeric' });
}

// ---- Avatar ----
function Avatar({ url, name, size, style: extraStyle }) {
  const bg  = nameColor(name);
  const cls = `lb-avatar-circle ${size||'lb-avatar-md'}`;
  if (url) return html`<${Fragment}>
    <img src=${url} class=${cls} style=${{ ...extraStyle }}
         alt=${name}
         onError=${e => { e.target.style.display='none'; e.target.nextSibling.style.display='flex'; }} />
    <div class=${cls} style=${{ ...extraStyle, background:bg, display:'none' }}>${initials(name)}</div>
  </${Fragment}>`;
  return html`<div class=${cls} style=${{ ...extraStyle, background:bg }}>${initials(name)}</div>`;
}

// ---- Top-3 Leader Card ----
function LeaderCard({ user, rank, cols, ptsKey, onClick }) {
  const size     = rank === 1 ? 'lb-avatar-xl' : 'lb-avatar-lg';
  const handle   = user.github_login || user.forum_username;
  const statCols = cols.filter(c => !c.pts).slice(0, 4);

  return html`
    <div class=${'lb-leader-card rank-' + rank} onClick=${() => onClick(user)}>
      <div style=${{ fontSize: rank===1 ? '80px' : '60px', lineHeight:1, marginBottom:'6px' }}>${RANK_MEDAL[rank]}</div>
      <${Avatar} url=${user.avatar_url} name=${user.display_name} size=${size}
                 style=${{ display:'inline-flex', margin:'0 auto 4px' }} />
      <div class="lb-leader-name">${user.display_name}</div>
      ${handle ? html`<div class="lb-leader-handle">@${handle}</div>` : html`<div style="height:18px"></div>`}
      <div class="lb-leader-pts">${fmtNum(user[ptsKey] ?? user.points_total ?? 0)}</div>
      <div class="lb-stat-grid">
        ${statCols.map(c => html`
          <div class="lb-stat-box">
            <div class="lb-stat-val">${fmtNum(user[c.key]||0)}</div>
            <div class="lb-stat-lbl">${c.label}</div>
          </div>
        `)}
      </div>
    </div>
  `;
}

// ---- Detail Modal ----
function UserDetailModal({ user, period, onClose }) {
  const [detail,  setDetail]  = useState(null);
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState(null);

  useEffect(() => {
    if (!user.user_key) { setLoading(false); return; }
    fetch(`${BASE}/users/${period}/${user.user_key}.json`)
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then(d  => { setDetail(d); setLoading(false); })
      .catch(e => { setError(e.message); setLoading(false); });
  }, [user.user_key, period]);

  const d      = detail || user;
  const handle = d.github_login || d.forum_username;

  return html`
    <div class="lb-overlay" onClick=${e => { if (e.target === e.currentTarget) onClose(); }}>
      <div class="lb-modal-lg" onClick=${e => e.stopPropagation()}>
        <button class="lb-modal-close" onClick=${e => { e.stopPropagation(); onClose(); }} aria-label="Close">✕</button>

        <div class="lb-modal-header">
          <${Avatar} url=${d.avatar_url} name=${d.display_name} size="lb-avatar-lg"
                     style=${{ display:'inline-flex', flexShrink:0 }} />
          <div style="flex:1; min-width:0">
            <h5 style="margin:0">${d.display_name}</h5>
            ${handle ? html`<div style="font-size:13px;color:#6c757d">@${handle}</div>` : null}
            <div style="margin-top:6px">
              <span class="lb-modal-pts">${fmtNum(d.points_total||0)}</span>
              <span class="lb-modal-pts-lbl" style="margin-left:4px">total points</span>
            </div>
          </div>
        </div>

        <div class="lb-modal-body">
          ${loading ? html`<div class="lb-spinner"></div>` : null}
          ${!loading && error && !detail ? html`<div style="text-align:center;padding:1rem;font-size:13px;color:#6c757d">Could not load contribution details.</div>` : null}

          ${!loading ? html`<${Fragment}>

            ${(d.points_github||d.points_content||d.points_forum) ? html`
              <div class="lb-modal-stats">
                <div class="lb-modal-stat"><div class="v">${fmtNum(d.points_github||0)}</div><div class="l">GitHub</div></div>
                <div class="lb-modal-stat"><div class="v">${fmtNum(d.points_content||0)}</div><div class="l">Content</div></div>
                <div class="lb-modal-stat"><div class="v">${fmtNum(d.points_forum||0)}</div><div class="l">Forum</div></div>
                ${(d.issues_created||d.prs_created) ? html`
                  <div class="lb-modal-stat"><div class="v">${fmtNum((d.issues_created||0)+(d.prs_created||0))}</div><div class="l">Issues+PRs</div></div>
                ` : null}
                ${d.solutions ? html`
                  <div class="lb-modal-stat"><div class="v">${fmtNum(d.solutions||0)}</div><div class="l">Solutions</div></div>
                ` : null}
              </div>
            ` : null}

            ${detail?.github_issues?.length ? html`
              <div class="lb-section">
                <div class="lb-section-title">GitHub Issues (${detail.github_issues.length})</div>
                ${detail.github_issues.map(it => html`
                  <div class="lb-contrib-item">
                    <div class="lb-contrib-left">
                      <span class=${'lb-badge ' + (it.state==='open' ? 'lb-badge-open' : 'lb-badge-closed')}>${it.state}</span>
                      <a class="lb-contrib-link" href=${it.url} target="_blank" rel="noopener">${it.title}</a>
                    </div>
                    <span class="lb-contrib-meta">${it.repo ? it.repo+' · ' : ''}${fmtDate(it.date)}</span>
                  </div>
                `)}
              </div>
            ` : null}

            ${detail?.github_prs?.length ? html`
              <div class="lb-section">
                <div class="lb-section-title">Pull Requests (${detail.github_prs.length})</div>
                ${detail.github_prs.map(it => html`
                  <div class="lb-contrib-item">
                    <div class="lb-contrib-left">
                      ${it.merged ? html`<span class="lb-badge lb-badge-merged">merged</span>` : null}
                      <a class="lb-contrib-link" href=${it.url} target="_blank" rel="noopener">${it.title}</a>
                    </div>
                    <span class="lb-contrib-meta">${it.repo ? it.repo+' · ' : ''}${fmtDate(it.date)}</span>
                  </div>
                `)}
              </div>
            ` : null}

            ${detail?.blog_list?.length ? html`
              <div class="lb-section">
                <div class="lb-section-title">Blog Posts (${detail.blog_list.length})</div>
                ${detail.blog_list.map(it => html`
                  <div class="lb-contrib-item">
                    <div class="lb-contrib-left">
                      <a class="lb-contrib-link" href=${it.url} target="_blank" rel="noopener">${it.title}</a>
                    </div>
                    <span class="lb-contrib-meta">${fmtDate(it.date)}</span>
                  </div>
                `)}
              </div>
            ` : null}

            ${detail?.forum_topics?.length ? html`
              <div class="lb-section">
                <div class="lb-section-title">Forum Topics (${detail.forum_topics.length})</div>
                ${detail.forum_topics.map(it => html`
                  <div class="lb-contrib-item">
                    <div class="lb-contrib-left">
                      <a class="lb-contrib-link" href=${it.url} target="_blank" rel="noopener">${it.title}</a>
                    </div>
                    <span class="lb-contrib-meta">${fmtDate(it.date)}</span>
                  </div>
                `)}
              </div>
            ` : null}

            ${detail?.forum_replies?.length ? html`
              <div class="lb-section">
                <div class="lb-section-title">Forum Replies (${detail.forum_replies.length})</div>
                ${detail.forum_replies.map(it => html`
                  <div class="lb-contrib-item">
                    <div class="lb-contrib-left">
                      <a class="lb-contrib-link" href=${it.url} target="_blank" rel="noopener">${it.topic_title||it.title||'Reply'}</a>
                    </div>
                    <span class="lb-contrib-meta">${fmtDate(it.date)}</span>
                  </div>
                `)}
              </div>
            ` : null}

            ${detail?.forum_solutions?.length ? html`
              <div class="lb-section">
                <div class="lb-section-title">Accepted Solutions (${detail.forum_solutions.length})</div>
                ${detail.forum_solutions.map(it => html`
                  <div class="lb-contrib-item">
                    <div class="lb-contrib-left">
                      <span class="lb-badge" style="background:#6f42c1;color:#fff">solution</span>
                      <a class="lb-contrib-link" href=${it.url} target="_blank" rel="noopener">${it.topic_title||it.title||'Solution'}</a>
                    </div>
                    <span class="lb-contrib-meta">${fmtDate(it.date)}</span>
                  </div>
                `)}
              </div>
            ` : null}

            ${!detail?.github_issues?.length && !detail?.github_prs?.length &&
              !detail?.blog_list?.length && !detail?.forum_topics?.length &&
              !detail?.forum_replies?.length && !detail?.forum_solutions?.length ? html`
              <p style="font-size:13px;color:#6c757d">No detailed contribution data available for this period.</p>
            ` : null}

            <div class="lb-cta">
              <strong>Is this you?</strong> Add your GitHub and blog accounts in your
              <a href="https://forums.percona.com/my/preferences/profile" target="_blank" rel="noopener">Percona Forum profile settings</a>
              to combine all your contributions in one place.
            </div>

          </${Fragment}>` : null}
        </div>
      </div>
    </div>
  `;
}

// ---- Main App ----
function LeaderboardApp({ meta }) {
  const [period,   setPeriod]   = useState(String(new Date().getFullYear()));
  const [cat,      setCat]      = useState('global');
  const [data,     setData]     = useState(null);
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState(null);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true); setData(null); setError(null); setSelected(null);
    fetch(`${BASE}/${cat}/${period}.json`)
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then(d  => { if (!cancelled) { setData(d); setLoading(false); } })
      .catch(e => { if (!cancelled) { setError(e.message); setLoading(false); } });
    return () => { cancelled = true; };
  }, [period, cat]);

  const grouped = {};
  for (const p of meta.periods) {
    if (!grouped[p.type]) grouped[p.type] = [];
    grouped[p.type].push(p);
  }

  const cols   = CAT_COLS[cat] || CAT_COLS.global;
  const ptsCol = cols.find(c => c.pts);
  const ptsKey = ptsCol ? ptsCol.key : 'points_total';
  const top3   = data?.top30?.slice(0, 3)  || [];
  const rest   = data?.top30?.slice(3, 30) || [];

  return html`
    <div>
      <div class="lb-toolbar">
        ${CATS.map(c => html`
          <button class=${'lb-cat-btn' + (c.key === cat ? ' active' : '')}
                  onClick=${() => setCat(c.key)}>
            ${c.icon} ${c.label}
          </button>
        `)}
        <div class="lb-period-sep"></div>
        <select class="lb-period-select"
                value=${period} onChange=${e => setPeriod(e.target.value)}>
          ${Object.entries(grouped).map(([type, items]) => html`
            <optgroup label=${TYPE_LABELS[type] || type}>
              ${items.map(p => html`<option value=${p.key}>${p.label}</option>`)}
            </optgroup>
          `)}
        </select>
      </div>

      <div style="min-height:300px;margin-top:12px">
        ${loading ? html`<div style="text-align:center;padding:3rem;color:#6c757d">Loading…</div>` : null}
        ${error   ? html`<div style="text-align:center;padding:3rem;color:#dc3545">Error: ${error}</div>` : null}

        ${!loading && !error && data ? html`<${Fragment}>
          ${top3.length ? html`
            <div class="lb-leaders">
              ${top3[1] ? html`<${LeaderCard} user=${top3[1]} rank=2 cols=${cols} ptsKey=${ptsKey} onClick=${setSelected} />` : null}
              ${top3[0] ? html`<${LeaderCard} user=${top3[0]} rank=1 cols=${cols} ptsKey=${ptsKey} onClick=${setSelected} />` : null}
              ${top3[2] ? html`<${LeaderCard} user=${top3[2]} rank=3 cols=${cols} ptsKey=${ptsKey} onClick=${setSelected} />` : null}
            </div>
          ` : null}

          ${rest.length ? html`
            <div class="lb-table-wrap" style="margin-top:8px">
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
                    <tr onClick=${() => setSelected(user)}>
                      <td class="col-rank">${user.rank}</td>
                      <td class="col-user">
                        <div class="lb-user-cell">
                          <${Avatar} url=${user.avatar_url} name=${user.display_name} size="lb-avatar-md" />
                          <div>
                            <div class="lb-user-name">${user.display_name}</div>
                            ${(user.github_login||user.forum_username)
                              ? html`<div class="lb-user-handle">@${user.github_login||user.forum_username}</div>`
                              : null}
                          </div>
                        </div>
                      </td>
                      ${cols.map(c => {
                        const val = user[c.key] ?? 0;
                        return html`<td class=${c.pts ? 'lb-pts-col' : (val===0 ? 'lb-zero' : '')}>${fmtNum(val)}</td>`;
                      })}
                    </tr>
                  `)}
                </tbody>
              </table>
            </div>
          ` : null}

          <div style="text-align:right;margin-top:8px">
            <small style="color:#6c757d">Updated: ${data.generated_at?.slice(0,10)}</small>
          </div>
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
  } catch(e) {
    el.innerHTML = '<p style="color:#6c757d;text-align:center;padding:2rem">Leaderboard data is not available yet.</p>';
  }
}
init();

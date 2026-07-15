import { h, Fragment } from 'https://esm.sh/preact@10';
import { useState, useEffect, useRef } from 'https://esm.sh/preact@10/hooks';
import { createPortal } from 'https://esm.sh/preact@10/compat';
import htm from 'https://esm.sh/htm@3';

const html = htm.bind(h);

export const BASE = window.LB_BASE || 'https://raw.githubusercontent.com/percona/community-leaderboard/widget';

const PALETTE = ['#653DF4', '#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f', '#b07aa1', '#9c755f'];

const LOADING_PHRASES = [
  'Checking the expedition logs…',
  'Plotting the routes…',
  'Rallying the climbers…',
  'Tightening the ropes…',
  'Scanning the slopes…',
  'Marking the summits…',
  'Syncing with base camp…',
  'Ascending to the data…',
];

export function initials(name) {
  return (name || '?').split(/[\s._-]/).map(w => w[0] || '').join('').slice(0, 2).toUpperCase() || '?';
}

export function nameColor(name) {
  let n = 0;
  for (let i = 0; i < (name || '').length; i++) n = name.charCodeAt(i) + ((n << 5) - n);
  return PALETTE[Math.abs(n) % PALETTE.length];
}

export function fmtNum(n) { return (n || 0).toLocaleString(); }

export function fmtDate(s) {
  if (!s) return '';
  return new Date(s).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

export function handleOf(user) {
  return user.github_login || user.forum_username || null;
}

export function LoadingStatus({ active }) {
  const [idx, setIdx] = useState(() => Math.floor(Math.random() * LOADING_PHRASES.length));

  useEffect(() => {
    if (!active) return;
    const tick = setInterval(() => {
      setIdx(i => (i + 1) % LOADING_PHRASES.length);
    }, 2400);
    return () => clearInterval(tick);
  }, [active]);

  if (!active) return null;

  return html`
    <div class="lb-loading" role="status" aria-live="polite">
      <div class="lb-loading__spinner" aria-hidden="true"></div>
      <p class="lb-loading__text">${LOADING_PHRASES[idx]}</p>
    </div>
  `;
}

export function Avatar({ url, name, size, square, style: extraStyle }) {
  const bg = nameColor(name);
  const shape = square ? 'lb-avatar-square' : 'lb-avatar-circle';
  const cls = `${shape} ${size || 'lb-avatar-md'}`;
  if (url) return html`<${Fragment}>
    <img src=${url} class=${cls} style=${{ ...extraStyle }}
         alt=${name}
         onError=${e => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'flex'; }} />
    <div class=${cls} style=${{ ...extraStyle, background: bg, display: 'none' }}>${initials(name)}</div>
  </${Fragment}>`;
  return html`<div class=${cls} style=${{ ...extraStyle, background: bg }}>${initials(name)}</div>`;
}

const HOVER_ICONS = {
  github: html`<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2C6.48 2 2 6.58 2 12.26c0 4.52 2.87 8.35 6.84 9.7.5.1.68-.22.68-.48 0-.24-.01-.87-.01-1.7-2.78.62-3.37-1.37-3.37-1.37-.45-1.18-1.11-1.5-1.11-1.5-.91-.64.07-.63.07-.63 1 .07 1.53 1.06 1.53 1.06.89 1.57 2.34 1.12 2.91.86.09-.66.35-1.12.63-1.37-2.22-.26-4.56-1.14-4.56-5.07 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.3.1-2.7 0 0 .84-.27 2.75 1.05A9.2 9.2 0 0 1 12 6.8c.85 0 1.7.12 2.5.34 1.9-1.32 2.74-1.05 2.74-1.05.55 1.4.2 2.44.1 2.7.64.72 1.03 1.63 1.03 2.75 0 3.94-2.34 4.8-4.57 5.06.36.32.68.94.68 1.9 0 1.37-.01 2.48-.01 2.81 0 .27.18.59.69.48A10.03 10.03 0 0 0 22 12.26C22 6.58 17.52 2 12 2z"/></svg>`,
  forum: html`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M21 12a8 8 0 0 1-8 8H7l-4 3V12a8 8 0 0 1 8-8h2a8 8 0 0 1 8 8z"/></svg>`,
  blog: html`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4 11.5-11.5z"/></svg>`,
};

export function profileChannelTabs(user) {
  const githubCount = (user.issues_created || 0) + (user.prs_created || 0);
  const forumCount = (user.topics_created || 0) + (user.replies || 0);
  const blogCount = user.blog_posts || 0;
  return [
    { key: 'github', label: 'GitHub', icon: HOVER_ICONS.github, count: githubCount, active: githubCount > 0 || (user.points_github || 0) > 0 },
    { key: 'forum', label: 'Forum', icon: HOVER_ICONS.forum, count: forumCount, active: forumCount > 0 || (user.points_forum || 0) > 0 },
    { key: 'blog', label: 'Blog', icon: HOVER_ICONS.blog, count: blogCount, active: blogCount > 0 || (user.points_content || 0) > 0 },
  ];
}

export function useProfileHover() {
  const [target, setTarget] = useState(null);
  const timerRef = useRef(null);
  const canHover = typeof window !== 'undefined' && window.matchMedia('(hover: hover)').matches;

  const clearTimer = () => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  };

  const show = (user, el) => {
    if (!canHover || !el) return;
    clearTimer();
    timerRef.current = setTimeout(() => {
      setTarget({ user, rect: el.getBoundingClientRect() });
    }, 140);
  };

  const hide = () => {
    clearTimer();
    timerRef.current = setTimeout(() => setTarget(null), 100);
  };

  const dismiss = () => {
    clearTimer();
    setTarget(null);
  };

  useEffect(() => () => clearTimer(), []);

  return { target, show, hide, dismiss, canHover };
}

function ProfileHoverCard({ user, rect }) {
  const cardRef = useRef(null);
  const [style, setStyle] = useState(null);
  const tabs = profileChannelTabs(user);

  useEffect(() => {
    const card = cardRef.current;
    if (!card || !rect) return;

    const update = () => {
      const cardRect = card.getBoundingClientRect();
      const gap = 14;
      const pad = 12;
      const centerX = rect.left + rect.width / 2;
      let left = centerX;
      let top;
      let placement = 'above';
      const cardH = cardRect.height || 130;

      if (rect.top > cardH + gap + pad) {
        top = rect.top - gap;
        placement = 'above';
      } else {
        top = rect.bottom + gap;
        placement = 'below';
      }

      const half = (cardRect.width || 240) / 2;
      const minLeft = pad + half;
      const maxLeft = window.innerWidth - pad - half;
      left = Math.min(Math.max(left, minLeft), maxLeft);

      setStyle({ left: `${left}px`, top: `${top}px`, placement });
    };

    update();
    requestAnimationFrame(update);
    window.addEventListener('scroll', update, true);
    window.addEventListener('resize', update);
    return () => {
      window.removeEventListener('scroll', update, true);
      window.removeEventListener('resize', update);
    };
  }, [rect, user.user_key]);

  return html`
    <div
      ref=${cardRef}
      class=${'lb-profile-hover' + (style ? ` lb-profile-hover--${style.placement}` : '')}
      style=${style ? {
        left: style.left,
        top: style.top,
        transform: style.placement === 'above' ? 'translate(-50%, -100%)' : 'translate(-50%, 0)',
        visibility: style ? 'visible' : 'hidden',
      } : { visibility: 'hidden' }}
      role="tooltip"
    >
      <div class="lb-profile-hover__name">${user.display_name}</div>
      <div class="lb-profile-hover__pts">${fmtNum(user.points_total || 0)} pts</div>
      <div class="lb-profile-hover__divider"></div>
      <div class="lb-profile-hover__tabs">
        ${tabs.map(tab => html`
          <span class=${'lb-profile-hover__tab' + (tab.active ? ' lb-profile-hover__tab--active' : '')}>
            ${tab.icon}
            <span class="lb-profile-hover__tab-label">${tab.label}</span>
            <span class="lb-profile-hover__tab-count">${fmtNum(tab.count)}</span>
          </span>
        `)}
      </div>
    </div>
  `;
}

export function ProfileHoverPortal({ target }) {
  if (!target) return null;
  return createPortal(
    html`<${ProfileHoverCard} user=${target.user} rect=${target.rect} />`,
    document.body,
  );
}

export function UserDetailModal({ user, period, onClose, theme = 'light' }) {
  const [detail, setDetail] = useState(null);
  const [leaderHistory, setLeaderHistory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const isDark = theme === 'dark';

  useEffect(() => {
    if (!user.user_key) { setLoading(false); return; }
    fetch(`${BASE}/users/${period}/${user.user_key}.json`)
      .then(r => {
        if (r.status === 404) return null;
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(d => { if (d) setDetail(d); setLoading(false); })
      .catch(e => { setError(e.message); setLoading(false); });
  }, [user.user_key, period]);

  useEffect(() => {
    if (!user.user_key) return;
    fetch(`${BASE}/users/leader-history/${user.user_key}.json`)
      .then(r => (r.ok ? r.json() : null))
      .then(h => { if (h?.summit_periods?.length) setLeaderHistory(h); })
      .catch(() => {});
  }, [user.user_key]);

  useEffect(() => {
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = prev; };
  }, []);

  const d = detail || user;
  const handle = handleOf(d);

  const modal = html`
    <div class=${'lb-overlay' + (isDark ? ' lb-overlay--dark' : '')} onClick=${e => { if (e.target === e.currentTarget) onClose(); }}>
      <div class=${'lb-modal-lg' + (isDark ? ' lb-modal-lg--dark' : '')} onClick=${e => e.stopPropagation()}>
        <button class="lb-modal-close" onClick=${e => { e.stopPropagation(); onClose(); }} aria-label="Close">✕</button>

        <div class="lb-modal-header">
          <${Avatar} url=${d.avatar_url} name=${d.display_name} size="lb-avatar-lg" square
                     style=${{ display: 'inline-flex', flexShrink: 0 }} />
          <div class="lb-modal-headcopy">
            <h5 class="lb-modal-name">${d.display_name}</h5>
            ${handle ? html`<div class="lb-modal-handle">@${handle}</div>` : null}
            <div class="lb-modal-pts-row">
              <span class="lb-modal-pts">${fmtNum(d.points_total || 0)}</span>
              <span class="lb-modal-pts-lbl">total points</span>
            </div>
          </div>
        </div>

        <div class="lb-modal-body">
          ${loading ? html`<div class="lb-spinner"></div>` : null}
          ${!loading && error ? html`<div class="lb-state">Could not load contribution details.</div>` : null}

          ${!loading ? html`<${Fragment}>
            ${leaderHistory?.summit_periods?.length ? html`
              <div class="lb-section lb-section--leader">
                <div class="lb-section-title">Global Top 10 (${leaderHistory.summit_periods.length})</div>
                <div class="lb-leader-periods">
                  ${leaderHistory.summit_periods.map(entry => html`
                    <span class=${'lb-leader-chip' + (entry.rank === 1 ? ' lb-leader-chip--gold' : '')}>
                      <span class="lb-leader-chip__rank">#${entry.rank}</span>
                      ${entry.period_label}
                    </span>
                  `)}
                </div>
              </div>
            ` : null}

            ${(d.points_github || d.points_content || d.points_forum) ? html`
              <div class="lb-modal-stats">
                <div class="lb-modal-stat"><div class="v">${fmtNum(d.points_github || 0)}</div><div class="l">GitHub</div></div>
                <div class="lb-modal-stat"><div class="v">${fmtNum(d.points_content || 0)}</div><div class="l">Content</div></div>
                <div class="lb-modal-stat"><div class="v">${fmtNum(d.points_forum || 0)}</div><div class="l">Forum</div></div>
                ${(d.issues_created || d.prs_created) ? html`
                  <div class="lb-modal-stat"><div class="v">${fmtNum((d.issues_created || 0) + (d.prs_created || 0))}</div><div class="l">Issues+PRs</div></div>
                ` : null}
                ${d.solutions ? html`
                  <div class="lb-modal-stat"><div class="v">${fmtNum(d.solutions || 0)}</div><div class="l">Solutions</div></div>
                ` : null}
              </div>
            ` : null}

            ${detail?.github_issues?.length ? html`
              <div class="lb-section">
                <div class="lb-section-title">GitHub Issues (${detail.github_issues.length})</div>
                ${detail.github_issues.map(it => html`
                  <div class="lb-contrib-item">
                    <div class="lb-contrib-left">
                      <span class=${'lb-badge ' + (it.state === 'open' ? 'lb-badge-open' : 'lb-badge-closed')}>${it.state}</span>
                      <a class="lb-contrib-link" href=${it.url} target="_blank" rel="noopener">${it.title}</a>
                    </div>
                    <span class="lb-contrib-meta">${it.repo ? it.repo + ' · ' : ''}${fmtDate(it.date)}</span>
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
                    <span class="lb-contrib-meta">${it.repo ? it.repo + ' · ' : ''}${fmtDate(it.date)}</span>
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
                      <a class="lb-contrib-link" href=${it.url} target="_blank" rel="noopener">${it.topic_title || it.title || 'Reply'}</a>
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
                      <span class="lb-badge" style="background:#653DF4;color:#fff">solution</span>
                      <a class="lb-contrib-link" href=${it.url} target="_blank" rel="noopener">${it.topic_title || it.title || 'Solution'}</a>
                    </div>
                    <span class="lb-contrib-meta">${fmtDate(it.date)}</span>
                  </div>
                `)}
              </div>
            ` : null}

            ${!detail?.github_issues?.length && !detail?.github_prs?.length &&
              !detail?.blog_list?.length && !detail?.forum_topics?.length &&
              !detail?.forum_replies?.length && !detail?.forum_solutions?.length ? html`
              <p class="lb-modal-empty">No detailed contribution data available for this period.</p>
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

  return createPortal(modal, document.body);
}

import { h, render, Fragment } from 'https://esm.sh/preact@10';
import { useState, useEffect } from 'https://esm.sh/preact@10/hooks';
import htm from 'https://esm.sh/htm@3';
import {
  BASE,
  LoadingStatus,
  UserDetailModal,
  ProfileHoverPortal,
  useProfileHover,
  initials,
  nameColor,
} from './lb-shared.js';

const html = htm.bind(h);

/** Percent positions along the mountain ridge (rank 1–10) — desktop. */
const MARKER_POS = [
  { left: 51, top: 6, size: 92 },
  { left: 40, top: 22, size: 76 },
  { left: 58, top: 26, size: 72 },
  { left: 69, top: 32, size: 58 },
  { left: 52, top: 36, size: 58 },
  { left: 35, top: 42, size: 56 },
  { left: 59, top: 45, size: 56 },
  { left: 43, top: 53, size: 54 },
  { left: 28, top: 60, size: 52 },
  { left: 20, top: 68, size: 50 },
];

/** Mobile: spread markers vertically along the visible mountain crop. */
const MARKER_POS_MOBILE = [
  { left: 50, top: 14, size: 64 },
  { left: 40, top: 23, size: 58 },
  { left: 64, top: 26, size: 58 },
  { left: 51, top: 34, size: 56 },
  { left: 37, top: 41, size: 56 },
  { left: 66, top: 47, size: 54 },
  { left: 28, top: 53, size: 52 },
  { left: 54, top: 60, size: 52 },
  { left: 34, top: 68, size: 50 },
  { left: 58, top: 75, size: 48 },
];

function useSummitMobile() {
  const [mobile, setMobile] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia('(max-width: 900px)');
    const update = () => setMobile(mq.matches);
    update();
    mq.addEventListener('change', update);
    return () => mq.removeEventListener('change', update);
  }, []);

  return mobile;
}

function markerSizeClass(size) {
  if (size >= 84) return 'lb-summit-marker--xl';
  if (size >= 68) return 'lb-summit-marker--lg';
  if (size >= 56) return 'lb-summit-marker--md';
  return 'lb-summit-marker--sm';
}

function markerZIndex(rank) {
  return 12 - rank;
}

function SummitMarker({ user, rank, pos, onClick, onHoverShow, onHoverHide, compact }) {
  const isFirst = rank === 1;
  const bg = nameColor(user.display_name);
  const size = pos.size;
  const sizeClass = markerSizeClass(size);
  const markerSize = compact
    ? `clamp(40px, ${size}px, 19vw)`
    : `${size}px`;

  return html`
    <button
      type="button"
      class=${'lb-summit-marker ' + sizeClass}
      style=${{
        left: `${pos.left}%`,
        top: `${pos.top}%`,
        width: markerSize,
        height: markerSize,
        zIndex: markerZIndex(rank),
      }}
      onClick=${() => onClick(user)}
      onMouseEnter=${onHoverShow ? e => onHoverShow(user, e.currentTarget) : undefined}
      onMouseLeave=${onHoverHide || undefined}
      aria-label="${user.display_name}, rank ${rank}"
    >
      <span class="lb-summit-marker__ring">
        ${user.avatar_url
          ? html`<img src=${user.avatar_url} alt="" class="lb-summit-marker__photo"
               onError=${e => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'flex'; }} />
             <span class="lb-summit-marker__fallback" style=${{ display: 'none', background: bg }}>${initials(user.display_name)}</span>`
          : html`<span class="lb-summit-marker__fallback" style=${{ background: bg }}>${initials(user.display_name)}</span>`}
      </span>
      <span class=${'lb-summit-marker__badge' + (isFirst ? ' lb-summit-marker__badge--gold' : '')}>${rank}</span>
    </button>
  `;
}

function SummitApp({ meta }) {
  const period = meta.periods?.find(p => p.key === 'all-time')?.key
    || meta.periods?.find(p => p.type === 'all-time')?.key
    || 'all-time';
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selected, setSelected] = useState(null);
  const { target: hoverTarget, show: showHover, hide: hideHover, dismiss: dismissHover, canHover } = useProfileHover();
  const isMobile = useSummitMobile();
  const markerPositions = isMobile ? MARKER_POS_MOBILE : MARKER_POS;

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    fetch(`${BASE}/global/${period}.json`)
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then(d => { if (!cancelled) { setData(d); setLoading(false); } })
      .catch(e => { if (!cancelled) { setError(e.message); setLoading(false); } });
    return () => { cancelled = true; };
  }, [period]);

  const leaders = data?.top30?.slice(0, 10) || [];

  const openProfile = (user) => {
    dismissHover();
    setSelected(user);
  };

  return html`
    <div class="lb-summit">
      <div class=${'lb-summit-mountain' + (isMobile ? ' lb-summit-mountain--mobile' : '')} aria-live="polite">
        ${loading ? html`<${LoadingStatus} active=${true} />` : null}
        ${error ? html`<div class="lb-state lb-state-error">Error: ${error}</div>` : null}

        ${!loading && !error && leaders.length ? html`<${Fragment}>
          ${leaders.map((user, i) => html`
            <${SummitMarker}
              key=${user.user_key || i}
              user=${user}
              rank=${i + 1}
              pos=${markerPositions[i]}
              onClick=${openProfile}
              onHoverShow=${canHover ? showHover : null}
              onHoverHide=${canHover ? hideHover : null}
              compact=${isMobile}
            />
          `)}
        </${Fragment}>` : null}

        ${!loading && !error && !leaders.length ? html`
          <div class="lb-state">No summit leaders for this period.</div>
        ` : null}
      </div>

      ${selected ? html`
        <${UserDetailModal} user=${selected} period=${period} theme="dark" onClose=${() => setSelected(null)} />
      ` : null}

      ${canHover ? html`<${ProfileHoverPortal} target=${hoverTarget} />` : null}
    </div>
  `;
}

async function init() {
  const el = document.getElementById('lb-summit-widget');
  if (!el) return;
  try {
    const meta = await fetch(`${BASE}/meta.json`).then(r => r.json());
    render(html`<${SummitApp} meta=${meta} />`, el);
  } catch {
    el.innerHTML = '<p class="lb-state">Summit data is not available yet.</p>';
  }
}

init();

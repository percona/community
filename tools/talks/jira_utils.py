"""
Jira SPEAK → Community Talks data layer.

Loads Talks ready for site publication, resolves Conf & Talk / Speaker & Talk,
and writes Community Website URL + Publication Status back to Jira.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# tools/talks/.env, then community/.env (CI/GitHub Actions inject env vars)
_HERE = Path(__file__).resolve().parent
load_dotenv(_HERE / ".env")
load_dotenv(_HERE.parent.parent / ".env")

_raw_jira_url = (os.getenv("JIRA_URL") or "").rstrip("/")
if _raw_jira_url and not _raw_jira_url.startswith(("http://", "https://")):
    _raw_jira_url = f"https://{_raw_jira_url}"
JIRA_URL = _raw_jira_url
JIRA_USER = os.getenv("JIRA_USER")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")

# SPEAK Talk / Conference field IDs (Atlassian custom fields)
PUB_STATUS = "customfield_13507"
COMMUNITY_URL = "customfield_13495"
CONF_URL = "customfield_11932"
TIME = "customfield_11931"
SLIDES = "customfield_13500"
VIDEO = "customfield_13501"
SPEAKERS_FIELD = "customfield_11938"
START_DATE = "customfield_11901"
FINISH_DATE = "customfield_11924"
CITY = "customfield_11920"
TECHNOLOGY = "customfield_13521"
CONF_NAME = "customfield_13520"
SPEAKER_ROLE = "customfield_11926"

CONF_TALK_LINK = "Conf & Talk"
SPEAKER_TALK_LINK = "Speaker & Talk"

PUBLISHABLE_STATUSES = frozenset({"Accepted", "Done"})
# Only queue for site sync. After write-back, status becomes Published.
PUBLISHABLE_PUB_STATUS = frozenset({"Ready for publication"})

_http = requests.Session()
_http.trust_env = False


def require_env() -> None:
    missing = [
        name
        for name, value in [
            ("JIRA_URL", JIRA_URL),
            ("JIRA_USER", JIRA_USER),
            ("JIRA_TOKEN", JIRA_TOKEN),
        ]
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing env vars: {', '.join(missing)}")


def jira_auth() -> HTTPBasicAuth:
    return HTTPBasicAuth(JIRA_USER or "", JIRA_TOKEN or "")


def jira_headers() -> dict[str, str]:
    return {"Accept": "application/json", "Content-Type": "application/json"}


def slugify_name(name: str) -> str:
    """Contributor slug: underscores (matches existing Notion convention)."""
    if not name:
        return ""
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def adf_to_text(value: Any) -> str:
    """Flatten Atlassian Document Format (or plain string) to text."""
    if not value:
        return ""
    if isinstance(value, str):
        return value.strip()
    if not isinstance(value, dict):
        return str(value).strip()

    parts: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            ntype = node.get("type")
            if ntype == "text":
                parts.append(str(node.get("text") or ""))
            elif ntype == "hardBreak":
                parts.append("\n")
            elif ntype in {"paragraph", "heading", "blockquote", "listItem", "codeBlock"}:
                before = len(parts)
                for child in node.get("content") or []:
                    walk(child)
                if ntype == "heading":
                    level = int((node.get("attrs") or {}).get("level") or 2)
                    text = "".join(parts[before:]).strip()
                    del parts[before:]
                    if text:
                        parts.append("#" * level + " " + text + "\n\n")
                elif parts[before:]:
                    parts.append("\n\n")
            else:
                for child in node.get("content") or []:
                    walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)
    text = "".join(parts)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_abstract_notes(text: str) -> str:
    """
    Drop trailing Notes-style lines (YouTube URL, minute markers) that belong
    in the video front-matter field, not the talk body.
    """
    if not text:
        return ""
    lines = text.rstrip().splitlines()
    while lines:
        line = lines[-1].strip()
        if not line:
            lines.pop()
            continue
        if re.fullmatch(
            r"https?://(www\.)?(youtube\.com|youtu\.be)/\S+",
            line,
            flags=re.I,
        ):
            lines.pop()
            continue
        if re.fullmatch(r"\(?\s*minute\s+\d{1,2}:\d{2}(:\d{2})?\s*\)?", line, flags=re.I):
            lines.pop()
            continue
        break
    return "\n".join(lines).strip()


def extract_abstract(description: Any) -> str:
    """
    Prefer ## Abstract section from Talk Description; else full text.
    Matches how migration stores Abstract + Notes in Jira.
    """
    text = adf_to_text(description)
    if not text:
        return ""
    match = re.search(
        r"^##\s*Abstract\s*\n+(.*?)(?=^##\s|\Z)",
        text,
        flags=re.I | re.M | re.S,
    )
    if match:
        text = match.group(1).strip()
    return clean_abstract_notes(text)


def select_value(field: Any) -> str:
    if not field:
        return ""
    if isinstance(field, dict):
        return str(field.get("value") or field.get("name") or "").strip()
    return str(field).strip()


def labels_list(field: Any) -> list[str]:
    if not field:
        return []
    if isinstance(field, list):
        out: list[str] = []
        for item in field:
            if isinstance(item, str) and item.strip():
                out.append(item.strip())
            elif isinstance(item, dict):
                name = str(item.get("value") or item.get("name") or "").strip()
                if name:
                    out.append(name)
        return out
    return []


def url_field(field: Any) -> str:
    if not field:
        return ""
    if isinstance(field, str):
        return field.strip()
    return str(field).strip()


def time_to_date(value: Any) -> str:
    """Jira datetime / date → YYYY-MM-DD for Hugo path."""
    if not value:
        return ""
    text = str(value).strip()
    if len(text) >= 10 and re.match(r"^\d{4}-\d{2}-\d{2}", text):
        return text[:10]
    return ""


def time_to_clock(value: Any) -> str:
    """Optional HH:MM from datetime. Ignore midnight (date-only fields)."""
    if not value:
        return ""
    text = str(value).strip()
    match = re.search(r"T(\d{2}:\d{2})", text)
    if not match:
        return ""
    clock = match.group(1)
    # Jira/Notion date-only values often serialize as T00:00 — not a real talk time.
    if clock == "00:00":
        return ""
    return clock


def jira_search(jql: str, fields: list[str], *, max_results: int = 100) -> list[dict]:
    """Paginated Jira issue search (/rest/api/3/search/jql, legacy /search fallback)."""
    issues: list[dict] = []
    next_token: str | None = None
    start_at = 0
    use_legacy = False

    while True:
        payload: dict[str, Any] = {
            "jql": jql,
            "maxResults": max_results,
            "fields": fields,
        }
        if use_legacy:
            payload["startAt"] = start_at
            url = f"{JIRA_URL}/rest/api/3/search"
        else:
            if next_token:
                payload["nextPageToken"] = next_token
            url = f"{JIRA_URL}/rest/api/3/search/jql"

        response = _http.post(
            url, headers=jira_headers(), auth=jira_auth(), json=payload, timeout=60
        )
        if response.status_code == 404 and not use_legacy:
            use_legacy = True
            continue
        if not response.ok:
            raise RuntimeError(
                f"Jira search failed: {response.status_code} {response.text[:400]}"
            )
        data = response.json()
        batch = data.get("issues") or []
        issues.extend(batch)

        if use_legacy:
            start_at += len(batch)
            total = int(data.get("total") or 0)
            if not batch or start_at >= total:
                break
            continue

        if data.get("isLast", True) or not data.get("nextPageToken"):
            break
        next_token = data["nextPageToken"]

    return issues


def get_issue(key: str, fields: list[str] | None = None) -> dict:
    params: dict[str, Any] = {}
    if fields:
        params["fields"] = ",".join(fields)
    response = _http.get(
        f"{JIRA_URL}/rest/api/3/issue/{key}",
        headers=jira_headers(),
        auth=jira_auth(),
        params=params,
        timeout=60,
    )
    if not response.ok:
        raise RuntimeError(
            f"Jira get {key} failed: {response.status_code} {response.text[:300]}"
        )
    return response.json()


def linked_issues(issue: dict, link_type: str) -> list[dict[str, str]]:
    """Return [{key, summary, issuetype}] for a given link type name."""
    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for link in (issue.get("fields") or {}).get("issuelinks") or []:
        if (link.get("type") or {}).get("name") != link_type:
            continue
        other = link.get("outwardIssue") or link.get("inwardIssue") or {}
        key = str(other.get("key") or "")
        if not key or key in seen:
            continue
        seen.add(key)
        fields = other.get("fields") or {}
        out.append(
            {
                "key": key,
                "summary": str((fields.get("summary") or "")).strip(),
                "issuetype": str(
                    ((fields.get("issuetype") or {}).get("name") or "")
                ).strip(),
            }
        )
    return out


def _norm_conf_name(text: str) -> str:
    return " ".join((text or "").casefold().split())


def best_jira_avatar_url(user: dict[str, Any] | None) -> str:
    """
    Pick the best avatar URL from a Jira user object (Speakers multi-user field).
    Atlassian CDN paths ending in /48|/32|… can be bumped to /256.
    """
    if not user:
        return ""
    urls = user.get("avatarUrls") or {}
    raw = ""
    for size in ("48x48", "32x32", "24x24", "16x16"):
        if urls.get(size):
            raw = str(urls[size]).strip()
            break
    if not raw:
        return ""
    if "avatar-management--avatars." in raw and re.search(r"/\d{2,3}$", raw.rstrip("/")):
        return re.sub(r"/\d{2,3}$", "/256", raw.rstrip("/"))
    return raw


def speakers_avatar_index(fields: dict[str, Any]) -> dict[str, str]:
    """
    Map lookup keys → avatar URL from Talk Speakers picker.

    Keys include normalized displayName and email-local forms so
    ``aldo.junior`` matches speaker name ``Aldo Junior``.
    """
    out: dict[str, str] = {}
    for user in fields.get(SPEAKERS_FIELD) or []:
        url = best_jira_avatar_url(user)
        if not url:
            continue
        name = str((user or {}).get("displayName") or "").strip()
        email = str((user or {}).get("emailAddress") or "").strip()
        local = email.split("@", 1)[0] if email else ""
        for key in (
            _norm_conf_name(name),
            _norm_conf_name(name.replace(".", " ")),
            _norm_conf_name(local.replace(".", " ")),
            _norm_conf_name(local.replace(".", "")),
            _norm_conf_name(re.sub(r"[._]+", " ", name)),
        ):
            if key:
                out[key] = url
    return out


def avatar_for_speaker_name(name: str, avatars: dict[str, str]) -> str:
    """Resolve avatar URL for a Speaker issue / person name."""
    raw = (name or "").strip()
    if not raw:
        return ""
    keys = [
        _norm_conf_name(raw),
        _norm_conf_name(raw.replace(".", " ")),
        _norm_conf_name(re.sub(r"[\s._-]+", "", raw)),
    ]
    for key in keys:
        if key and key in avatars:
            return avatars[key]
    # Token match: all name tokens appear in some avatar key (aldo junior ⊂ aldo junior)
    tokens = [t for t in re.split(r"[\s._-]+", raw.casefold()) if len(t) > 1]
    if len(tokens) >= 2:
        for key, url in avatars.items():
            key_tokens = [t for t in re.split(r"[\s._-]+", key) if len(t) > 1]
            compact_key = re.sub(r"[\s._-]+", "", key)
            if all(t in key_tokens or t in compact_key for t in tokens):
                return url
    return ""


def pick_conference_link(
    conf_links: list[dict[str, str]],
    conference_name: str,
) -> dict[str, str] | None:
    """
    Resolve which Conference a Talk belongs to.

    - 0 links → None
    - 1 link → that Conference (Conference Name is ignored)
    - 2+ links → pick the one whose summary matches Conference Name
    """
    if not conf_links:
        return None
    if len(conf_links) == 1:
        return conf_links[0]

    wanted = _norm_conf_name(conference_name)
    if wanted:
        for link in conf_links:
            if _norm_conf_name(link.get("summary") or "") == wanted:
                return link
        for link in conf_links:
            summary = _norm_conf_name(link.get("summary") or "")
            if wanted in summary or summary in wanted:
                return link
        print(
            f"⚠️ No Conf & Talk match for Conference Name {conference_name!r}; "
            f"using {conf_links[0].get('key')}"
        )
    return conf_links[0]


TALK_FIELDS = [
    "summary",
    "description",
    "status",
    "labels",
    "issuelinks",
    PUB_STATUS,
    COMMUNITY_URL,
    CONF_URL,
    TIME,
    SLIDES,
    VIDEO,
    SPEAKERS_FIELD,
    CONF_NAME,
    TECHNOLOGY,
]

CONF_FIELDS = [
    "summary",
    CONF_URL,
    START_DATE,
    FINISH_DATE,
    CITY,
    TECHNOLOGY,
]

SPEAKER_FIELDS = [
    "summary",
    SPEAKER_ROLE,
]


def publishable_jql(
    *,
    jira_key: str | None = None,
    include_published: bool = False,
) -> str:
    if jira_key:
        # Explicit key: sync that Talk regardless of Publication Status
        # (re-publish / fix). Queue sync uses Ready only.
        return (
            f'project = SPEAK AND issuetype = Talk AND key = {jira_key}'
        )
    # Talks queue: Ready only. Events pages: Ready + already Published on site.
    if include_published:
        pub_clause = (
            'AND "Publication Status" in ("Ready for publication", Published) '
        )
    else:
        pub_clause = 'AND "Publication Status" = "Ready for publication" '
    return (
        'project = SPEAK AND issuetype = Talk '
        'AND status in (Accepted, Done) '
        f'{pub_clause}'
        'ORDER BY updated DESC'
    )


def load_conference(key: str) -> dict[str, Any]:
    issue = get_issue(key, CONF_FIELDS)
    fields = issue.get("fields") or {}
    city = fields.get(CITY)
    if isinstance(city, str):
        location = city.strip()
    else:
        location = str(city or "").strip()
    return {
        "key": key,
        "name": str(fields.get("summary") or "").strip(),
        "url": url_field(fields.get(CONF_URL)),
        "date_start": time_to_date(fields.get(START_DATE)),
        "date_end": time_to_date(fields.get(FINISH_DATE)),
        "location": location,
        "technology": labels_list(fields.get(TECHNOLOGY)),
    }


def load_speaker(key: str) -> dict[str, Any]:
    issue = get_issue(key, SPEAKER_FIELDS)
    fields = issue.get("fields") or {}
    name = str(fields.get("summary") or "").strip()
    role = fields.get(SPEAKER_ROLE)
    if isinstance(role, dict):
        role_text = str(role.get("value") or "").strip()
    else:
        role_text = str(role or "").strip()
    return {
        "key": key,
        "Name": name,
        "Role": role_text,
        "Status": "available",  # assume current unless we know otherwise
        "slug": slugify_name(name),
        "Tagline": "",
        "Technology": "",
        "Bio": "",
        "LinkedIn": "",
        "Twitter": "",
        "GitHub": "",
        "Website": "",
        "Facebook": "",
    }


def issue_to_site_talk(issue: dict) -> dict[str, Any]:
    """Normalize a Jira Talk issue into a site-facing record."""
    key = str(issue.get("key") or "")
    fields = issue.get("fields") or {}
    status = str(((fields.get("status") or {}).get("name") or "")).strip()
    pub = select_value(fields.get(PUB_STATUS))

    conf_links = linked_issues(issue, CONF_TALK_LINK)
    speaker_links = linked_issues(issue, SPEAKER_TALK_LINK)
    conf_name = str(fields.get(CONF_NAME) or "").strip()

    event: dict[str, Any] = {
        "key": "",
        "name": conf_name,
        "url": "",
        "date_start": "",
        "date_end": "",
        "location": "",
        "technology": labels_list(fields.get(TECHNOLOGY)),
    }
    chosen = pick_conference_link(conf_links, conf_name)
    if chosen:
        conf = load_conference(chosen["key"])
        event = conf
        if not event.get("name"):
            event["name"] = chosen.get("summary") or conf_name or ""
    speakers: list[dict[str, Any]] = []
    avatars = speakers_avatar_index(fields)

    def _with_avatar(sp: dict[str, Any]) -> dict[str, Any]:
        if not sp.get("avatar_url"):
            sp["avatar_url"] = avatar_for_speaker_name(sp.get("Name") or "", avatars)
        return sp

    if speaker_links:
        for link in speaker_links:
            try:
                speakers.append(_with_avatar(load_speaker(link["key"])))
            except Exception as exc:
                print(f"⚠️ Speaker {link.get('key')}: {exc}")
                name = link.get("summary") or "Unknown"
                speakers.append(
                    _with_avatar(
                        {
                            "key": link.get("key") or "",
                            "Name": name,
                            "Role": "",
                            "Status": "available",
                            "slug": slugify_name(name),
                            "Tagline": "",
                            "Technology": "",
                            "Bio": "",
                            "LinkedIn": "",
                            "Twitter": "",
                            "GitHub": "",
                            "Website": "",
                            "Facebook": "",
                        }
                    )
                )
    else:
        # Fallback: Speakers multi-user picker → displayName + avatar
        for user in fields.get(SPEAKERS_FIELD) or []:
            name = str((user or {}).get("displayName") or "").strip()
            if not name:
                continue
            speakers.append(
                {
                    "key": "",
                    "Name": name,
                    "Role": "",
                    "Status": "available",
                    "slug": slugify_name(name),
                    "Tagline": "",
                    "Technology": "",
                    "Bio": "",
                    "LinkedIn": "",
                    "Twitter": "",
                    "GitHub": "",
                    "Website": "",
                    "Facebook": "",
                    "avatar_url": best_jira_avatar_url(user),
                }
            )

    time_raw = fields.get(TIME)
    return {
        "key": key,
        "id": key,  # Hugo id — Jira key replaces Notion UUID
        "title": str(fields.get("summary") or "").strip(),
        "abstract": extract_abstract(fields.get("description")),
        "slides": url_field(fields.get(SLIDES)),
        "video": url_field(fields.get(VIDEO)),
        "labels": labels_list(fields.get("labels")),
        "presentation_date": time_to_date(time_raw),
        "presentation_time": time_to_clock(time_raw),
        "talk_url": url_field(fields.get(CONF_URL)),
        "status": status,
        "publication_status": pub,
        "community_url": url_field(fields.get(COMMUNITY_URL)),
        "event": event,
        "speakers": speakers,
    }


def load_talks(
    *,
    jira_key: str | None = None,
    include_published: bool = False,
) -> list[dict[str, Any]]:
    """
    Load publishable Talks from Jira, enriched with Conference + Speakers.

    include_published: also load Published (for event pages / Talks lists).
    Default False = Ready for publication queue only.
    """
    require_env()
    jql = publishable_jql(jira_key=jira_key, include_published=include_published)
    print(f"JQL: {jql}")
    raw = jira_search(jql, TALK_FIELDS)
    print(f"Found {len(raw)} Talk issue(s)")
    talks: list[dict[str, Any]] = []
    for issue in raw:
        try:
            talks.append(issue_to_site_talk(issue))
        except Exception as exc:
            print(f"❌ Skip {issue.get('key')}: {exc}")
    return talks


def patch_talk(jira_key: str, url: str) -> None:
    """
    Write Community Website URL + set Publication Status to Published.
    """
    require_env()
    payload = {
        "fields": {
            COMMUNITY_URL: url,
            PUB_STATUS: {"value": "Published"},
        }
    }
    response = _http.put(
        f"{JIRA_URL}/rest/api/3/issue/{jira_key}",
        headers=jira_headers(),
        auth=jira_auth(),
        params={"notifyUsers": "false"},
        json=payload,
        timeout=60,
    )
    if not response.ok:
        raise RuntimeError(
            f"Jira patch {jira_key} failed: {response.status_code} {response.text[:400]}"
        )
    print(f"🔄 Jira updated for {jira_key}: {url}")

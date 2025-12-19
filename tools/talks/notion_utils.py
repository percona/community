import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()

NOTION_SECRET = os.getenv("NOTION_SECRET")
TALKS_ID = os.getenv("NOTION_TALKS_ID")
SPEAKERS_ID = os.getenv("NOTION_SPEAKERS_ID")
EVENTS_ID = os.getenv("NOTION_EVENTS_ID")

BASE_URL = "https://api.notion.com/v1/data_sources"

HEADERS = {
    "Authorization": f"Bearer {NOTION_SECRET}",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json"
}

def query_datasource(datasource_id, payload=None):
    """
    Query a Notion datasource and return all results, handling pagination.

    Args:
        datasource_id (str): The ID of the datasource to query.
        payload (dict, optional): Additional query filters or parameters.

    Returns:
        dict: A dictionary containing all results under the "results" key.
    """
    url = f"{BASE_URL}/{datasource_id}/query"
    all_results = []
    next_cursor = None

    while True:
        body = payload.copy() if payload else {}
        if next_cursor:
            body["start_cursor"] = next_cursor

        response = requests.post(url, headers=HEADERS, json=body)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        all_results.extend(results)

        if not data.get("has_more"):
            break
        next_cursor = data.get("next_cursor")

    return {"results": all_results}


def retrieve_datasource(datasource_id):
    """
    Retrieve the schema and metadata of a Notion datasource.

    Args:
        datasource_id (str): The ID of the datasource.

    Returns:
        dict: JSON response containing datasource schema and metadata.
    """
    url = f"{BASE_URL}/{datasource_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def extract_value(prop):
    """
    Extract a human-readable value from a Notion property object.

    Args:
        prop (dict): A property object from Notion.

    Returns:
        str | dict: The extracted value depending on property type.
    """
    if not prop:
        return ""
    t = prop.get("type")
    if t == "title":
        return " ".join([p.get("plain_text", "") for p in prop.get("title", [])])
    if t == "rich_text":
        return " ".join([p.get("plain_text", "") for p in prop.get("rich_text", [])])
    if t == "status":
        return (prop.get("status") or {}).get("name", "")
    if t == "select":
        return (prop.get("select") or {}).get("name", "")
    if t == "multi_select":
        return ", ".join([s.get("name", "") for s in (prop.get("multi_select") or [])])
    if t == "date":
        date_obj = prop.get("date")
        if isinstance(date_obj, dict):
            return {
                "start": date_obj.get("start", ""),
                "end": date_obj.get("end", "")
            }
        return {"start": "", "end": ""}
    if t == "url":
        return prop.get("url", "") or ""
    if t == "files":
        files = prop.get("files")
        if isinstance(files, list):
            return ", ".join([f.get("name", "") for f in files])
        return ""
    if t == "people":
        people = prop.get("people")
        if isinstance(people, list):
            return ", ".join([p.get("name", "") for p in people])
        return ""
    return str(prop)


def slugify_name(name: str) -> str:
    """
    Convert a string into a slug-friendly format using underscores.

    Args:
        name (str): The input string.

    Returns:
        str: Slugified version of the string.
    """
    if not name:
        return ""
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def load_speakers():
    """
    Load all speakers from the Notion datasource.

    Returns:
        tuple: (speakers_fields, speakers_map)
            - speakers_fields: Schema of the speakers datasource.
            - speakers_map: Dictionary mapping speaker IDs to their properties.
    """
    schema = retrieve_datasource(SPEAKERS_ID)
    speakers_fields = schema.get("properties", {})

    payload = {
        "filter": {
            "property": "Talks",
            "relation": {"is_not_empty": True}
        }
    }
    data = query_datasource(SPEAKERS_ID, payload)
    results = data.get("results", [])

    speakers_map = {}
    for sp in results:
        props = sp.get("properties", {})
        sp_id = sp.get("id")
        sp_values = {}
        for field_name in speakers_fields.keys():
            sp_values[field_name] = extract_value(props.get(field_name))
        sp_values["slug"] = slugify_name(sp_values.get("Name", ""))
        speakers_map[sp_id] = sp_values

    return speakers_fields, speakers_map


def load_events():
    """
    Load all events from the Notion datasource.

    Returns:
        tuple: (events_fields, events_map)
            - events_fields: Schema of the events datasource.
            - events_map: Dictionary mapping event IDs to their properties.
    """
    schema = retrieve_datasource(EVENTS_ID)
    events_fields = schema.get("properties", {})

    payload = {
        "filter": {
            "property": "Talks",
            "relation": {"is_not_empty": True}
        }
    }
    data = query_datasource(EVENTS_ID, payload)
    results = data.get("results", [])

    events_map = {}
    for ev in results:
        props = ev.get("properties", {})
        ev_id = ev.get("id")
        ev_values = {}
        for field_name in events_fields.keys():
            ev_values[field_name] = extract_value(props.get(field_name))
        events_map[ev_id] = ev_values

    return events_fields, events_map


def load_talks():
    """
    Load all talks that are ready for publication or already published,
    and whose event status is Done or Accepted.

    Returns:
        list: List of talk objects from Notion.
    """
    payload = {
        "filter": {
            "and": [
                {
                    "or": [
                        {"property": "Publication Status", "status": {"equals": "Ready for Publication"}},
                        {"property": "Publication Status", "status": {"equals": "Published"}}
                    ]
                },
                {
                    "or": [
                        {"property": "Event Status", "select": {"equals": "Done"}},
                        {"property": "Event Status", "select": {"equals": "Accepted"}}
                    ]
                }
            ]
        }
    }
    data = query_datasource(TALKS_ID, payload)
    return data.get("results", [])


def patch_talk(talk_id: str, url: str):
    """
    Update a talk in Notion:
      - Set Community Website URL to the given URL.
      - Set Publication Status to "Published".

    Args:
        talk_id (str): The ID of the talk page in Notion.
        url (str): The new URL to set in the talk's properties.
    """
    patch_url = f"https://api.notion.com/v1/pages/{talk_id}"
    payload = {
        "properties": {
            "Community Website URL": {"url": url},
            "Publication Status": {"status": {"name": "Published"}}
        }
    }
    response = requests.patch(patch_url, headers=HEADERS, json=payload)
    response.raise_for_status()
    print(f"🔄 Notion updated for {talk_id}: {url}")

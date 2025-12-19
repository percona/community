import sys

def print_props(props: dict, stop: bool = False):
    """
    Print all fields and values from the props dictionary (Notion properties).
    Uses extract_value for normalization (if applied externally).
    If stop=True — terminate the script after printing.
    """
    if not props:
        print("⚠️ Props is empty")
        if stop:
            sys.exit(1)
        return

    print("🗂 Props dump:")
    for field, value in props.items():
        print(f"{field}: {value}")

    if stop:
        sys.exit(1)


def print_count(obj, stop: bool = False):
    """
    Print the number of items in a map (dict) or array (list).
    If stop=True — terminate the script after printing.
    """
    if isinstance(obj, dict):
        count = len(obj)
    elif isinstance(obj, list):
        count = len(obj)
    else:
        print("⚠️ Unsupported type for print_count")
        if stop:
            sys.exit(1)
        return

    print(f"🔢 Count: {count}")
    if stop:
        sys.exit(1)


def print_first(obj_map: dict, stop: bool = False):
    """
    Print the first object from a map (dict of dicts) with its fields and values.
    If stop=True — terminate the script after printing.
    """
    if not obj_map:
        print("⚠️ Map is empty")
        if stop:
            sys.exit(1)
        return

    first_id = next(iter(obj_map))
    print(f"🔎 First object ID: {first_id}")
    for field, value in obj_map[first_id].items():
        print(f"  {field}: {value}")

    if stop:
        sys.exit(1)


def print_field_list(obj_map: dict, field: str, limit: int = 10, stop: bool = False):
    """
    Print a list of values for the specified field from the first `limit` objects.
    If stop=True — terminate the script after printing.
    """
    if not obj_map:
        print("⚠️ Map is empty")
        if stop:
            sys.exit(1)
        return

    print(f"📋 Field '{field}' values (limit {limit}):")
    for i, (obj_id, obj) in enumerate(obj_map.items()):
        if i >= limit:
            break
        value = obj.get(field, None)
        print(f"  {i+1}. {value}")

    if stop:
        sys.exit(1)


def print_all_fields(obj_map: dict, limit: int = 1, stop: bool = False):
    """
    Print all fields and values for the first `limit` objects.
    If stop=True — terminate the script after printing.
    """
    if not obj_map:
        print("⚠️ Map is empty")
        if stop:
            sys.exit(1)
        return

    print(f"🗂 Printing all fields for first {limit} objects:")
    for i, (obj_id, obj) in enumerate(obj_map.items()):
        if i >= limit:
            break
        print(f"\n🔎 Object {i+1} \n  ID: {obj_id}")
        for field, value in obj.items():
            print(f"  {field}: {value}")

    if stop:
        sys.exit(1)

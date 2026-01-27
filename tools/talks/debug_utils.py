import sys
import pprint

def dd(*args, sep="\n", file=sys.stderr):
    """
    Dump and die: pretty-prints any number of variables and exits immediately.

    Usage:
        dd(my_var)
        dd(var1, var2, "debug label", some_dict)

    Args:
        *args: Any number of objects to print
        sep: Separator between objects (default: newline)
        file: Output stream (default: stderr, to avoid mixing with stdout data)
    """
    printer = pprint.PrettyPrinter(indent=2, width=80, compact=False, stream=file)
    for i, arg in enumerate(args):
        if i > 0:
            print(sep, file=file)
        printer.pprint(arg)
    sys.exit(1)

def ddd(*args, sep="\n", file=sys.stderr):
    """
    Dump only: pretty-prints variables without exiting.
    Use for temporary debugging.
    """
    printer = pprint.PrettyPrinter(indent=2, width=80, compact=False, stream=file)
    for i, arg in enumerate(args):
        if i > 0:
            print(sep, file=file)
        printer.pprint(arg)

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

def print_count(obj, label: str = "Items", stop: bool = False):
    """
    Prints the count of items in a dictionary or list with a custom label.
    
    Args:
        obj: dict or list to count
        label: Label to display (e.g., "Speakers", "Talks")
        stop: If True, exits the script after printing
    """
    if isinstance(obj, dict):
        count = len(obj)
    elif isinstance(obj, list):
        count = len(obj)
    else:
        print(f"⚠️ Unsupported type for print_count: {type(obj).__name__}")
        if stop:
            sys.exit(1)
        return

    print(f"📊 {label}: {count}")
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

def print_all_fields(obj, limit: int = 1, stop: bool = False):
    """
    Print all fields and values for the first `limit` objects.
    Works with both:
      - list of dicts (e.g. talks, speakers from Notion results)
      - dict of dicts (e.g. speakers_map, events_map)

    If stop=True — terminate the script after printing.
    """
    if not obj:
        print("⚠️ Input is empty")
        if stop:
            sys.exit(1)
        return

    if isinstance(obj, dict):
        items = list(obj.items())
        print(f"🗂 Printing first {limit} items from dict (ID → fields):")
    elif isinstance(obj, list):
        items = [(f"item_{i}", item) for i, item in enumerate(obj)]
        print(f"🗂 Printing first {limit} items from list:")
    else:
        print("⚠️ Unsupported type. Expected list or dict.")
        if stop:
            sys.exit(1)
        return

    for i, (obj_id, obj_data) in enumerate(items):
        if i >= limit:
            break
        print(f"\n🔎 Object {i+1}")
        print(f"  ID: {obj_id}")
        if isinstance(obj_data, dict):
            for field, value in obj_data.items():
                print(f"    {field}: {value}")
        else:
            print(f"    Value: {obj_data}")

    if stop:
        sys.exit(1)


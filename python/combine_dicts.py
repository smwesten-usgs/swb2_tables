# based on code from https://stackoverflow.com/questions/67993940/python-recursively-append-dictionary-to-another

def combine_lists(a: list, b: list) -> list:
    """combine lists, but drop duplicate list items

    Args:
        a (list): Python list object
        b (list): Second Python list object

    Returns:
        list: new list object containing no duplicated list items
    """
    return a + [i for i in b if i not in a]

def combine_strs(a: str, b: str) -> str:
    """combine strings, only if they are not duplicates of one another

    Args:
        a (str): Python string object
        b (str): Second Python string object

    Returns:
        str/list: string containing the unique string value, or a containing both strings, if they are not duplicates of one another
    """
    if a == b:
        return a
    return [a, b]

class EMPTY:
    "A sentinel representing an empty value."

def combine_dicts(a: dict, b: dict) -> dict:
    output = {}
    # make a complete list of keys (unique values only) from both dicts
    keys = list(a) + [k for k in b if k not in a]
    for key in keys:
        aval = a.get(key, EMPTY)
        bval = b.get(key, EMPTY)
        if isinstance(aval, list) and isinstance(bval, list):
            output[key] = combine_lists(aval, bval)
        elif isinstance(aval, str) and isinstance(bval, str):
            output[key] = combine_strs(aval, bval)
        elif isinstance(aval, dict) and isinstance(bval, dict):
            output[key] = combine_dicts(aval, bval)
        elif bval is EMPTY:
            output[key] = aval
        elif aval is EMPTY:
            output[key] = bval
        else:
            raise RuntimeError(
                f"Cannot combine types: {type(aval)} and {type(bval)}"
            )
    return output
# utils.py
def access_nested_map(nested_map, path):
    """Access a value in a nested dictionary using a tuple path"""
    current = nested_map
    for key in path:
        if key not in current:
            raise KeyError(key)
        current = current[key]
    return current

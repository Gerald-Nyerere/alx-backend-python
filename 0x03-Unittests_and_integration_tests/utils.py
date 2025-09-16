import requests

def access_nested_map(nested_map, path):
    """Access a value in a nested dictionary using a tuple path"""
    current = nested_map
    for key in path:
        if not isinstance(current, dict):
            raise KeyError(key)
        if key not in current:
            raise KeyError(key)
        current = current[key]
    return current

def get_json(url):
    """Fetch JSON data from a URL and return it as a Python dict"""
    response = requests.get(url)
    return response.json()

def memoize(method):
    """Decorator to cache method result as a property"""
    attr_name = "_{}".format(method.__name__)

    @property
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)
    return memoized
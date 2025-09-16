# client.py
from utils import get_json

class GithubOrgClient:
    """Client to interact with GitHub organizations"""

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        """Fetch org data from GitHub"""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)

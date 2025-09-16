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
    
    @property
    def _public_repos_url(self):
        return self.org.get("repos_url")
    
    def public_repos(self):
        """Return list of public repository names"""
        repos = get_json(self._public_repos_url)

        if license:
            licensed_repos = [repo for repo in repos if self.has_license(repo, license)]
            return [repo["name"] for repo in licensed_repos]

        return [repo["name"] for repo in repos]
    
    @staticmethod
    def has_license(repo, license_key):
        """Check if repo has the given license key"""
        return repo.get("license", {}).get("key") == license_key

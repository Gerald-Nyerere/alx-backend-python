#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org calls get_json once with correct URL"""
        # Arrange: fake return value for get_json
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        # Act: create client and call .org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert: get_json was called with correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)

    #!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org calls get_json once with correct URL"""
        # Arrange: fake return value for get_json
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        # Act: create client and call .org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert: get_json was called with correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that GithubOrgClient.public_repos returns the expected list of repos"""
        # Arrange
        fake_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = fake_repos_payload

        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://fake-url.com/repos"

            # Act
            client = GithubOrgClient("google")
            result = client.public_repos()

            # Assert
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_repos)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://fake-url.com/repos")

    @patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns repos_url from org payload"""
        # Arrange: fake payload with repos_url
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}

        client = GithubOrgClient("google")
        result = client._public_repos_url

        # Assert: result matches repos_url from fake payload
        self.assertEqual(result, "https://api.github.com/orgs/google/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct boolean"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)



if __name__ == "__main__":
    unittest.main()

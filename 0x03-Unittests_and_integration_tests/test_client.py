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

    @patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns repos_url from org payload"""
        # Arrange: fake payload with repos_url
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}

        client = GithubOrgClient("google")
        result = client._public_repos_url

        # Assert: result matches repos_url from fake payload
        self.assertEqual(result, "https://api.github.com/orgs/google/repos")



if __name__ == "__main__":
    unittest.main()

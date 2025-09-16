#!/usr/bin/env python3
"""Test module for GithubOrgClient class - unit and integration tests"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized_class
from parameterized import parameterized
from client import GithubOrgClient

# --- Test Fixtures ---
TEST_PAYLOAD = [
    (
        # org_payload
        {
            "login": "google",
            "id": 1342004,
            "url": "https://api.github.com/orgs/google",
            "repos_url": "https://api.github.com/orgs/google/repos",
            "name": "Google",
            "blog": "https://opensource.google.com/",
            "public_repos": 100
        },
        # repos_payload
        [
            {
                "id": 1,
                "name": "repo1",
                "full_name": "google/repo1",
                "private": False,
                "owner": {
                    "login": "google",
                    "id": 1342004
                },
                "html_url": "https://github.com/google/repo1",
                "description": "Google's first repo",
                "fork": False,
                "url": "https://api.github.com/repos/google/repo1",
                "license": {
                    "key": "apache-2.0",
                    "name": "Apache License 2.0",
                    "spdx_id": "Apache-2.0"
                }
            },
            {
                "id": 2,
                "name": "repo2",
                "full_name": "google/repo2",
                "private": False,
                "owner": {
                    "login": "google",
                    "id": 1342004
                },
                "html_url": "https://github.com/google/repo2",
                "description": "Google's second repo",
                "fork": False,
                "url": "https://api.github.com/repos/google/repo2",
                "license": {
                    "key": "mit",
                    "name": "MIT License",
                    "spdx_id": "MIT"
                }
            },
            {
                "id": 3,
                "name": "repo3",
                "full_name": "google/repo3",
                "private": False,
                "owner": {
                    "login": "google",
                    "id": 1342004
                },
                "html_url": "https://github.com/google/repo3",
                "description": "Google's third repo",
                "fork": False,
                "url": "https://api.github.com/repos/google/repo3",
                "license": {
                    "key": "apache-2.0",
                    "name": "Apache License 2.0",
                    "spdx_id": "Apache-2.0"
                }
            }
        ],
        # expected_repos
        ["repo1", "repo2", "repo3"],
        # apache2_repos
        ["repo1", "repo3"]
    )
]


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org calls get_json once"""
        # Arrange
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        # Act
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert
        url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(url)
        self.assertEqual(result, expected_payload)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that GithubOrgClient.public_repos returns repos"""
        fake_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = fake_repos_payload

        mock_path = 'client.GithubOrgClient._public_repos_url'
        with patch(mock_path, new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://fake-url.com/repos"

            client = GithubOrgClient("google")
            result = client.public_repos()

            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://fake-url.com/repos")

    @patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns repos_url from org"""
        repos_url = "https://api.github.com/orgs/google/repos"
        mock_org.return_value = {"repos_url": repos_url}

        client = GithubOrgClient("google")
        expected_url = "https://api.github.com/orgs/google/repos"
        self.assertEqual(client._public_repos_url, expected_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": None}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct boolean"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


# ----------------- INTEGRATION TESTS -----------------
@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos method"""

    @classmethod
    def setUpClass(cls):
        """Set up class method to mock get_json"""
        cls.get_patcher = patch('client.get_json')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if 'orgs/' in url and '/repos' not in url:
                return cls.org_payload
            elif 'repos' in url:
                return cls.repos_payload
            return {}

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class method to stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method with integration"""
        client = GithubOrgClient("google")
        repos = client.public_repos()

        # Verify the returned repositories match expected_repos
        self.assertEqual(repos, self.expected_repos)

        # Verify get_json was called twice (org + repos)
        self.assertEqual(self.mock_get_json.call_count, 2)

    def test_public_repos_with_license(self):
        """Test public_repos method with license filter"""
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")

        self.assertEqual(repos, self.apache2_repos)
        self.assertIn("repo1", repos)
        self.assertIn("repo3", repos)
        self.assertNotIn("repo2", repos)


if __name__ == "__main__":
    unittest.main()

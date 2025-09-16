#!/usr/bin/env python3
import unittest
from unittest.mock import patch
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


if __name__ == "__main__":
    unittest.main()

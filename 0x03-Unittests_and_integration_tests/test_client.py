#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized_class
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD

# --- Fixtures (from fixtures.py) ---
org_payload = {
    "login": "google",
    "repos_url": "https://api.github.com/orgs/google/repos"
}

repos_payload = [
    {"id": 1, "name": "repo1", "license": {"key": "apache-2.0"}},
    {"id": 2, "name": "repo2", "license": {"key": "other-license"}},
    {"id": 3, "name": "repo3", "license": {"key": "apache-2.0"}},
]

expected_repos = ["repo1", "repo2", "repo3"]
apache2_repos = ["repo1", "repo3"]


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org calls get_json once with correct URL"""
        # Arrange
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        # Act
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that GithubOrgClient.public_repos returns the expected list of repos"""
        fake_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = fake_repos_payload

        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://fake-url.com/repos"

            client = GithubOrgClient("google")
            result = client.public_repos()

            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://fake-url.com/repos")

    @patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns repos_url from org payload"""
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}

        client = GithubOrgClient("google")
        self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/google/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct boolean"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


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
        """Set up class method to mock requests.get"""
        # Create a dictionary to map URLs to their corresponding responses
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        
        # Define side_effect function to return different responses based on URL
        def side_effect(url, *args, **kwargs):
            class MockResponse:
                @staticmethod
                def json():
                    if 'orgs/' in url and '/repos' not in url:
                        return cls.org_payload
                    elif 'repos' in url:
                        return cls.repos_payload
                    return {}
                
                @staticmethod
                def raise_for_status():
                    """Mock raise_for_status method"""
                    pass
            
            return MockResponse()
        
        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class method to stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method with integration"""
        # Reset mock call count to isolate this test
        self.mock_get.reset_mock()
        
        client = GithubOrgClient("test-org")
        repos = client.public_repos()
        
        # Verify the returned repositories match expected_repos
        self.assertEqual(repos, self.expected_repos)
        
        # Verify requests.get was called twice (org + repos)
        self.assertEqual(self.mock_get.call_count, 2)
        
        # Verify the correct URLs were called
        call_urls = [call[0][0] for call in self.mock_get.call_args_list]
        
        # Should call organization endpoint first
        self.assertIn("https://api.github.com/orgs/test-org", call_urls[0])
        # Should call repos endpoint second
        self.assertIn("https://api.github.com/orgs/test-org/repos", call_urls[1])

    def test_public_repos_with_license(self):
        """Test public_repos method with license filter"""
        # Reset mock call count to isolate this test
        self.mock_get.reset_mock()
        
        client = GithubOrgClient("test-org")
        repos = client.public_repos(license="apache-2.0")
        
        self.assertEqual(repos, self.apache2_repos)

        self.assertIn("repo1", repos)
        self.assertIn("repo3", repos)
        self.assertNotIn("repo2", repos) 
        
        self.assertEqual(self.mock_get.call_count, 2)
        
        # Verify the correct URLs were called
        call_urls = [call[0][0] for call in self.mock_get.call_args_list]
        
        # Should call organization endpoint first
        self.assertIn("https://api.github.com/orgs/test-org", call_urls[0])
        # Should call repos endpoint second
        self.assertIn("https://api.github.com/orgs/test-org/repos", call_urls[1])

    def test_public_repos_caching(self):
        """Test that public_repos caches results properly"""
        # Reset mock call count
        self.mock_get.reset_mock()
        
        client = GithubOrgClient("test-org")
        
        # First call - should make API calls
        repos1 = client.public_repos()
        self.assertEqual(self.mock_get.call_count, 2)
        
        # Second call - should use cached result, no additional API calls
        repos2 = client.public_repos()
        self.assertEqual(self.mock_get.call_count, 2)  # Should not increase
        self.assertEqual(repos1, repos2)
        
        # Third call with different license - should use cached repos but filter them
        apache_repos = client.public_repos(license="apache-2.0")
        self.assertEqual(self.mock_get.call_count, 2)  # Should not increase
        self.assertEqual(apache_repos, self.apache2_repos)

    def test_public_repos_empty_result(self):
        """Test public_repos with empty repository list"""
        # Reset mock and temporarily modify repos_payload to be empty
        self.mock_get.reset_mock()
        
        original_repos_payload = self.repos_payload
        self.repos_payload = []  # Empty repository list
        
        try:
            client = GithubOrgClient("test-org")
            repos = client.public_repos()
            
            # Should return empty list
            self.assertEqual(repos, [])
            self.assertEqual(self.mock_get.call_count, 2)
        finally:
            # Restore original repos_payload
            self.repos_payload = original_repos_payload

if __name__ == "__main__":
    unittest.main()

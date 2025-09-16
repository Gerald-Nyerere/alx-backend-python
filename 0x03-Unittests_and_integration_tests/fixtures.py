#!/usr/bin/env python3
"""Test fixtures for GithubOrgClient integration tests"""

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
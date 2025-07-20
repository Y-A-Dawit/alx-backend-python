#!/usr/bin/env python3

"""
Test suite for the GithubOrgClient class methods.
"""


import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient  # adjust import if needed


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')  # patch get_json in the client module
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns the expected data."""
        # Setup mock return value
        expected = {"login": org_name}
        mock_get_json.return_value = expected

        # Create client instance and call org
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert that get_json was called once with the right URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        # Assert the org property returns the mock data
        self.assertEqual(result, expected)

    @patch('client.get_json')
    def test_public_repos_url(self, mock_get_json):
        """Test GithubOrgClient._public_repos_url returns correct repos_url from org property."""
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            # Setup the mock to return a dict with repos_url
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}

            client = GithubOrgClient("google")
            result = client._public_repos_url
            expected = "https://api.github.com/orgs/google/repos"

            self.assertEqual(result, expected)
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns list of repo names correctly."""
        
        # Mock the return value of get_json to a list of repo dicts
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]

        client = GithubOrgClient("some_org")

        # Patch the _public_repos_url property to return a dummy URL
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/some_org/repos"
            
            # Call public_repos(), which uses the mocked _public_repos_url and get_json
            repos = client.public_repos()
            
            # Expected list of repo names
            expected_repos = ["repo1", "repo2", "repo3"]
            
            self.assertEqual(repos, expected_repos)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/some_org/repos")
#!/usr/bin/env python3

import unittest
from unittest.mock import patch
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
        """Test GithubOrgClient.org returns the correct value."""
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

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url returns correct repos_url from org property."""
        with patch.object(GithubOrgClient, 'org', new_callable=unittest.mock.PropertyMock) as mock_org:
            # Setup the mock to return a dict with repos_url
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}

            client = GithubOrgClient("google")
            result = client._public_repos_url
            expected = "https://api.github.com/orgs/google/repos"

            self.assertEqual(result, expected)
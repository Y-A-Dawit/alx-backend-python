#!/usr/bin/env python3

"""
Test suite for the GithubOrgClient class methods.
"""


import unittest
from unittest import TestCase
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient  # adjust import if needed
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class."""

    org_payload = {
        "login": "google",
        "id": 1,
        "repos_url": "https://api.github.com/orgs/google/repos"
    }

    repos_payload = [
        {
            "id": 1,
            "name": "repo1",
            "license": {"key": "apache-2.0"}
        },
        {
            "id": 2,
            "name": "repo2",
            "license": {"key": "mit"}
        }
    ]

    expected_repos = ["repo1", "repo2"]
    apache2_repos = ["repo1"]

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
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")
        # Assert the org property returns the mock data
        self.assertEqual(result, expected)

    @patch('client.get_json')
    def test_public_repos_url(self, mock_get_json):
        """
        Test GithubOrgClient._public_repos_url returns
        correct repos_url from org property.
        """
        with patch.object(
                GithubOrgClient, 'org', new_callable=PropertyMock
                ) as mock_org:
            # Setup the mock to return a dict with repos_url
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"}

            client = GithubOrgClient("google")
            result = client._public_repos_url
            expected = "https://api.github.com/orgs/google/repos"

            self.assertEqual(result, expected)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test GithubOrgClient.public_repos returns list of repo names.
        """
        # Mock the return value of get_json to a list of repo dicts
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]

        client = GithubOrgClient("some_org")

        # Patch the _public_repos_url property to return a dummy URL
        with patch.object(
                GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
                ) as mock_url:
            mock_url.return_value = (
                "https://api.github.com/orgs/some_org/repos"
            )
            # Call public_repos(), which uses the mocked
            # _public_repos_url and get_json
            repos = client.public_repos()
            # Expected list of repo names
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_repos)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/some_org/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that GithubOrgClient.has_license returns correct boolean.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

    @parameterized_class([
        {
            "org_payload": TEST_PAYLOAD[0][0],
            "repos_payload": TEST_PAYLOAD[0][1],
            "expected_repos": TEST_PAYLOAD[0][2],
            "apache2_repos": TEST_PAYLOAD[0][3],
        }
    ])
    class TestIntegrationGithubOrgClient(unittest.TestCase):
        """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Mock requests.get and set side effects based on URL"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            mock_resp = Mock()
            if url == f"https://api.github.com/orgs/test_org":
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload.get("repos_url"):
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = None
            return mock_resp

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo names"""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by license"""
        client = GithubOrgClient("test_org")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos)

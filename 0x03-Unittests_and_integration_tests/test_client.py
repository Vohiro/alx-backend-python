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
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with
        (f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected URL"""
        expected_url = "https://api.github.com/orgs/test-org/repos"
        payload = {"repos_url": expected_url}

        with patch.object(GithubOrgClient, "org", 
                          new_callable=property(lambda self: payload)):
            client = GithubOrgClient("test-org")
            self.assertEqual(client._public_repos_url, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repos"""
        expected_repos = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = expected_repos

        with patch.object(GithubOrgClient, "_public_repos_url", 
                          new_callable=PropertyMock) as mock_url:
            mock_url.return_value="https://api.github.com/orgs/test-org/repos"
            client = GithubOrgClient("test-org")
            result = client.public_repos()

            # Verify results
            self.assertEqual(result, ["repo1", "repo2"])

            # Verify mocks were called exactly once
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with
            ("https://api.github.com/orgs/test-org/repos")


if __name__ == "__main__":
    unittest.main()

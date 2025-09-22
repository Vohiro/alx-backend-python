#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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
                          new_callable=PropertyMock) as mo_url:
            mo_url.return_value = "https://api.github.com/orgs/test-org/repos"
            client = GithubOrgClient("test-org")
            result = client.public_repos()

            # Verify results
            self.assertEqual(result, ["repo1", "repo2"])

            # Verify mocks were called exactly once
            mo_url.assert_called_once()
            mock_get_json.assert_called_once_with
            ("https://api.github.com/orgs/test-org/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean based on license"""
        client = GithubOrgClient("test-org")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get"""
        cls.get_patcher = patch("requests.get")

        mock_get = cls.get_patcher.start()

        # Configure side_effect that .json() returns depending on URL
        def side_effect(url):
            mock_response = unittest.mock.Mock()
            if url == "https://api.github.com/orgs/test-org":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload.get("repos_url"):
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the expected list"""
        client = GithubOrgClient("test-org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters by license properly"""
        client = GithubOrgClient("test-org")
        self.assertEqual(client.public_repos(license="apache-2.0"),
                         self.apache2_repos)



if __name__ == "__main__":
    unittest.main()

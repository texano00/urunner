import unittest
from unittest.mock import patch, MagicMock
from utils.model.image import Image
from utils.dockerapi import get_dockerapi_digest


class TestDockerAPIDigest(unittest.TestCase):

    @patch("utils.dockerapi.requests.get")
    @patch("utils.dockerapi.config.get_urunner_conf_docker_api_accept_header")
    @patch("utils.dockerapi.config.get_urunner_conf_docker_api_verify")
    @patch("utils.helpers.explode_image")
    @patch("utils.dockerapi.get_dockerapi_image_path")
    def test_get_dockerapi_digest_success(self, mock_get_image_path, mock_explode_image, mock_verify, mock_accept_header, mock_requests_get):
        # Mock configuration values
        mock_accept_header.return_value = "application/vnd.docker.distribution.manifest.v2+json"
        mock_verify.return_value = True

        # Mock explode_image
        mock_explode_image.return_value = ("test-image", "latest")

        # Mock get_dockerapi_image_path
        mock_get_image_path.return_value = "library/test-image"

        # Mock requests.get response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"docker-content-digest": "sha256:testdigest"}
        mock_requests_get.return_value = mock_response

        # Create a test image
        test_image = Image(
            image_id="test-id",
            namespace="test-namespace",
            resource="test-resource",
            image="test-image:latest",
            tag="latest",
            tag_digest=""
        )

        # Call the function
        digest = get_dockerapi_digest(
            image=test_image,
            authorization="Bearer test-token",
            host="https://test-registry.com",
            container_registry_type="dockerhub"
        )

        # Assertions
        self.assertEqual(digest, "sha256:testdigest")
        mock_requests_get.assert_called_once_with(
            "https://test-registry.com/v2/library/test-image/manifests/latest",
            headers={
                "Authorization": "Bearer test-token",
                "Accept": "application/vnd.docker.distribution.manifest.v2+json",
            },
            verify=True,
            timeout=60
        )

    @patch("utils.dockerapi.requests.get")
    @patch("utils.dockerapi.config.get_urunner_conf_docker_api_accept_header")
    @patch("utils.dockerapi.config.get_urunner_conf_docker_api_verify")
    @patch("utils.helpers.explode_image")
    @patch("utils.dockerapi.get_dockerapi_image_path")
    def test_get_dockerapi_digest_failure(self, mock_get_image_path, mock_explode_image, mock_verify, mock_accept_header, mock_requests_get):
        # Mock configuration values
        mock_accept_header.return_value = "application/vnd.docker.distribution.manifest.v2+json"
        mock_verify.return_value = True

        # Mock explode_image
        mock_explode_image.return_value = ("test-image", "latest")

        # Mock get_dockerapi_image_path
        mock_get_image_path.return_value = "library/test-image"

        # Mock requests.get response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        # Create a test image
        test_image = Image(
            image_id="test-id",
            namespace="test-namespace",
            resource="test-resource",
            image="test-image:latest",
            tag="latest",
            tag_digest=""
        )

        # Call the function
        digest = get_dockerapi_digest(
            image=test_image,
            authorization="Bearer test-token",
            host="https://test-registry.com",
            container_registry_type="dockerhub"
        )

        # Assertions
        self.assertIsNone(digest)
        mock_requests_get.assert_called_once_with(
            "https://test-registry.com/v2/library/test-image/manifests/latest",
            headers={
                "Authorization": "Bearer test-token",
                "Accept": "application/vnd.docker.distribution.manifest.v2+json",
            },
            verify=True,
            timeout=60
        )


if __name__ == "__main__":
    unittest.main()

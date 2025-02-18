import unittest
from utils.model.image import Image
from utils.general import explode_image


class TestGeneral(unittest.TestCase):

    def test_explode_image_with_tag(self):
        image = Image(
            image_id="",
            namespace="",
            resource="",
            image="registry.harbor/image:latest-latest",
            tag="",
            tag_digest=""
        )
        image_name, tag = explode_image(image)
        self.assertEqual(image_name, "registry.harbor/image")
        self.assertEqual(tag, "latest-latest")

    def test_explode_image_without_tag(self):
        image = Image(
            image_id="",
            namespace="",
            resource="",
            image="registry.harbor/image",
            tag="",
            tag_digest=""
        )
        image_name, tag = explode_image(image)
        self.assertEqual(image_name, "registry.harbor/image")
        self.assertEqual(tag, "latest")

    def test_explode_image_with_default_registry(self):
        image = Image(
            image_id="",
            namespace="",
            resource="",
            image="nginx:latest",
            tag="",
            tag_digest=""
        )
        image_name, tag = explode_image(image)
        self.assertEqual(image_name, "nginx")
        self.assertEqual(tag, "latest")

    def test_explode_image_without_tag_default_registry(self):
        image = Image(
            image_id="",
            namespace="",
            resource="",
            image="nginx",
            tag="",
            tag_digest=""
        )
        image_name, tag = explode_image(image)
        self.assertEqual(image_name, "nginx")
        self.assertEqual(tag, "latest")

    def test_explode_image_with_complex_tag(self):
        image = Image(
            image_id="",
            namespace="",
            resource="",
            image="registry.harbor/mapineq/mapineqfrontend:latest-latest",
            tag="",
            tag_digest=""
        )
        image_name, tag = explode_image(image)
        self.assertEqual(image_name, "registry.harbor/mapineq/mapineqfrontend")
        self.assertEqual(tag, "latest-latest")

    def test_explode_image_with_port(self):
        image = Image(
            image_id="",
            namespace="",
            resource="",
            image="harbor:8080/image:latest",
            tag="",
            tag_digest=""
        )
        image_name, tag = explode_image(image)
        self.assertEqual(image_name, "harbor:8080/image")
        self.assertEqual(tag, "latest")

    def test_explode_image_with_registry_and_tag(self):
        image = Image(
            image_id="",
            namespace="",
            resource="",
            image="435734619587.dkr.ecr.us-east-2.amazonaws.com/urunner-test/nginx:latest",
            tag="",
            tag_digest=""
        )
        image_name, tag = explode_image(image)
        self.assertEqual(image_name, "435734619587.dkr.ecr.us-east-2.amazonaws.com/urunner-test/nginx")
        self.assertEqual(tag, "latest")

    def test_explode_image_with_registry_without_tag(self):
        image = Image(
            image_id="",
            namespace="",
            resource="",
            image="435734619587.dkr.ecr.us-east-2.amazonaws.com/urunner-test/nginx",
            tag="",
            tag_digest=""
        )
        image_name, tag = explode_image(image)
        self.assertEqual(image_name, "435734619587.dkr.ecr.us-east-2.amazonaws.com/urunner-test/nginx")
        self.assertEqual(tag, "latest")

    def test_explode_one_image_layer_with_registry_and_tag(self):
        image = Image(
            image_id="",
            namespace="",
            resource="",
            image="435734619587.dkr.ecr.us-east-2.amazonaws.com/nginx:latest",
            tag="",
            tag_digest=""
        )
        image_name, tag = explode_image(image)
        self.assertEqual(image_name, "435734619587.dkr.ecr.us-east-2.amazonaws.com/nginx")
        self.assertEqual(tag, "latest")

if __name__ == '__main__':
    unittest.main()
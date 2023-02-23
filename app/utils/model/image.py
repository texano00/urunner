"""Image model"""
from dataclasses import dataclass


@dataclass
class Image:
    """Image model"""

    image_id: str
    namespace: str
    resource: str
    image: str
    tag: str
    tag_digest: str

    # def get_image_id(self):
    #     """image_id"""
    #     return self.image_id

    # def get_namespace(self):
    #     """namespace"""
    #     return self.namespace

    # def get_resource(self):
    #     """get_resource"""
    #     return self.resource

    # def get_image(self):
    #     """get_image"""
    #     return self.image

    # def get_tag(self):
    #     """get_tag"""
    #     return self.tag

    # def get_tag_digest(self):
    #     """get_tag_digest"""
    #     return self.tag_digest

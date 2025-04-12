import re
from utils.model.image import Image
import utils.config as config


def explode_image(image: Image):
    """explode_image"""
    # Example image formats:
    # harbor:8080/image:latest
    # harbor:8080/image
    # nginx:latest
    # nginx
    # 435734619587.dkr.ecr.us-east-2.amazonaws.com/urunner-test/nginx:latest
    image_name = image.image
    registry_to_watch = config.get_urunner_conf_container_registry_to_watch()
    image_name = image_name.replace(registry_to_watch, "")
    if image_name.startswith("/"):
        image_name = image_name[1:]

    # Regular expression to match image name and tag
    match = re.match(r'^(.*?)(?::([^:/]+))?$', image_name)
    if match:
        image_name = match.group(1)
        tag = match.group(2) if match.group(2) else "latest"
        return (image_name, tag)

    return (image_name, "latest")
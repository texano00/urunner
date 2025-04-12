""""General module"""
import datetime
import logging
from utils.dockerapi import (
    get_dockerapi_digest,
    get_dockerhub_auth,
    get_harbor_auth,
    get_aws_auth,
    get_digitalocean_auth,
    get_gitlab_auth,
    get_dockerhub_host,
    get_configured_host,
    get_digitalocean_host,
)
from utils.model.image import Image
from utils.kubernetes import Kubernetes
import utils.config as config
import utils.persistence as persistence


def get_date_time():
    """get_date_time"""
    now = datetime.datetime.utcnow()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_container_registry(image):
    """get_container_registry"""
    registry_host = config.get_urunner_conf_container_registry_to_watch()
    if registry_host in image:
        return config.get_urunner_conf_container_registry_type()

    return None


def process_resource(db_ref: persistence.Persistence, kubernetes: Kubernetes, image: Image):
    """process_resource"""
    docker_api_auth_mapper = {
        "dockerhub": get_dockerhub_auth,
        "harbor": get_harbor_auth,
        "aws_ecr": get_aws_auth,
        "digitalocean": get_digitalocean_auth,
        "gitlab" : get_gitlab_auth
    }

    docker_api_host_mapper = {
        "dockerhub": get_dockerhub_host,
        "harbor": get_configured_host,
        "aws_ecr": get_configured_host,
        "digitalocean": get_digitalocean_host,
        "gitlab": get_configured_host
    }
    container_registry_type = get_container_registry(image.image)
    if container_registry_type is None:
        logging.debug("Container registry not recognized")
        return

    auth = docker_api_auth_mapper[container_registry_type](image)
    docker_api_host = docker_api_host_mapper[container_registry_type]()
    tag_digest = get_dockerapi_digest(image, auth, docker_api_host, container_registry_type)
    if tag_digest is None:
        return

    result = db_ref.get_image_by_id(image.image_id)
    image.tag_digest = tag_digest
    logging.debug(image)

    if result is None:
        logging.debug("DB miss")
        db_ref.add_new_image(data=image)
    else:
        logging.debug("DB hit")
        if result["tag_digest"] != image.tag_digest:
            db_ref.update_image_digest(image_id=image.image_id, new_tag_digest=image.tag_digest)
            kubernetes.restart_deployment(image.namespace, image.resource)

        db_ref.update_image_last_check_data(image_id=image.image_id)

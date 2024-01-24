"""dockerapi module"""
from base64 import b64encode
import logging
import hashlib
import requests
import boto3
import utils.general as general
import utils.config as config
from utils.model.image import Image


def get_dockerapi_image_path(image_name):
    """get_dockerapi_image_path"""
    if "/" in image_name:
        return image_name

    return "library/" + image_name


def get_harbor_auth(image: Image):
    """get_harbor_auth"""
    logging.debug(image)
    username = config.get_urunner_secr_harbor_user()
    password = config.get_urunner_secr_harbor_pass()
    auth = f"{username}:{password}".encode("ascii")
    return f"Basic {auth}"


def get_aws_auth(image: Image):
    """get_aws_auth"""
    logging.debug(image)
    # ex. 435734619587.dkr.ecr.us-east-2.amazonaws.com
    region_name = config.get_urunner_conf_container_registry_to_watch().split(".")[3]
    registry_id = config.get_urunner_conf_container_registry_to_watch().split(".")[0]
    boto3.Session(
        aws_access_key_id=config.get_urunner_secr_aws_access_key_id,
        aws_secret_access_key=config.get_urunner_secr_aws_secret_access_key,
        region_name=region_name,
    )

    client = boto3.client("ecr", region_name=region_name)

    response = client.get_authorization_token(
        registryIds=[
            registry_id,
        ]
    )
    token = response["authorizationData"][0]["authorizationToken"]
    return f"Basic {token}"


def get_dockerhub_auth(image: Image):
    """get_dockerhub_auth"""
    auth_service = "registry.docker.io"
    auth_url = "https://auth.docker.io/token"
    return get_docker_v2_api_auth_style(image=image, auth_url=auth_url, auth_service=auth_service)


def get_digitalocean_auth(image: Image):
    """get_digitalocean_auth"""
    auth_service = "registry.digitalocean.com"
    auth_url = "https://api.digitalocean.com/v2/registry/auth"
    do_token = config.get_urunner_secr_digital_ocean_token()
    do_token = b64encode(f"{do_token}:{do_token}".encode("ascii")).decode("ascii")
    auth_header = f"Basic {do_token}"
    return get_docker_v2_api_auth_style(
        image=image, auth_url=auth_url, auth_service=auth_service, auth_header=auth_header
    )

def get_gitlab_auth(image: Image):
    """get_gitlab_auth"""
    auth_service = "gitlab.com"
    auth_url = "https://gitlab.com/jwt/auth"
    do_token = config.get_urunner_secr_gitlab_token()
    do_token = b64encode(f"{do_token}:{do_token}".encode("ascii")).decode("ascii")
    auth_header = f"Basic {do_token}"
    return get_docker_v2_api_auth_style(
        image=image, auth_url=auth_url, auth_service=auth_service, auth_header=auth_header
    )

def get_docker_v2_api_auth_style(image: Image, auth_service, auth_url, auth_header=None):
    """get_docker_v2_api_auth_style"""
    exploded_image = general.explode_image(image)
    image_name = exploded_image[0]
    dockerhub_image_path = get_dockerapi_image_path(image_name)
    auth_scope = f"repository:{dockerhub_image_path}:pull"
    headers = {"Authorization": auth_header} if auth_header else {}
    url = f"{auth_url}?service={auth_service}&scope={auth_scope}"
    response = requests.get(url, headers=headers, timeout=60)
    token = response.json()["token"]
    return f"Bearer {token}"


def get_dockerhub_host():
    """get_dockerhub_host"""
    return "https://registry-1.docker.io"


def get_digitalocean_host():
    """get_digitalocean_host"""
    return "https://registry.digitalocean.com"


def get_configured_host():
    """get_configured_host"""
    registry_host = config.get_urunner_conf_container_registry_to_watch()
    return f"https://{registry_host}"


def get_dockerapi_digest(image: Image, authorization, host):
    """get_dockerapi_digest"""
    exploded_image = general.explode_image(image)
    logging.debug(exploded_image)
    image_name = exploded_image[0]
    image_tag = exploded_image[1]

    dockerhub_image_path = get_dockerapi_image_path(image_name)
    logging.debug(dockerhub_image_path)

    headers = {"Authorization": authorization}
    url = f"{host}/v2/{dockerhub_image_path}/manifests/{image_tag}"
    try:
        response = requests.get(url, headers=headers, verify=config.get_urunner_conf_docker_api_verify(), timeout=60)
    except requests.exceptions.RequestException as exception:
        logging.error(exception)
        return None

    logging.debug(response)
    if response.status_code == 200:
        logging.debug(response.headers)
        image_digest = (
            response.headers["docker-content-digest"]
            if "docker-content-digest" in response.headers
            else hashlib.sha1(f"{response.content}".encode("utf-8")).hexdigest()
        )
        logging.debug("image_digest: %s", image_digest)
        return image_digest

    logging.error("Error status code: %i", response.status_code)
    logging.debug(response)
    return None

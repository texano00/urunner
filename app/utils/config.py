"""config module"""
import os
from ast import literal_eval


def get_urunner_conf_docker_api_verify():
    """get_urunner_conf_docker_api_verify"""
    return literal_eval(os.environ.get("URUNNER_CONF_DOCKER_API_VERIFY", "True").capitalize())


def get_urunner_conf_log_level():
    """get_urunner_conf_log_level"""
    return os.environ.get("URUNNER_CONF_LOG_LEVEL", "INFO")


def get_urunner_conf_k8s_auth_strategy():
    """get_urunner_conf_k8s_auth_strategy"""
    return os.environ.get("URUNNER_CONF_KUBE_AUTH", "incluster")


def get_urunner_conf_sqlight_path():
    """get_urunner_conf_sqlight_path"""
    return os.environ.get("URUNNER_CONF_SQLLIGHT_PATH", "./urunner.db")


def get_urunner_conf_frequency_check_seconds():
    """get_urunner_conf_frequency_check_seconds"""
    return int(os.environ.get("URUNNER_CONF_FREQUENCY_CHECK_SECONDS", "30"))


def get_urunner_conf_container_registry_to_watch():
    """get_urunner_conf_container_registry_to_watch"""
    return os.environ.get("URUNNER_CONF_CONTAINER_REGISTRY_TO_WATCH", "harbor.default.svc.cluster.local:8080")


def get_urunner_conf_container_registry_type():
    """get_urunner_conf_container_registry_type"""
    return os.environ.get("URUNNER_CONF_CONTAINER_REGISTRY_TYPE", "harbor")


def get_urunner_secr_harbor_user():
    """get_urunner_secr_harbor_user"""
    return os.environ.get("URUNNER_SECR_HARBOR_USER", "admin")


def get_urunner_secr_harbor_pass():
    """get_urunner_secr_harbor_pass"""
    return os.environ.get("URUNNER_SECR_HARBOR_PASS", "Harbor12345")

def get_urunner_secr_aws_region():
    """def get_urunner_secr_aws_region"""
    return os.environ.get("URUNNER_SECR_AWS_REGION", "us-east-2")


def get_urunner_secr_aws_access_key_id():
    """def get_urunner_secr_aws_access_key_id"""
    return os.environ.get("URUNNER_SECR_AWS_ACCESS_KEY_ID", "AKIAIOSFODNN7EXAMPLE")


def get_urunner_secr_aws_secret_access_key():
    """def get_urunner_secr_aws_secret_access_key"""
    return os.environ.get("URUNNER_SECR_AWS_SECRET_ACCESS_KEY", "wJalrXUtnFEMI/K7MDENG/xRfiCYEXAMPLEKEY")


def get_urunner_secr_digital_ocean_token():
    """def get_urunner_secr_digital_ocean_token"""
    return os.environ.get("URUNNER_SECR_DIGITAL_OCEAN_TOKEN", "xxxxx")

def get_urunner_secr_gitlab_token():
    """def get_urunner_secr_gitlab_token"""
    return os.environ.get("URUNNER_SECR_GITLAB_TOKEN", "xxxxx")

def get_urunner_secr_gitlab_url():
    """def get_urunner_secr_gitlab_url"""
    return os.environ.get("URUNNER_SECR_GITLAB_URL", "https://gitlab.com")

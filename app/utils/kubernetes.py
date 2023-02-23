"""Kubernetes module"""
import datetime
import logging
from kubernetes.client.rest import ApiException
from kubernetes import client, config
import utils.config as urunnerConfig


class Kubernetes:
    """Kubernetes class"""

    def __init__(self):
        auth_strategy_mapper = {"incluster": config.load_incluster_config, "kubeconfig": config.load_kube_config}
        auth_strategy_mapper[urunnerConfig.get_urunner_conf_k8s_auth_strategy()]()
        self.v1_apps = client.AppsV1Api()
        self.v1_core = client.CoreV1Api()

    def get_namespaces(self):
        """get_namespaces"""
        namespace = self.v1_core.list_namespace()
        return namespace

    def get_deployments(self, namespace):
        """get_deployments"""
        deployments = self.v1_apps.list_namespaced_deployment(namespace=namespace)
        return deployments

    def restart_deployment(self, namespace, deployment):
        """restart_deployment"""
        logging.info("Restarting %s in ns %s", deployment, namespace)
        now = datetime.datetime.utcnow()
        now = str(now.isoformat("T") + "Z")
        body = {"spec": {"template": {"metadata": {"annotations": {"kubectl.kubernetes.io/restartedAt": now}}}}}
        try:
            self.v1_apps.patch_namespaced_deployment(deployment, namespace, body, pretty="true")
        except ApiException as exception:
            logging.error("Exception when calling AppsV1Api->read_namespaced_deployment_status: %s\n", exception)

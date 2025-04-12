"""Entrypoint module."""
import logging
import time
import schedule
from app.utils.helpers import explode_image
import utils.persistence as persistence
import utils.kubernetes as k8s
import utils.config as config
import utils.general as general
from utils.model.image import Image


def job():
    """Recurrent urunner Job"""
    logging.debug("%s start scheduler", general.get_date_time())
    all_namespaces = kubernetes.get_namespaces()
    for namespace in all_namespaces.items:
        namespace = namespace.metadata.name

        logging.debug("Listing deployments in namespace %s", namespace)
        deployments = kubernetes.get_deployments(namespace=namespace)
        for deployment in deployments.items:
            logging.debug("Name: %s", deployment.metadata.name)
            for container in deployment.spec.template.spec.containers:
                image = Image(
                    image_id="",
                    namespace=namespace,
                    resource=deployment.metadata.name,
                    tag="",
                    tag_digest="",
                    image=container.image,
                )

                image_tag = explode_image(image)[1]
                image.tag = image_tag
                image_id = f"{namespace}-{deployment.metadata.name}-{container.image}-{image_tag}"
                image.image_id = image_id
                logging.debug("Image: %s", image)

                general.process_resource(db_ref=db_ref, kubernetes=kubernetes, image=image)


logging.basicConfig(encoding="utf-8", level=config.get_urunner_conf_log_level())

db_ref = persistence.Persistence(path=config.get_urunner_conf_sqlight_path())
db_ref.init()

kubernetes = k8s.Kubernetes()
schedule.every(config.get_urunner_conf_frequency_check_seconds()).seconds.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)

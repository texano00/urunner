# urunner

<img width=200 src=asset/logo.png>

URunner is a Kubernetes utiity in order to **auto restart** pods on image **tag digest change**.\
This is very useful on environments where it is commonly used the `latest` tag which frequently changes over time.\
Urunner auto detects the container image tag digest (for example the digest of tag `latest`) and automatically restart pods.\
Urunner integrates external container registry (ex. [Harbor](https://goharbor.io/)) using standard [Docker API V2](https://docs.docker.com/registry/spec/api/).

Urunner is also **fully configurable** in order to **watch only specific namespaces** and **specific tags** (ex. latest, dev) based on **regex**.

## Helm

[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/urunner)](https://artifacthub.io/packages/search?repo=urunner)

[Artifact Hub Link](https://artifacthub.io/packages/helm/urunner/urunner)

```
helm upgrade --install urunner oci://ghcr.io/texano00/urunner/helm/urunner --version 0.1.0 --values my-values.yaml -n urunner --create-namespace
```

## Env vars

| Var                                      | Description                                               | Example                              |
| ---------------------------------------- | --------------------------------------------------------- | ------------------------------------ |
| URUNNER_CONF_DOCKER_API_VERIFY           | SSL verify to docker registry                             | True or False                        |
| URUNNER_CONF_LOG_LEVEL                   | Log Level                                                 | DEBUG,INFO,WARNING                   |
| URUNNER_CONF_KUBE_AUTH                   | Kubernetes client authentication strategy                 | incluster or kubeconfig              |
| URUNNER_CONF_SQLLIGHT_PATH               | Path of sqlight DB                                        | ./urunner.db                         |
| URUNNER_CONF_FREQUENCY_CHECK_SECONDS     | Frequency of urunner cron job (seconds)                   | 30                                   |
| URUNNER_CONF_NAMESPACES_TO_WATCH         | Which images/tags foreach namespaces urunner has to watch | default:.?latest,namespace2:latest-. |
| URUNNER_CONF_CONTAINER_REGISTRY_TO_WATCH | Which is the container registry to watch                  | registry.mycompanyhost.net:8080      |
| URUNNER_CONF_CONTAINER_REGISTRY_TYPE     | Kind of container registry                                | harbor or dockerhub                  |
| URUNNER_SECR_HARBOR_USER                 | Harbor username                                           | user                                 |
| URUNNER_SECR_HARBOR_PASS                 | Harbor password                                           | pass                                 |

## Flow

<img src=asset/urunner.png>

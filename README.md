# urunner

## Intro

<img width=200 src=asset/logo.png>

URunner is a Kubernetes utiity in order to **auto restart** pods on image **tag digest change**.\
This is very useful on environments where it is commonly used the `latest` tag which frequently changes over time.\
Urunner auto detects the container image tag digest (for example the digest of tag `latest`) and automatically restart pods.

## Docker API V2

Urunner integrates external container registry (ex. [Harbor](https://goharbor.io/)) using standard [Docker API V2](https://docs.docker.com/registry/spec/api/).\
Actually **Harbor** is the only container registry officially supported.\
**AWS ECR and Azure ACR** support will be released soon.

## Configurable watcher

Urunner is also **fully configurable** in order to **watch only specific namespaces** and **specific tags** (ex. latest, dev) based on **regex**.

## Status

Actually Urunner is released with a `0.x.x` version, a stable version will be released as soon as possible thanks also to the **open source community**.

## Helm

[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/urunner)](https://artifacthub.io/packages/search?repo=urunner)

[Artifact Hub Link](https://artifacthub.io/packages/helm/urunner/urunner)

```
helm upgrade --install urunner oci://ghcr.io/texano00/urunner/helm/urunner --version 0.1.0 --values my-values.yaml -n urunner --create-namespace
```

## Urunner env vars

| Var                                      | Description                                               | Example                                |
| ---------------------------------------- | --------------------------------------------------------- | -------------------------------------- |
| URUNNER_CONF_DOCKER_API_VERIFY           | SSL verify to docker registry                             | True or False                          |
| URUNNER_CONF_LOG_LEVEL                   | Log Level                                                 | DEBUG,INFO,WARNING                     |
| URUNNER_CONF_KUBE_AUTH                   | Kubernetes client authentication strategy                 | incluster or kubeconfig                |
| URUNNER_CONF_SQLLIGHT_PATH               | Path of sqlight DB                                        | ./urunner.db                           |
| URUNNER_CONF_FREQUENCY_CHECK_SECONDS     | Frequency of urunner cron job (seconds)                   | 30                                     |
| URUNNER_CONF_NAMESPACES_TO_WATCH         | Which images/tags foreach namespaces urunner has to watch | default:.?latest,namespace2:latest-.   |
| URUNNER_CONF_CONTAINER_REGISTRY_TO_WATCH | Which is the container registry to watch                  | registry.mycompanyhost.net:8080        |
| URUNNER_CONF_CONTAINER_REGISTRY_TYPE     | Kind of container registry                                | harbor,aws_ecr,dockerhub               |
| URUNNER_SECR_HARBOR_USER                 | Harbor username                                           | user                                   |
| URUNNER_SECR_HARBOR_PASS                 | Harbor password                                           | pass                                   |
| URUNNER_SECR_AWS_ACCESS_KEY_ID           | AWS credential in order to pull from AWS private ECR      | AKIAIOSFODNN7EXAMPLE                   |
| URUNNER_SECR_AWS_SECRET_ACCESS_KEY       | AWS credential in order to pull from AWS private ECR      | wJalrXUtnFEMI/K7MDENG/xRfiCYEXAMPLEKEY |

## Flow

<img src=asset/urunner.png>

## ToDo

- Test AWS ECR integration
- Test Azure ACR integration

## Notes

Logo was generated using Fotor AI tool https://www.fotor.com/features/ai-image-generator/

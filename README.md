# urunner
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/urunner)](https://artifacthub.io/packages/search?repo=urunner)
![CI_CD_Helm](https://github.com/texano00/urunner/actions/workflows/CI_CD_Helm.yml/badge.svg)
![CI_CD_App](https://github.com/texano00/urunner/actions/workflows/CI_CD_App.yml/badge.svg)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=texano00/urunner&type=Date)](https://star-history.com/#texano00/urunner&Date)

## Intro

<img width=200 src=asset/logo.png>

URunner is a lightweight **Kubernetes** utility in order to **auto restart** pods on image **tag digest change**.\
This is very useful on environments where it is commonly used the `latest` tag which frequently changes over time.\
Urunner auto detects the container image tag digest (for example the digest of tag `latest`) and automatically restart pods.

## Docker API V2

Urunner integrates external container registry (ex. [Harbor](https://goharbor.io/)) using standard [Docker API V2](https://docs.docker.com/registry/spec/api/).\
Actually **Harbor**, **AWS ECR**, **Digital Ocean** and **GitLab** are the container registries officially supported.\
**Azure ACR** and **Dockerhub** support will be released soon.

URunner use cases with specific how-to:

- [AWS use case](https://www.yuribacciarini.com/automatically-pull-images-on-aws-ecr-latest-tag-change-from-aws-eks/)
- [DigitalOcean container registry DOCR use case](https://www.yuribacciarini.com/automatically-pull-new-digitalocean-container-registry-docr-latest-tags-from-kubernetes/)
- [GitLab container registry use case](https://www.yuribacciarini.com/k8s-automatically-pull-images-from-gitlab-container-registry-without-change-the-tag/)
## Configurable watcher

Urunner is also **fully configurable** in order to **watch only specific namespaces** with specific label to manage exception.\
Add label `urunner=enable` to all namespaces in order to be watched by Urunner.\
`kubectl label ns mynamespace urunner=enable`

```
apiVersion: v1
kind: Namespace
metadata:
  labels:
    # add this label
    urunner: enable
  name: mynamespace
```

Also, you can add exceptions inside `mynamespace`, for example\
`kubectl label deployment mydeployment urunner=disable -n mynamespace`

```
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    # add this label
    urunner: disable
...
```

Doing so, all deployments except `mydeployment` will be watched by Urunner.

## Helm

```
helm upgrade --install urunner oci://ghcr.io/texano00/urunner/helm/urunner --version 0.1.0 --values my-values.yaml -n urunner --create-namespace
```

## Urunner env vars

| Var                                      | Description                                                                                                        | Example                                                                                          |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| DOCKER_API_ACCEPT_HEADER                 | Accept header to inject on Docker API v2 registry                                                                  | application/vnd.docker.distribution.manifest.v2+json, application/vnd.oci.image.manifest.v1+json |
| URUNNER_CONF_DOCKER_API_VERIFY           | SSL verify to docker registry                                                                                      | True or False                                                                                    |
| URUNNER_CONF_LOG_LEVEL                   | Log Level                                                                                                          | DEBUG,INFO,WARNING                                                                               |
| URUNNER_CONF_KUBE_AUTH                   | Kubernetes client authentication strategy                                                                          | incluster or kubeconfig                                                                          |
| URUNNER_CONF_SQLLIGHT_PATH               | Path of sqlight DB                                                                                                 | ./urunner.db                                                                                     |
| URUNNER_CONF_FREQUENCY_CHECK_SECONDS     | Frequency of urunner cron job (seconds)                                                                            | 30                                                                                               |
| URUNNER_CONF_CONTAINER_REGISTRY_TO_WATCH | Which is the container registry to watch                                                                           | registry.mycompanyhost.net:8080                                                                  |
| URUNNER_CONF_CONTAINER_REGISTRY_TYPE     | Kind of container registry                                                                                         | harbor,aws_ecr, digitalocean, gitlab                                                             |
| URUNNER_SECR_HARBOR_USER                 | Harbor username, configure only if registry type is harbor                                                         | user                                                                                             |
| URUNNER_SECR_HARBOR_PASS                 | Harbor password, configure only if registry type is harbor                                                         | pass                                                                                             |
| URUNNER_SECR_AWS_ACCESS_KEY_ID           | AWS credential in order to pull from AWS private ECR, configure only if registry type is aws_ecr                   | AKIAIOSFODNN7EXAMPLE                                                                             |
| URUNNER_SECR_AWS_REGION                  | AWS region                                                                                                         | us-east-2                                                                                        |
| URUNNER_SECR_AWS_SECRET_ACCESS_KEY       | AWS credential in order to pull from AWS private ECR, configure only if registry type is aws_ecr                   | wJalrXUtnFEMI/K7MDENG/xRfiCYEXAMPLEKEY                                                           |
| URUNNER_SECR_DIGITAL_OCEAN_TOKEN         | Digital Ocean token                                                                                                | xxxxx                                                                                            |
| URUNNER_SECR_GITLAB_TOKEN                | Gitlab token                                                                                                       | xxxxx                                                                                            |
| URUNNER_SECR_GITLAB_AUTH_URL             | Gitlab URL where `/jwt/auth` API is exposed. This is usually the same URL where GitLab instance itself is exposed. | my-gitlab.com                                                                                    |

## Flow

### Generic

<img src=asset/urunner.png>

### AWS

<img src=asset/urunner-aws.png>

### DigitalOCean
<img src=asset/urunner-do.png>

### GitLab
<img src=asset/urunner-gitlab.png>


## ToDo

- Test Azure ACR integration
- manage sqlite persistence in Helm chart

## Notes

Logo was generated using Fotor AI tool https://www.fotor.com/features/ai-image-generator/

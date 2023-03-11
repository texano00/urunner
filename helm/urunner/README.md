# Urunner Helm chart

URunner is a lightweight **Kubernetes** utility in order to **auto restart** pods on image **tag digest change**.\
This is very useful on environments where it is commonly used the `latest` tag which frequently changes over time.\
Urunner auto detects the container image tag digest (for example the digest of tag `latest`) and automatically restart pods.

## TL;DR

```console
helm upgrade --install urunner oci://ghcr.io/texano00/urunner/helm/urunner --version 0.1.0 --values my-values.yaml -n urunner --create-namespace
```

## Docker API V2

Urunner integrates external container registry (ex. [Harbor](https://goharbor.io/)) using standard [Docker API V2](https://docs.docker.com/registry/spec/api/).\
Actually **Harbor** and **AWS ECR** are the container registries officially supported.\
**Azure ACR** and **Dockerhub** support will be released soon.

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

# Urunner Helm chart

URunner is a Kubernetes utiity in order to auto restart pods on image tag digest change.\
This is very useful on environments where it is commonly used the `latest` tag which frequently changes over time.\
Urunner auto detects the container image tag digest (for example the digest of tag `latest`) and automatically restart pods.

## TL;DR

```console
helm upgrade --install urunner oci://ghcr.io/texano00/urunner/helm/urunner --version 0.1.0 --values my-values.yaml -n urunner --create-namespace
```
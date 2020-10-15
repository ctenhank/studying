# Kubernetes Overview

![Kubernetes](img/kubernetes.png)

- 쿠버네티스는 컨테이너화된 어플레케이션을 실행하는 워커 노드들로 구성되어 있는 클러스터
- 모든 클러스터는 적어도 하나 이상의 워커 노드를 가짐
- 워커 노드는 어플리케이션 워크 로드의 구성요소인 Pod들을 호스팅함

## Cluster Architecture

<img src="img/components-of-kubernetes.svg" alt="Control Plane" style="zoom:150%;" />

### Control Plane Components

- Control plane is role as brain of cluster
  - Container scheduling
  - Service management
  - Processing API request
- `components of control plane` is executed in master node
  - kube-apiserver
  - etcd
  - scheduler
  - controller-manager
  - cloud-controller-manager

### Node Components

- kubelet
- kube-proxy
- Container Runtime

### Addons

- DNS
- Web UI(Dashboard)
- Container Resource Monitoring
- Cluster-level Logging

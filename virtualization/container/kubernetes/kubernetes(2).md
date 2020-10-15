# Kubernetes 시작하기

### Features compared to [Docker Swarm](../docker/swarm.md)

- 모든 리소스는 오브젝트 형태로 관리

  - Docker Swarm에서는 컨테이너 묶음을 표현하기 위해 `Service`를 사용했는데, 이는 오브젝트라 볼 수 있음

  - 쿠버네티스는 이러한 개념을 더욱 폭넓고 세밀한 단위로 사용

    - `Pod`: 컨테이너의 집합
    - `Replica Set`: Pods을 관리하는 컨트롤러
    - `Service Account`: 사용자
    - `Node`

  - `kubectl api-resources` 명령어를 통해 모든 종류의 오브젝트를 확인할 수 있음

  - `kubectl explain OBJECT` 명령어로 오브젝트에 대한 자세한 설명을 볼 수 있음

    ```bash
    $ kubelctl explain pod
    KIND:     Pod
    VERSION:  v1
    
    DESCRIPTION:
         Pod is a collection of containers that can run on a host. This resource is
         created by clients and scheduled onto hosts.
    ...
    ```

- 쿠버네티스 명령어로도 사용할 수 있지만, 대부분 YAML 파일로 사용

  - Docker Swarm에서는 `stack`을 생성하기 위해 YAML 파일을 사용한 것과 같이 쿠버네티스도 가능
  - 쿠버네티스에서는 컨테이너 리소스 뿐만 아니라 거의 모든 리소스 오브젝트들에 사용 가능

- 쿠버네티스는 여러 개의 컴포넌트로 구성됨

  - 쿠버네티스 노드의 역할은 크게 `master`, `worker` 노드로 나뉨

  - `master node`는 클러스터를 관리하는 역할을 담당

  - `worker node`는 어플리케이션 컨테이너가 생성됨

  - 쿠버네티스는 도커를 포함한 매우 많은 컴포넌트를 실행하며 마스터 노드에서 도커 컨테이너들로 실행

    - 마스터 노드에서는 `kube-apiserver`, `kube-controller-manager`, `kube-scheduler`, `coreDNS`
    - 모든 노드에서는 `kube-proxy`, network plugin들이 실행됨

    ```bash
    # docker에서 쿠버네티스를 위해 매우 많은 컨테이너들이 실행됨을 알 수 있음
    $ docker ps --format "table {{.Names}}"
    NAMES
    k8s_kube-proxy_kube-proxy-m5j58_kube-system_756a01ae-ab9e-4d3f-8657-498ff3c369f4_0
    k8s_POD_kube-proxy-m5j58_kube-system_756a01ae-ab9e-4d3f-8657-498ff3c369f4_0
    k8s_kube-apiserver_kube-apiserver-dohan_kube-system_9a4e896260cafac245130e8d19f19d25_0
    k8s_etcd_etcd-dohan_kube-system_c3be258830189573a2035817242bc723_0
    k8s_kube-scheduler_kube-scheduler-dohan_kube-system_f543c94683059cb32a4441e29fbdb238_0
    k8s_kube-controller-manager_kube-controller-manager-dohan_kube-system_aa9d084ad37e56894bc5ec833cf20941_0
    k8s_POD_kube-scheduler-dohan_kube-system_f543c94683059cb32a4441e29fbdb238_0
    k8s_POD_kube-controller-manager-dohan_kube-system_aa9d084ad37e56894bc5ec833cf20941_0
    k8s_POD_kube-apiserver-dohan_kube-system_9a4e896260cafac245130e8d19f19d25_0
    k8s_POD_etcd-dohan_kube-system_c3be258830189573a2035817242bc723_0
    ```

  - 쿠버네티스는 클러스터링 구성을 위해 `kubelet`이라는 에이전트가 모든 노드에서는 실행됨

    - 컨테이너 생성·삭제, 마스터와 워커 노드 간의 통신 등 매우 중요한 에이전트
    - 정상적으로 실행되지 않으면, 해당 노드는 쿠버테니스에 제대로 연결되지 않을 수 있음

  - 도커는 필수적인 구성요소는 아님
    OCI(Open Container Initiative) 라는 컨테이너 런타임 표준을 구현한 CRI(Container Runtime Interface)를 갖춘 컨테이너면 이용 가능

## Core Objects

- 컨테이너 어플리케이션을 구동하기 위해 반드시 알아야 하는 몇 가지 오브젝트가 존재:
  `Pod`, `Replica set`, `Service`, `Deployment`

### Pod(포드)

- Docker Engine에서는 기본 단위가 컨테이너, Docker Swarm에서는 기본 단위는 서비스
- 쿠버네티스에서 기본 단위는 Pod인데, 이는 한 개 이상의 컨테이너로 구성된 컨테이너 집합를 의미
- [쿠버네티스에서의 yaml grammar는 여기서 참고](kube_yaml.md)
- yaml 파일은 `kubectl apply -f` 명령어를 통해 쿠버네티스에 생성할 수 있음




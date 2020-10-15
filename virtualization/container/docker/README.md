# Docker Overview

![Docker](img/docker.png)

<div style="text-align:right"><a herf="https://www.docker.com/">https://www.docker.com/</a></div>

### Features

- 도커는 어플리케이션을 개발(Developing), 출시(Shipping), 운용(Running)하기 위한 오픈소스 플랫폼
- 도커는 **컨테이너** 환경을 통해 많은 어플리케이션들을 패키지화(격리)하여 인프라에서 운영할 수 있게 함
- 즉, 도커는 컨테이너 생명주기(lifecycle)을 관리하기 위한 도구들과 플랫폼을 제공해줌

### Architecture
<img src="img/docker-architecture.png" alt="Docker Architecture" style="zoom: 80%;" />

<div style="text-align:right" ><a herf="https://docs.docker.com/get-started/overview/">https://docs.docker.com/get-started/overview/</a></div>

- 도커는 **Client-Server Architecture**를 가지는 어플리케이션
- **Client**는 서버에게 어떤 기능을 수행시키기 위해 CLI(Command Line Interface) 제공, `docker` 명령어로 수행
- **Server**는 클라이언트에게 CLI를 입력 받아서 실질적으로 도커 엔진의 기능을 수행, `dockerd` 명령어로 수행
- **Server**는 `docker daemon`이라고 불리며, 설치 시 자동으로 서비스로 등록되어 호스트 재시작 시 자동으로 실행됨
- `docker daemon`이 로컬에 있다면 클라이언트는 `/var/run/docker.sock`에 위치한 유닉스 소켓을 통해 도커 데몬 API를 호출
                                   원격에 있다면 `tcp`를 통해 통신하는데, docker daemon의 `defualt port`는  **2375**
- `REST API`를 이용하여 프로그램을 통해 `docker daemon`과 통신할 수 있음[[1]](https://docs.docker.com/engine/api/)

```sequence
Developer->Client: CLI: docker COMMAND
Client->Server: execute the APIs
Note right of Server: Server execute the libraries
Server-->Client: return
Client-->Developer: print
RemoteNode->Server:curl 192.168.99.100:2375
Server-->RemoteNode:return & print
```

### Components

도커는 많은 컴포넌트들로 구성되어 있는데, 아래와 같다. 또한, 더 자세한 사항들은 링크를 통해 알아보자.

- [**Docker Daemon**](daemon.md)
  - 클라이언트에게서 API Request를 `listen`하며, 실질적으로 이미지, 컨테이너, 네트워크, 볼륨과 같은 오브젝트들을 관리
  - 다른 `docker daemon`들과 `service`를 관리하기 위해 통신하기도 함
  
- [**Docker Client**](client.md)
  - `docker daemon`, 즉 `server`에게 어떤 기능을 수행시키기 위해 API Request을 함
  - API Request는 `CLI` 또는 `RESTful API`를 이용해서 할 수 있음
  - 하나 이상의 `docker daemon`들과 통신할 수 있ᅌᅳᆷ
  
- [**Docker Registry**](registry.md)
  - `Docker Inc.`에서 사용자에게 `docker image`를 저장하는데 제공하는 Hub
  - `docker pull`, `docker push`를 통해서 `docker registry`와 이미지를 주고 받을 수 있음
  
- **Docker objects**
  
  - 도커 엔진에서 사용하는 **기본 단위는 image와 container**이며, 이는 **도커 엔진의 핵심**
  
  - [**Image**](image_container.md)
    - 도커 컨테이너를 생성하기 위한 `read-only` 템플릿
    - 어떤 이미지를 기반으로 컨테이너를 생성하고, 그 컨테이너를 변경하면 그 변동사항을 바탕으로 `build`하여 새로운 이미지를 생성
    - 또한 [`Dockerfile`](dockerfile.md)을 통해 이미지를 `build`할 수 있음
  - [**Container**](image_container.md)
    - Docker API나 CLI를 통해 이미지를 통해 생성한 실행가능한 인스턴스
    - 컨테이너는 하나 이상의 네트워크, 스토리지에 연결할 수 있음
    - 컨테이너 상태를 기반으로 새로운 이미지를 만들 수 있음
    - 새로운 이미지로 만들지 않으면 컨테이너 상태는 스토리지에 저장되지 않음
  - [**Volume**](volume.md)
  - [**Network**](network.md)
  - [**Plugins**](plugins.md)
  - [**Service**](swarm.md)
    - 서비스는 컨테이너를 단일 호스트에서만 아니라 다수의 호스트들에서 분산시켜 실행할 수 있도록 해줌
    - 서비스는 Docker Swarm과 함께 작동하는데, 다양한 설정과 로드 밸런싱 등을 할 수 있음

### The Underlying Technology

#### [Namespaces](namespaces.md)

- 네임스페이스를 이용하여 컨테이너를 격리시켜줌
- 리눅스 커널에 구현되어 있는 `Linux kernel namespace` 이용

#### [Control groups](cgroups.md)

- 컨테이너에 특정 리소스들을 제한·할당시켜줌
- 리눅스 커널에 구현되어 있는 `cgroups` 이용

#### [Union file systems](ufs.md)

- 레이어를 생성하여 동작하는 파일 시스템

#### Container format

- 도커 엔진은 `namespaces`, `control groups`, `UnionFW` 등을 하나로 묶어 컨테이너 포맷으로 만듬
- 도커의 기본 컨테이너 포맷은 `libcontainer`이며, 차후에 `BSD jail`, `Solaris Zone`등도 지원할 예정



## Reference

[1]: https://docs.docker.com/engine/api/ "Develop with Docker Engine API"
[2]: https://blog.naver.com/alice_k106/221738032450 "시작하세요! 도커/쿠버네티스, p 154-155"


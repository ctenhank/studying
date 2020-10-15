# Docker Image & Container

- 이미지는 컨테이너를 생성할 때 필요한 요소

- 여러 개의 레이어로 된 바이너리 파일로 존재

- 컨테이너를 생성하고 실행할 때 읽기 전용으로 사용됨

- 도커에서 사용하는 이미지 이름은 기본적으로 `[저장소 이름]/[이미지 이름]:[태그]` 형태로 구성

  - 저장소 이름(Repository)

    - 이미지가 저장된 장소를 의미
    - 명시되지 않으면, 기본적으로 **docker hub**의 공식 이미지(`docker.io`)
    - 그 외에 구글 클라우드 컨테이너 레지스트리(`gcr.io`) 등이 있음

  - 이미지 이름(Image)

    - 이미지가 어떤 역할을 하는지 나타냄

      > ubuntu, nginx, ...

  - 태그(Tag)

    - 이미지 버전 관리 또는 리비전 관리 의미
    - 태그 생략 시 도커 엔진은 이미지 태그를 latest로 인식

# Docker container

- 도커 이미지는 `ubuntu`, `CentOS`, `Apache Web server`, `mysql`, ... 등 갖가지 종류의 어플리케이션들이 있음
- 이미지로 컨테이너를 생성하면 해당 이미지 목적에 맞는 파일이 들어 있는 파일시스템과 격리된 자원 및 네트워크를 사용할 수 있는 독립된 공간이 생성됨
- 이미지를 읽기 전용으로 사용하고 변경 사항은 컨테이너 계층에 저장하므로 원래 이미지에는 영향을 주지 않음
- 호스트와 독립된 파일 시스템을 제공받으므로 특정 컨테이너에서 어떤 어플리케이션 설치 및 삭제 시 다른 컨테이너와 호스트는 변화가 없음

### Container Creation

- 도커에서는 컨테이너를 생성할 수 있는 두 가지 명령어가 있음

  - `docker run`
  - `docker create`

- 컨테이너 생성 명령어는 이미지가 로컬 도커 엔진에 존재하지 않으면, 자동으로 도커 허브에서 이미지를 내려 받음

  > 만약 네트워크가 없다면, 아래 과정은 실패할 것이다.

  ```bash
  $ docker run ubuntu:18.04
  Unable to find image 'ubuntu:18.04' locally
  18.04: Pulling from library/ubuntu
  171857c49d0f: Pull complete 
  419640447d26: Pull complete 
  61e52f862619: Pull complete 
  Digest: sha256:646942475da61b4ce9cc5b3fadb42642ea90e5d0de46111458e100ff2c7031e6
  Status: Downloaded newer image for ubuntu:18.04
  
  $ docker create ubuntu:18.04
  ```

- 두 가지 명령어의 차이점은 아래와 같음

  

  


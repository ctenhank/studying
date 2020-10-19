# Stored data within containers

### Storage Driver

- Storage driver를 효율적으로 사용하기 위해서는 다음을 알아야 함
  - 이미지를 어떻게 빌드하고 저장하는가?
  - 어떻게 이런 이미지가 컨테이너로 사용되는가?
- 이를 통해 다음과 같은 것들을 알 수 있음
  - 어플리케이션으로부터 데이터를 유지하기에 가장 최선의 방법
  - 성능 문제가 발생하는 것을 방지
  - 이를 위해 [`docker volume`](volume.md)을 알아야 함

### Images and Layers

<img src="https://docs.docker.com/storage/storagedriver/images/container-layers.jpg" alt="Images and Layers" style="zoom:67%;" />

- 도커 이미지는 레이어 시리즈로 쌓아올려져 있음

- **최상단 레이어**를 제외한 나머지 레이어들은 `read-only`

  - 도커 엔진이 이미지를 바탕으로 컨테이너를 생성할 때 이미지 레이어의 가장 위에 생성하는 레이어

  - 실행 중인 컨테이너가 만들어내는 모든 변경 사항들은 이 `Thin R/W layer`에 저장됨

    > 변경사항에는 새로운 파일을 생성하거나, 기존의 파일을 수정·삭제하는 등

  - 따라서 가장 윗 층의 레이어는 **Writable layer** 또는 **Container Layer**라고도 불림

  - 앞으로는 이 글에서는 레이어를 **컨테이너 레이어**라고 함

- 각 레이어들은 [`dockerfile`](dockerfile.md)을 통해 표현할 수 있음

  ```dockerfile
  FROM ubuntu:18.04
  COPY . /app
  RUN make /app
  CMD python /app/app.py
  ```

- Storage drvier는 이러한 레이어들이 어떻게 서로 상호작용 하는지에 대해서 다룸

  > 따라서 상황에 따라 장·단점이 존재할 수 있음

### Containers and Layers

- 컨테이너와 이미지의 주요한 차이점은 컨테이너의 변경사항이 저장되는 최상단 레이어
- 동일한 이미지로 여러 컨테이너를 생성하면 각기 다른 컨테이너 레이어가 생성됨
  <img src="https://docs.docker.com/storage/storagedriver/images/sharing-layers.jpg" alt="Containers and Layers" style="zoom:67%;" />
- Storage driver는 이미지 레이어와 컨테이너 레이어를 다루는 것의 구현은 다를 수 있지만, 모든 드라이버들은 쌓을 수 있는 이미지 레이어와 CoW(Copy-on-Write) 기법을 사용함

### Container size on disk

- `docker ps -s` 명령어로 실행중인 컨테이너의 사이즈를 볼 수 있는데 사이즈에 대해 두 가지 컬럼이 있음
  - `size`: 컨테이너 레이어의 사이즈를 의미
  - `virtual size`
    - 컨테이너 레이어 + 이미지 레이어 사이즈를 의미
    - 다양한 컨테이너들은 이미지의 일부 또는 전체를 공유하는데, 실질적으로는 `read-only` 이미지를 공유하는 것이기 때문에 동일한 이미지를 이용하는  n 개의  컨테이너가 있더라도 이미지 한 개 용량 분량만 디스크를 차지

### The copy-on-write(CoW) Stategy

- 이미지의 어떤 낮은 층의 레이어에 파일이나 디렉토리가 존재하면, 또 다른 레이어는 그 레이어의 파일을 읽음
- 또다른 레이어가 그 파일을 변경해야 한다면, 그 파일은 그 레이어(또다른 레이어)에 복사되고 복사된 파일이 수정됨

#### Sharing promotes smaller iamges

- 이미지를 다운받는 경우는 두 가지가 있음

  - `docker pull` 명령어를 통해 image를 레지스트리에서 다운로드
  - 로컬에 없는 어떤 이미지로 컨테이너를 생성

- 이미지를 다운로드하면, 이미지의 각 레이어는 개별적으로 다운로드 받아지고 저장됨

- 리눅스의 경우 디폴트로 저장되는 경로는 `/var/lib/docker/<storage-driver>`

  > 이미지의 디렉토리 이름은 레이어 ID와는 다름

  ```bash
  $ docker pull ubuntu:18.04
  18.04: Pulling from library/ubuntu
  171857c49d0f: Pull complete 
  419640447d26: Pull complete 
  61e52f862619: Pull complete 
  Digest: sha256:646942475da61b4ce9cc5b3fadb42642ea90e5d0de46111458e100ff2c7031e6
  Status: Downloaded newer image for ubuntu:18.04
  docker.io/library/ubuntu:18.04
  
  # 이미지 확인
  $ ls /var/lib/docker/overlay2
  38113e6685eb5b787ddf909790bf6d8fa7fa18619d05348cdce129a98fa56fc4  b9d8fc2ee4a3805d52a0a524f064b8a6d8cf05491c14cc4fd7a207a6d23479fc
  6d7405672620f5032c8bfeaf7824a781e967975d15cfec7f747ced10182722ed  
  l
  ```

- `dockerfile`을 통해 동일한 이미지를 가지고 두 개의 컨테이너를 만들어 레이어들을 공유하고 있는지 확인해보자

  1. `Dockerfile.base` 생성

     ```dockerfile
     # Dockerfile.base
     FROM ubuntu:18.04
     COPY . /app
     ```

  2. `Dockerfile` 생성

     ```dockerfile
     # Dockerfile
     FROM acme/my-base-image:1.0
     CMD /app/hello.sh
     ```

  3. `hello.sh` 생성

     ```sh
     #!/bin/bash
     echo "Hello world"
     ```

  4. `Dockerfile.base` 파일을 사용해서 `acme/my-base-image:1.0`  이미지 빌드

     ```bash
     $ docker build -t acme/my-base-image:1.0 -f Dockerfile.base .
     Sending build context to Docker daemon  4.096kB
     Step 1/2 : FROM ubuntu:18.04
      ---> 56def654ec22
     Step 2/2 : COPY . /app
      ---> af35611334d1
     Successfully built af35611334d1
     Successfully tagged acme/my-base-image:1.0
     ```

  5. `Dockerfile` 파일을 사용해서 `acme/my-final-image:1.0` 이미지 빌드

     ```bash
     docker build -t acme/my-final-image:1.0 -f Dockerfile .
     Sending build context to Docker daemon  4.096kB
     Step 1/2 : FROM acme/my-base-image:1.0
      ---> af35611334d1
     Step 2/2 : CMD /app/hello.sh
      ---> Running in e63d6dee9c8e
     Removing intermediate container e63d6dee9c8e
      ---> 858632c73635
     Successfully built 858632c73635
     Successfully tagged acme/my-final-image:1.0
     ```

  6.  두 개의 이미지가 제대로 생성됐는지 확인해보자

     ```bash
     $ docker image ls
     REPOSITORY            TAG                 IMAGE ID            CREATED              SIZE
     acme/my-final-image   1.0                 858632c73635        7 seconds ago        63.2MB
     acme/my-base-image    1.0                 af35611334d1        23 seconds ago       63.2MB
     <none>                <none>              10ec75f1151e        About a minute ago   63.2MB
     ubuntu                18.04               56def654ec22        2 weeks ago          63.2MB
     ```

  7. `docker history IMAGE` 명령어를 이용해 각 이미지의 레이어를 확인해보자


     ```bash
     $ docker history ubuntu:18.04
     IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
     56def654ec22        2 weeks ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B                  
     <missing>           2 weeks ago         /bin/sh -c mkdir -p /run/systemd && echo 'do…   7B                  
     <missing>           2 weeks ago         /bin/sh -c [ -z "$(apt-get indextargets)" ]     0B                  
     <missing>           2 weeks ago         /bin/sh -c set -xe   && echo '#!/bin/sh' > /…   745B                
     <missing>           2 weeks ago         /bin/sh -c #(nop) ADD file:4974bb5483c392fb5…   63.2MB  
     $ docker history acme/my-base-image:1.0
     IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
     858632c73635        25 seconds ago      /bin/sh -c #(nop)  CMD ["/bin/sh" "-c" "/app…   0B                  
     af35611334d1        41 seconds ago      /bin/sh -c #(nop) COPY dir:761361cb9dc4164cd…   106B                
     56def654ec22        2 weeks ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B                  
     <missing>           2 weeks ago         /bin/sh -c mkdir -p /run/systemd && echo 'do…   7B                  
     <missing>           2 weeks ago         /bin/sh -c [ -z "$(apt-get indextargets)" ]     0B                  
     <missing>           2 weeks ago         /bin/sh -c set -xe   && echo '#!/bin/sh' > /…   745B                
     <missing>           2 weeks ago         /bin/sh -c #(nop) ADD file:4974bb5483c392fb5…   63.2MB              
     $ docker history acme/my-final-image:1.0
     IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
     af35611334d1        44 seconds ago      /bin/sh -c #(nop) COPY dir:761361cb9dc4164cd…   106B                
     56def654ec22        2 weeks ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B                  
     <missing>           2 weeks ago         /bin/sh -c mkdir -p /run/systemd && echo 'do…   7B                  
     <missing>           2 weeks ago         /bin/sh -c [ -z "$(apt-get indextargets)" ]     0B                  
     <missing>           2 weeks ago         /bin/sh -c set -xe   && echo '#!/bin/sh' > /…   745B                
     <missing>           2 weeks ago         /bin/sh -c #(nop) ADD file:4974bb5483c392fb5…   63.2MB              
     ```

### Copying makes containers efficient

- 컨테이너를 시작할 때 컨테이너 레이어는 다른 레이어들 최상단에 추가됨

- 변경이 없다면 아무것도 컨테이너 레이어에 복사되지 않음

- 변경이 있다면 Storage driver는 CoW 연산을 수행하는데 `aufs`, `overlayFS`의 순서는 다음과 같음

  1. 가장 최신 레이어부터 아래로 가면서 업데이트할 파일들이 있는 이미지 레이어를 찾음

     > 만약 파일이 있다면, 이는 다음 번 연산 속도 향상을 위해 캐시를 함

  2. 컨테이너 레이어에 파일을 복사하기 위해 `copy_up` 연산을 수행

     > `copy_up` 연산은 overhead를 발생시키는데 이는 드라이버마다 다를 수 있음 

  3. 복사본에 수정사항들을 반영함

- `zfs`, `btrfs` 등 다른 storage driver는 다르게 `CoW` 연산을 수행하는데 이는 나중에 좀 더 자세하게 알아봄

- 데이터를 저장해야 한다면 컨테이너 레이어에 저장하는 것이 아니라 [`docker volume`](volume.md)을 이용

- CoW 연산은 컨테이너 레이어만 생성하면 되니 저장 공간을 아낄뿐만 아니라 시작 시간 또한 줄여줌



### Select a storage driver

- 워크로드에 따라 가장 최적의 드라이버를 선택할 수 있어야 하는데 이를 위한 세 가지의 주요사항이 있음
  - 운영체제의 드라이버 지원 여부
  - backing filesystem 지원 여부
  - 도커 엔진 버전에 따른 지원 여부
- 도커는 `overlay2`, `aufs`, `devicemapper`, `btrfs`, `zfs`, `vfs` 등과 같은 드라이버를 지원
- 운영체제가 위와 같은 드라이버들 중 다수를 지원한다면, 우선순위에 따라 드라이버를 배정[[1]](https://github.com/docker/docker-ce/blob/19.03/components/engine/daemon/graphdriver/driver_linux.go#L50)

#### 운영체제의 드라이버 지원 여부[[2]](https://docs.docker.com/storage/storagedriver/select-storage-driver/#supported-storage-drivers-per-linux-distribution)

- Linux distribution마다 특정 드라이버는 지원 안될 수 있음
- Windows 또는 Mac은 드라이버를 변경하는 것이 불가능

| Linux distribution                  | Recommended storage drivers                                  | Alternative drivers                       |
| :---------------------------------- | :----------------------------------------------------------- | :---------------------------------------- |
| Docker Engine - Community on Ubuntu | `overlay2` or `aufs` (for Ubuntu 14.04 running on kernel 3.13) | `overlay`¹, `devicemapper`², `zfs`, `vfs` |
| Docker Engine - Community on Debian | `overlay2` (Debian Stretch), `aufs` or `devicemapper` (older versions) | `overlay`¹, `vfs`                         |
| Docker Engine - Community on CentOS | `overlay2`                                                   | `overlay`¹, `devicemapper`², `zfs`, `vfs` |
| Docker Engine - Community on Fedora | `overlay2`                                                   | `overlay`¹, `devicemapper`², `zfs`, `vfs` |

### backing filesystem 지원 여부

- backing filesystem은 `/var/lib/docker/`가 위치한 곳의 파일시스템
- 어떤 드라이버는 특정 backing filesystem만 이용할 수 있음

| Storage driver        | Supported backing filesystems |
| :-------------------- | :---------------------------- |
| `overlay2`, `overlay` | `xfs` with ftype=1, `ext4`    |
| `aufs`                | `xfs`, `ext4`                 |
| `devicemapper`        | `direct-lvm`                  |
| `btrfs`               | `btrfs`                       |
| `zfs`                 | `zfs`                         |
| `vfs`                 | any filesystem                |

### Other Considerations

#### Suitability for your workload

- 드라이버는 워크로드에 따라 성능적 특징들을 가짐
- `overlayFS`, `aufs`는 블록 레벨보다 파일 레벨에서 동작하는데, 이는 메모리를 더 효율적으로 사용하지만  `write-heavy workloads` 경우 컨테이너 레이어가 급속도로 커질수도 있음
- `devicemapper`, `btrfs`, `zfs`는 블록 레벨의 드라이버인데 `write-heavy workloads` 경우 더 효율적임
- `btrfs`, `zfs`는 많은 메모리를 필요하고, `zfs`는 PaaS와 같은 `high-density workload`에 좋음

#### Shared storage systems and the storage driver[[3]](https://docs.docker.com/storage/storagedriver/select-storage-driver/#shared-storage-systems-and-the-storage-driver)

#### Stability

- 어떤 사용자에게는 성능보다 안정성이 더 중요할 수 있음
- 도커에서 제공하는 드라이버는 대다수 안정적임

### Union Filesystem

- 다른 파일시스템에 대해서 통합된 디렉토리를 제공해주는 파일시스템 서비스

- 분리된 파일시스템의 파일과 디렉토리들을 하나의 파일시스템으로 만들어줌

- 각 드라이버의 레이어들은 `/var/lib/docker/<STORAGE-DRIVER>` 에 존재

- Storage Drvier를 원하는 드라이버로 바꾸는 법

  ```bash
  # aufs가 호스트 시스템에서 사용 가능한지 확인
  # aufs 대신 원하는 드라이버 입력(overlay2, zfs, btrfs, ...)
  $ grep aufs /proc/filesystems
  
  # 현재 도커가 어떤 드라이버를 이용하기 있는지 확인
  $ docker info
   ...
   Storage Driver: overlay2
    Backing Filesystem: extfs
    Supports d_type: true
    Native Overlay Diff: true
   ...
   
  # 해당 드라이버가 아니면 아래 명령어로 도커를 멈춤
  $ sudo systemctl stop docker
  # 도커 백업 만들기(필요하면 할 것)
  $ sudo cp -au /var/lib/docker /var/lib/docker.bk
  
  # /etc/docker/daemon.json 파일 수정
  $ sudo vim /etc/docker/daemon.json
  {
  	...
  	"storage-drvier": "aufs"
  	...
  }
  
  # 도커 재시작
  $ sudo systemctl start docker
  
  # storage-driver가 변경됐는지 확인
  $ docker info
  ```

  

### AUFS Storage Driver

- AUFS는 union filesystem인데, 이전에 이미지와 레이어를 관리하기 위해 디폴트로 사용된 드라이버
  ![aufs](https://docs.docker.com/storage/storagedriver/images/aufs_layers.jpg)
- `aufs`에서는 `layer`를 `branch`라고 부르고, `unification process`인 `union mount`를 통해 모든 레이어들이 하나의 디렉토리인 것처럼 보이게 만들어 줌
- 이미지 레이어들과 컨테이너 레이어는 `/var/lib/docker/aufs` 디렉토리에 위치하며, 각 이미지 또는 컨테이너 레이어의 ID는 하위 폴더들의 이름과 일치하지 않음
- `aufs`는 오버헤드를 최소화하면서 효율성을 극대화하기 위해 `CoW` 전략을 이용
- 이미지 및 컨테이너 레이어는 `/var/lib/docker/aufs/`에 위치해 있는데 각 레이어는 세 가지 디렉토리가 존재
  - `diff/`: 각 레이어의 컨테텐츠가 저장되어 있는 디렉토리
  - `layers/`: 이미지 레이어들이 어떻게 쌓이는지(순서)에 대한 메타데이터가 위치
  - `mnt/`: 각 이미지 레이어들과 컨테이너 레이어들이 마운트되는 디렉토리이며, 읽기 전용 이미지 레이어들은 항상 비어 있음

#### How Container reads and writes work with `aufs`

##### Reading files

- 컨테이너가 `aufs`를 이용하여 파일을 읽는 세 가지 시나리오가 있음

  - 컨테이너 레이어 파일이 존재하지 않을 때

    컨테이너 레이어에 존재하지 않는 파일을 읽으려고 하면, 드라이버는 이미지 레이어에서 파일을 찾은 후 읽음

  - 컨테이너 레이어에만 파일이 존재할 때

    컨테이너 레이어에 존재하는 파일을 읽으려고 하면, 그걸 그대로 읽음

  - 컨테이너 레이어와 이미지 레이어에 파일이 존재할 때

    컨테이너 레이어에서 파일을 읽지만, 이 파일은 이미지 레이어들에 존재하는 같은 이름의 파일을 모호하게 함

##### Modifying files or directories

- 파일을 처음으로 수정할 때
  - 컨테이너 레이어에 존재하지 않는 파일을 수정하려고 하면, `aufs` 드라이버는 `copy_up` 연산을 통해 파일이 존재하는 이미지 레이어로부터 컨테이너 레이어로 복사하고 이를 수정함
  - `aufs`는 파일 단위보다 block 단위로 동작하기 때문에, 그 파일이 매우 크지만 작은 부분을 수정하더라도 그 전체를 복사한다. 이는 성능 저하를 일으킬 수 있다.
  - 다음 수정부터는 이미 복사한 파일을 수정
- 파일이나 디렉토리를 삭제할 때
  - 컨테이너에서 파일이 지워진다면 이미지 레이어에서의 파일은 지워지지 않고 `whiteout` 파일이 생성되는데,  이는 컨테이너에서 그 파일을 이용하는 것을 막아줌
  - 컨테이너에서 디렉토리가 지워진다면, `opaque` 파일이 생기는데 위와 동일함
- 디렉토리의 이름을 수정할 때
  - `aufs`에서는 `rename`이 제대로 지원하지 않아서, `rename` 수행 시 `EXDEV`를 반환함
  - 따라서 `rename`을 하기위해서 `ESDEV`을 처리하는 적절한 루틴이 필요

### OverlayFS Storage Driver

- `aufs`와 비슷하게 더 최신의 `union filesystem`인데 구현하기가 좀 더 간단하면서 더 빠름
- 도커는 overlayFS를 두 가지 종류의 드라이버 `overlay`, `overlay2` 를 제공
- 도커에서는 `overlay2`를 사용하기를 권장함

#### How the `overlay` driver works

- OverlayFS 단일 Linux 호스트에서 두 디렉토리를 계층화하고 이를 하나의 디렉토리로 제공

- 이러한 디렉토리를 `layer`라고 하며, 통합 과정을 `union mount`라 함

- OverlayFS에서는 더 하층의 레이어(즉, parent)는 `lowerdir`이라 하며, 윗 층의 디렉토리를 `upperdir`이라 하고 통합된 디렉토리를 `merged`라 부름
  ![overlay](https://docs.docker.com/storage/storagedriver/images/overlay_constructs.jpg)

- 컨테이너 레이어와 이미지 레어어가 동일한 파일을 가지고 있으면, 컨테이너의 파일을 보여주며 이미지의 파일은 흐리게 함

- `overlay` 드라이버는 **오직 두개의 레이어로만 동작**하는데, 즉 다수의 레이어로는 구현하지 못함

- 각 이미지 레이어는 그 자신의 디렉토리로만 구성되고, **하위 레이어 파일들은 Hard link로 해당 이미지 레이어에서 참조**

- 하드 링크의 사용은 inode의 과도한 사용을 야기하며, 이는 `overlay`가 legacy가 된 이유 중 하나이며 또한 backing filesystem의 추가적인 구성이 필요할 수 있음

  > 이해할 수 없음. 하드 링크 사용은 오히려 inode 사용을 줄이지 않나?
  >
  > Answer:
  >
  > 먼저 알아야 하는 배경지식이 있다
  >
  > - 모든 파일(하드 링크 혹은 심볼릭 링크)는 inode를 사용
  > - 파일 시스템의 cycle 발생을 방지하기 위해 디렉토리에 대한 하드 링크는 불가능
  >
  > `overlay`에서 단 두 개의 레이어만 지원을 하기 위해서 하드 링크를 이용하면, 하위 이미지 레이어에 대한 모든 파일들을 최상위 이미지 레이어에 하드 링크로서 생성한다. 따라서 수많은 inode들이 사용되는데, `overlay2`에서는 하드링크 방식이 아니라 심볼릭 링크로 디렉토리를 참조하기 때문에 수많은 파일들을 하드링크 할 필요 없다. 따라서 수많은 inode들을 사용하지 않을 수 있다.

- 컨테이너를 생성하기 위해 `overlay` 드라이버는 이미지 최상위 레이어와 컨테이너의 새로운 디렉토리를 결합함

  > 이미지 최상위 레이어는 `lowerdir`이며 읽기 전용
  >
  > 컨테이너 레이어는 `upperdir`이며 수정 가능

- 이미지를 다운받아서 확인해보자

  ```bash
  # ubuntu 이미지를 다운받음
  $ docker pull ubuntu
  
  Using default tag: latest
  latest: Pulling from library/ubuntu
  
  5ba4f30e5bea: Pull complete
  9d7d19c9dc56: Pull complete
  ac6ad7efd0f9: Pull complete
  e7491a747824: Pull complete
  a3ed95caeb02: Pull complete
  Digest: sha256:46fb5d001b88ad9하드 링크로 04c5c732b086b596b92cfb4a4840a3abd0e35dbb6870585e4
  Status: Downloaded newer image for ubuntu:latest
  
  # overlay 디렉토리에 이미지 레이어들이 생성됐는지 확인
  $ ls -l /var/lib/docker/overlay/
  
  total 20
  drwx------ 3 root root 4096 Jun 20 16:11 38f3ed2eac129654acef11c32670b534670c3a06e483fce313d72e3e0a15baa8
  drwx------ 3 root root 4096 Jun 20 16:11 55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358
  drwx------ 3 root root 4096 Jun 20 16:11 824c8a961a4f5e8fe4f4243dab57c5be798e7fd195f6d88ab06aea92ba931654
  drwx------ 3 root root 4096 Jun 20 16:11 ad0fe55125ebf599da124da175174a4b8c1878afe6907bf7c78570341f308461
  drwx------ 3 root root 4096 Jun 20 16:11 edab9b5e5bf73f2997524eebeac1de4cf9c8b904fa8ad3ec43b3504196aa3801
  
  # 두 개의 레이어의 `ls`파일의 inode를 보면 동일한 파일을 가리킴을 확인할 수 있음
  # 이를 통해 효율적인 디스크 공간 사용을 하게 해줌
  $ ls -i /var/lib/docker/overlay/38f3ed2eac129654acef11c32670b534670c3a06e483fce313d72e3e0a15baa8/root/bin/ls
  
  19793696 /var/lib/docker/overlay/38f3ed2eac129654acef11c32670b534670c3a06e483fce313d72e3e0a15baa8/root/bin/ls
  
  $ ls -i /var/lib/docker/overlay/55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358/root/bin/ls
  
  19793696 /var/lib/docker/overlay/55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358/root/bin/ls
  ```

- 컨테이너를 생성해서 확인해보자

  ```bash
  $ ls -l /var/lib/docker/overlay/<directory-of-running-container>
  
  total 16
  -rw-r--r-- 1 root root   64 Jun 20 16:39 lower-id
  drwxr-xr-x 1 root root 4096 Jun 20 16:39 merged
  drwxr-xr-x 4 root root 4096 Jun 20 16:39 upper
  drwx------ 3 root root 4096 Jun 20 16:39 work
  
  # lower-id를 확인해보면, 최상위 이미지 레이어를 가리키는 것을 확인할 수 있음
  $ cat /var/lib/docker/overlay/ec444863a55a9f1ca2df72223d459c5d940a721b2288ff86a3f27be28b53be6c/lower-id
  
  55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358
  ```

#### How the `overlay2` driver work

- `overlay` 드라이버는 단 두 개의 레이어만 지원했던 것과는 달리 `128`개의 레이어까지 지원함

- `overlay` 드라이버의 디렉토리 개념 `lowerdir`, `upperdir`, `merged`는 동일

- `overlay2` 드라이버는 해당 디렉토리에서 `l` 디렉토리를 확인할 수 있는데, 이는 이미지의 심볼릭 링크

- base layer를 제외한 레이어들은 각 레이어 디렉토리의 `lower`  파일에 레이어들의 순서가 표현되어 있음

- `link` 파일은 해당 레이어의 ID, 즉 이 ID를 통해 해당 디렉토리를 표현

- `work/` 디렉토리는 OverlayFS에서 내부적으로 사용하는 디렉토리

  > 정확히 무슨 역할을 하는가?

#### How container reads and writes work with `overlay` or `overlay2`

##### Reading files in overlayFS

- `aufs`와 동일하게 세 가지 시나리오가 존재

  - 파일이 컨테이너 레이어에는 존재하지 않을 때
    `lowerdir`에서 파일을 찾아 읽는데, 이는 매우 적은 오버헤드를 발생시킬 수 있음

  - 파일이 컨테이너 레어어에만 존재할 때
    `upperdir`에서 파일을 직접 읽음

  -  파일이 컨테이너 레이어와 이미지 레이어에서 둘 다 존재할 때
    `upperdir`에서 파일을 읽고, `lowerdir`의 파일들은 흐리게 만듬

    > 흐리게 만든다는 것이 정확한 의미가 무엇인가?

##### Modifying files or directories in overlayFS

- `aufs` 와 동일한 시나리오

  - 처음으로 파일을 수정할 때
    [`aufs`와 유사하지만](#Modifying-files-or-directories) 차이점은 `aufs`는 이미지의 전체 레이어에서 파일을 찾은 반면, `overlay`는 단 두 개의 레이어만 검색하고 `overlay2`는 처음 읽기 때 cache를 해두기 때문에 좀 더 빠름

  - 파일이나 디렉토리를 삭제할 때

    - 파일을 삭제할 때는 `whiteout`파일이 `upperdir`에 생성되어 이미지 레이어의 파일들은 삭제되지 않고, 컨테이너 레이어 파일을 이용하려고 할 시 이를 막아줌
    - 디렉토리를 삭제할 때는 `opaque` 파일이 `upperdir`에 생성되어 `whiteout`파일과 동일한 동작을 함

  - 디렉토리 이름을 수정할 때

    컨테이너 레이어에서만 디렉토리 수정이 가능하며, 그렇지 않으면 `EXDEV` 에러가 리턴됨




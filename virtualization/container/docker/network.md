# Docker Network

- 도커 컨테이너들과 서비스들은 서로 연결할 수 있고, 또한 도커가 아닌 워크로드에도 연결할 수 있음

- 도커는 이렇게 연결할 수 있는 네트워크 기능을 자체적으로 지원하는데, 여러가지 네트워크 드라이버가 있음

  - `bridge`
  - `host`

  - `none`
  - `container`

  - `overlay`
  - `macvlan`
  - third-party plugins: `weave`, `flannel`, ...

- 도커는 컨테이너에 내부 IP를 순차적으로 할당하며 호스트와 통신에 사용

- 내부 IP는 컨테이너를 재시작할 때마다 변경될 수 있음

- 외부와 연결될 때는 컨테이너를 시작할 때마다 `veth···` 인터페이스를 생성하여 이뤄짐

- 도커가 설치될 시 디폴트로 존재하는 네트워크는 다음과 같음

  ```bash
  # host network configuration
  $ ifconfig
  ...
  docker0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
          inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
          inet6 fe80::42:fff:fe96:2fb2  prefixlen 64  scopeid 0x20<link>
          ether 02:42:0f:96:2f:b2  txqueuelen 0  (Ethernet)
          RX packets 90  bytes 98750 (98.7 KB)
          RX errors 0  dropped 0  overruns 0  frame 0
          TX packets 2667  bytes 543733 (543.7 KB)
          TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
  ...
  
  # default docker network list
  $ docker network ls
  NETWORK ID          NAME                DRIVER              SCOPE
  7e13c2e2794a        bridge              bridge              local
  d3cf64a9e06b        host                host                local
  ff6f0caaa861        none                null                local
  
  # check the bridge in docker network
  # the docker0 in host network is same as the bridge in docker network list
  $ docker network inspect bridge
  [
      {
          "Name": "bridge",
          ...
          "IPAM": {
              "Driver": "default",
              "Options": null,
              "Config": [
                  {
                      "Subnet": "172.17.0.0/16",
                      "Gateway": "172.17.0.1"
                  }
              ]
          },
          ...
      }
  ]
  ```

  

### Bridge Network

<img src="http://img.scoop.it/bmExZyvGWidultcwx9hCb7nTzqrqzN7Y9aBZTaXoQ8Q=" alt="bridge network" style="zoom:33%;" />

- bridge는 *네트워크 세그먼트* 사이에 트래픽을 전송하는 `Link Layer` 장치(HW or SW)

  > 네트워크 세그먼트는 하나의 네트워크를 bridge 등을 사용해서 분리했을 때 그 각각을 지칭하는 단위

- 도커에서는 소프트웨어 bridge를 이용하여 같은 bridge에 속하는 컨테이너들끼리 통신하게 해줌
- 도커 설치시 `bridge`는 자동으로 설정되는 네트워크 타입이며 `docker0`로 설정됨
- 동일한 호스트 상에서 운영하는 컨테이너들에만 적용이 되고, 다른 호스트들 사이의 통신에는 적용이 안 됨
  - 이를 위해서는 *OS 수준의 라우팅*이 필요하거나, `overlay network`를 이용해야 함
- 동일한 사용자 정의 브릿지 네트워크에 연결된 컨테이너들은 서로에게 모든 `port`를 노출시킴
- 다른 네트워크 상의 컨테이너 또는 도커와 관련없는 호스트에게 접근할 수 있는 포트를 위해 `-p` 옵션을 이용해야 함

#### Default Bridge Network and User-defined Bridge Network

- 사용자 정의 브릿지 네트워크는 컨테이너 사이의 automatic DNS resolution을 제공

  - default bridge network는 IP 주소로만 서로에게 접근할 수 있음

    > `--link` 옵션을 통해서 할 수 있지만 이는 `legacy`

  - user-defined bridge network에서는 컨테이너 이름이나 별칭을 통해 접근 가능

- 사용자 정의 브릿지는 더 나은 격리를 제공

  - `docker run` 명령어 이용할 때 `--network` 옵션을 이용해 네트워크를 설정하지 않으면 기본적으로 `bridge(docker0)`에 연결되는데, 이는 불필요한 연결을 야기시킬 수 있음

- 사용자 정의 네트워크는 적용된 컨테이너에서 그때그때 연결하거나 연결 해제할 수 있음

  - 디폴트 브릿지 네트워크를 재설정 하기 위해서는 컨테이너를 `stop`하고 재생성 해야 함

- 사용자 정의 네트워크는 새로운 설정을 생성할 수 있ᅌᅳᆷ

  - `사용자 정의 브릿지는 더 나은 격리를 제공`와 유사한 내용인데, default bridge network에서 수정을 가하면 이를 이용하고 있는 다른 컨테이너들에게도 영향을 끼칠 수 있음
  - 이를 위해 사용자 정의 네트워크를 생성하여 필요한 컨테이너들만 해당 네트워크에 연결

- 디폴트 브릿지 네트워크에 연결된 컨테이너들은 환경 변수들을 공유

  - 디폴트 브릿지 네트워크에서 컨테이너들이 환경 변수를 공유하는 것은 `--link` 옵션을 통해 가능했음
  - 사용자 정의 브릿지 네트워크는 위의 방법은 되지 않고 아래와 같은 방법으로 할 수 있음
    - `docker volume` 을 통해서 파일이나 디렉토리를 공유
    - ` docker-compose`를 이용한 변수 공유
    - `docker swarm`의 `service`를 이용



### Host Network

- 호스트와 컨테이너의 네트워크 격리를 없애고, 호스트 네트워킹을 그대로 이용

### None Network

- 네트워크 기능을 이용할 필요가 없을 때 사용

- ```bash
  docker run --rm -dit \
  --network none \
  --name no-net-alpine \
  alpine:latest \
  ash
  ```

- 

### Overlay Network

- 여러 호스트들을 연결하여 도커 스웜을 통해 서로 통신할 수 있는 서비스를 운용할 경우 이용
- 스웜 서비스와 standalone 컨테이너 사이에 통신할 때, 다른 호스트 상의 두 개의 standalone 컨테이너들 사이에 통신을 용이하게 함

### Container Network

### MacVLAN Network

- 컨테이너에 MAC 주소를 할당하여 네트워크 상에서 물리적 장치처럼 보이게 해줌
- 보통 물리적 장치에 직접적으로 네트워크가 필요한 `legacy application` 경우 주로 이용
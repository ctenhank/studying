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

- `docker network create -d(--driver) DRIVER NETWORK_NAME` 명령어를 통해 생성 가능

  > default driver는 `bridge`이다.

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

- 도커에서는 소프트웨어 bridge를 이용하여 같은 bridge에 속하는 컨테이너들에게 순차적으로 내부 IP를 부여하여 통신하게 해줌

- 도커 설치시 `bridge`는 자동으로 설정되는 네트워크 타입이며 `docker0`로 설정됨

- 동일한 호스트 상에서 운영하는 컨테이너들에만 적용이 되고, 다른 호스트들 사이의 통신에는 적용이 안 됨
  
  - 이를 위해서는 *OS 수준의 라우팅*이 필요하거나, `overlay network`를 이용해야 함
  
- 동일한 사용자 정의 브릿지 네트워크에 연결된 컨테이너들은 서로에게 모든 `port`를 노출시킴

- 다른 네트워크 상의 컨테이너 또는 도커와 관련없는 호스트에게 접근할 수 있는 포트를 위해 `-p` 옵션을 이용해야 함

  ```bash
  # bridge network 생성
  $ docker network create myBridge
  # bridge network 제거
  $ docker network rm myBridge
  $
  ```

- `docker network create -d bridge NETWORK` 명령어를 통해 사용자 정의 브릿지 네트워크를 생성하면 호스트의 운영체제에 해당 브릿지 네트워크를 생성함

  ```bash
  $ docker network ls
  NETWORK ID          NAME                DRIVER              SCOPE
  ...
  4f7a52330cc8        myBridge            bridge              local
  ...
  
  $ ifconfig
  ...
  # same id br-NETWORKID as docker bridge network defined 'myBridge'
  br-4f7a52330cc8: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
          inet 172.20.0.1  netmask 255.255.0.0  broadcast 172.20.255.255
          ether 02:42:f5:4f:47:e8  txqueuelen 0  (Ethernet)
          RX packets 0  bytes 0 (0.0 B)
          RX errors 0  dropped 0  overruns 0  frame 0
          TX packets 0  bytes 0 (0.0 B)
          TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
  ...
  ```

- `docker run`에서  `--net-alias` 옵션을 통해 특정 호스트 이름으로 컨테이너 여러 개에 접근할 수 있음

  - 내장 DNS가 특정 호스트 이름을 라운드 로빈 방식으로 설정한 컨테이너로 변환

    ```bash
    # 컨테이너 세 개 생성
    $ docker run --rm -dit \
    --name network_alias_container1 \
    --network myBridge \
    --net-alias na \
    alpine
    
    $ docker run --rm -dit \
    --name network_alias_container2 \
    --network myBridge \
    --net-alias na \
    alpine
    
    $ docker run --rm -dit \
    --name network_alias_container3 \
    --network myBridge \
    --net-alias na \
    alpine
    
    # IP 주소 확인
    $ docker inspect network_alias_container1 | grep IPAddress
                "SecondaryIPAddresses": null,
                "IPAddress": "",
                        "IPAddress": "172.20.0.2",
    
    # ping을 보내는 컨테이너 생성
    $ docker run --rm -it \
    --name network_alias_ping \
    --net myBridge \
    alpine
    
    # ping 컨테이너 안에서 ping을 실행해보면 동일한 na라는 이름으로 다양한 IP가 실행됨을 볼 수 있음
    # ping -c 1 na
    PING na (172.20.0.3): 56 data bytes
    ...
    
    # ping -c 1 na
    PING na (172.20.0.2): 56 data bytes
    ...
    
    # ping -c 1 na
    PING na (172.20.0.4): 56 data bytes
    ...
    ```

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

- 호스트와 컨테이너의 네트워크 격리를 없애고, 호스트의 네트워킹을 그대로 이용

- 성능 최적화를 하거나, 컨테이너가 매우 많은 `port`를 이용할 때 유용

  > NAT와 `userland-proxy`가 필요없음

- `Linux`에서만 사용 가능한 네트워크 타입이며, 윈도우, 맥에서는 사용할 수 없음

- `docker swarm`에서도 `host` 네트워크를 이용할 수 있는데, `control traffic`은 `overlay` 네트워크를 이용하면, service container들은 각 호스트의 네트워크와 포트를 이용

- 어떤 원리로 동작하는 것일까?

  > - 격리 수준을 없애니깐 단순하게 하나의 프로세스로 실행하는가?

  ```bash
  $ docker run --rm -dit \
  --network host \
  --name host-net-alpine \
  alpine \
  ash
  ```

- `docker run`에서  `--net-alias` 옵션을 통해 특정 호스트 이름으로 컨테이너 여러 개에 접근할 수 있음

  - 내장 DNS가 특정 호스트 이름을 라운드 로빈 방식으로 설정한 컨테이너로 변환

    ```bash
    # 컨테이너 세 개 생성
    $ docker run --rm -dit \
    --name network_alias_container1 \
    --network myBridge \
    --net-alias na \
    alpine
    
    $ docker run --rm -dit \
    --name network_alias_container2 \
    --network myBridge \
    --net-alias na \
    alpine
    
    $ docker run --rm -dit \
    --name network_alias_container3 \
    --network myBridge \
    --net-alias na \
    alpine
    
    # IP 주소 확인
    $ docker inspect network_alias_container1 | grep IPAddress
                "SecondaryIPAddresses": null,
                "IPAddress": "",
                        "IPAddress": "172.20.0.2",
    
    # ping을 보내는 컨테이너 생성
    $ docker run --rm -it \
    --name network_alias_ping \
    --net myBridge \
    alpine
    
    # ping 컨테이너 안에서 ping을 실행해보면 동일한 na라는 이름으로 다양한 IP가 실행됨을 볼 수 있음
    # ping -c 1 na
    PING na (172.20.0.3): 56 data bytes
    ...
    
    # ping -c 1 na
    PING na (172.20.0.2): 56 data bytes
    ...
    
    # ping -c 1 na
    PING na (172.20.0.4): 56 data bytes
    ...
    ```

    

### None Network

- 네트워크 기능을 이용할 필요가 없을 때 사용

  ```bash
  $ docker run --rm -dit \
  --network none \
  --name no-net-alpine \
  alpine:latest \
  ash
  ```


### Overlay Network

- `overlay` 네트워크는 여러 호스트들 사이의 분산 네트워크를 생성하여 컨테이너들이 서로 통신할 수 있게 해줌
- `docker swarm`을 초기화하거나, `swarm`에 참여하면, 그 도커 호스트에는 두 가지 네트워크가 생성됨
  - `ingress network`
    - 도커 스웜 서비스에 관련된 컨트롤 및 데이터 트래픽을 다룸
    - 스웜 서비스를 생성하고 이를 사용자 정의 오버레이 네트워크에 연결하지 않으면 자동으로 `ingress` 네트워크에 연결
  - `docker_gwbridge`
    - 여러 도커 데몬을 스웜에 참여하도록 서로서로 연결시켜줌
- `docker network create -d overlay NETWORK` 명령어를 통해서 사용자 정의 오버레이 네트워크를 생성할 수 있음
- [docker swarm](swarm.md)에 대해서 자세한 것은 링크에서 확인할 수 있음

#### Operation for Overlay Network

- swarm services와 standalone containers는 둘 다 overlay network에 연결할 수 있지만 각각에 대한 기본 동작 및 구성은 다름
- operation을 세 가지 범주로 나눠 overlay 네트워크는 여러 호스트로 구성되소개
  - operation for all overlay networks
  - operation for swarm services
  - operation for standalone containers

##### Operation for all overlay networks

- overlay 네트워크 생성은 일반적으로 아래와 같으나, standalone containers에서는 `--attachable` 옵션을 추가해줘야 이용할 수 있음

  - `docker network create -d overlay myOverlay`
  - `docker network create -d overlay --attachable myAttachableOverlay`

- overlay 네트워크를 이용하기 위해서는 먼저 호스트의 port를 개방해야 함

  - `2377/tcp` : 클러스터 관리 통신 관련 포트
  - `7946/tcp`, `7946/udp` : 노드 간 통신 관련 포트
  - `4789/udp` : overlay 네트워크 트래픽 관련 포트

- 오버레이 네트워크에서 트래픽을 암호화할 수 있음

  - 모든 swarm service를 관리하는 트래픽은 기본적으로 AES-GCM 알고리즘을 이용해 암호화됨

  - 어플리케이션 데이터를 암호화하기 위해서는 overlay network 생성 시 `--opt encrypted` 옵션을 추가해야 하는데 이는`vxlan` 수준에서 `IPsec` 암호화를 함

    (standalone container에서 사용하려면 `--attachable` 옵션을 추가해줘야 함)

    > 무시하지 못 할 성능 저하가 발생하기 때문에 이에 대한 테스트가 필요

  - 매니저 노드는 컨트롤 트래픽과 데이터 트래픽을 암호화하는 데 사용하는 키 값을 매 12시간마다 변경해줌

- `default ingress network` 커스텀마이징

  - ingress network 구성을 바꾸려면 제거 후 재생성해야 함
    - port를 publish한 서비스가 있다면, 이러한 서비스부터 제거해야 함
    - 남은 서비스는 계속해서 사용은 할 수 있지만 로드 밸런스는 되지 않음

  1. `docker network inspect ingress` 명령어를 통해 `ingress` 네트워크를 이용하고 있는 `published services`를 확인하고 제거

  2. `docker network rm ingress` 명령어를 통해 `ingress` 네트워크 제거

  3.  `ingress` 네트워크를 생성([driver options 확인](https://docs.docker.com/engine/reference/commandline/network_create/#bridge-driver-options))

     ```bash
     $ docker network create \
     --driver overlay \
     --ingress \
     --subnet=10.11.0.0/16
     --gateway=10.11.0.2
     --opt com.docker.network.driver.mtu=1200 \
     myIngress
     ```

  4. 사용할 서비스를 다시 생성한 네트워크에 연결하여 재시작

- `docker_gwbridge` 인터페이스 커스텀마이징

  - `docker_gwbridge`는 overlay network에 각 도커 데몬의 물리적 네트워크를 연결시켜주는 가상 브릿지
  - `docker swarm init` 또는 `docker swarm join` 시  자동으로 호스트에 생성하는데 이는 호스트의 커널을 이용

  ```bash
  # 1. 도커 중지
  $ sudo service docker stop
  
  # 2. 이미 존재하는 `docker_gwbridge`를 삭제
  $ sudo ip link set docker_gwbridge down
  $ sudo ip link del dev docker_gwbridge
  
  # 3. 도커 재시작
  $ sudo service docker start
  
  # 4. `docker_gwbridge` 재생성
  $ docker network create \
  --subnet 10.11.0.0/16 \
  --opt com.docker.network.bridge.name=docker_gwbridge \
  --opt com.docker.network.bridge.enable_icc = enable \
  docker_gwbridge
  ```

##### Operation for swarm services

- overlay network에 포트 노출
  - 동일한 오버레이 네트워크에 스웜 서비스를 연결하면 서로서로에게 모든 포트들을 노출시킴
  - 서비스의 외부와 연결 또는 통신하기 위해서는 `-p(--publish)` 옵션을 이용하여 포트를 노출시켜야 함
  - `-p` 옵션을 사용하는 다양한 포맷이 있는데 [링크](https://docs.docker.com/network/overlay/#operations-for-swarm-services/#operations-for-swarm-services)에서 확인하자
- 도커 스웜 서비스의 라우팅 메시 우회하기
  - Routing Mesh
    - 포트를 노출한 스웜 서비스는 디폴트로 라우팅 메시를 Virtual IP 모드에서 이용
    - 이 기능은 어떤 스웜 노드에서라도 해당 포트로 접근한다면, 그 서비스를 운영하고 있는 워커 노드로 재연결시켜줌
    - 라우팅 메시를 이용하면, 어떤 도커 노드가 클라이언트 요청을 서비스하는지에 대해 보장이 없음, 즉 무작위 노드가 뽑혀 이를 서비스해줌
  - `dnsrr`(DNS Round Robin)
    - `--endpoint-mode dnsrr`  옵션을 통해 할 수 있음
    - 그 서비스를 위해 로드 밸런서를 운영해야 함
- 컨트롤 트래픽과 데이터 트래픽 분리
  - 두 트래픽은 디폴트로 같은 네트워크에서 운용됨
  - 두 트래픽을 다른 네트워크에서 운영하기 위해서는  `swarm`을 `init` 할 때나 `join`할 때, `--addvertise-addr`과 `--datapath-addr` 옵션을 통해 분리

##### Operation for standalone containers

- `--attachable` 옵션 추가

### Container Network

### MacVLAN Network

- 보통 물리적 장치에 직접적으로 네트워크가 필요한 `legacy application` 또는 네트워크 트래픽을 모니터링 해야 하는 어플리케이션 같은 경우 주로 이용

- 각 컨테이너의 가상의 네트워크 인터페이스에 MAC 주소를 할당하여 네트워크 상에서 물리적 장치처럼 보이게 해줌

- 이를 지원해주는 도커 네트워크 타입이 `macvlan`이며, 또한 `subnet`과 `gateway`까지 부여할 수 있음

- `macvlan` 네트워크는 여러 가지 모드를 이용할 수 있음

  - `bridge mode`

    - `macvlan` 트래픽은 호스트의 물리적 장치를 통해 이동

      ```bash
      # 먼저 호스트의 물리적 네트워크 인터페이스를 확인
      $ ifconfig
      ...
      eno1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
              inet IP_ADDR  netmask 255.255.255.0  broadcast IP_ADDR_BROAD
              inet6 IP_V6_ADDR  prefixlen 64  scopeid 0x20<link>
              ether e0:d5:5e:8f:a2:3f  txqueuelen 1000  (Ethernet)
              RX packets 4922706  bytes 1948953837 (1.9 GB)
              RX errors 0  dropped 10992  overruns 0  frame 0
              TX packets 750353  bytes 153070212 (153.0 MB)
              TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
              device interrupt 16  memory 0xa1200000-a1220000  
      ...
      
      # network interface가 여러 개 있을 시, 그 중 원하는 물리적 네트워크 인터페이스를 택하여 할당해줌
      $ docker network create -d macvlan \
      --subnet=172.16.86.0/24 \
      --gateway=172.16.86.1 \
      -o parent=eno1 pub_net
        
      # 자동으로 할당되는 IP 주소 일부를 어떤 목적으로 제외시킬 수도 있음
      # --aux-addresses 옵션을 통해서 할 수 있ᅌᅳᆷ
      $ docker network create -d macvlan \
      --subnet=192.168.32.0/24 \
      --ip-range=192.168.32.128/25 \
      --gateway=192.168.32.254 \
      --aux-address="my-router=192.168.32.129" \
      -o parent=eno1 macnet32
      ```

  - `802.1q trunk bridge mode`

    - `802.1q` 프로토콜은 현재 VLAN 프로토콜 중 가장 널리 사용되고 있는 프로토콜

    - 트래픽은 도커가 호스트의 물리적 장치에 상황에 따라 생성한 서브 인터페이스를 통해 이동

    - 이는 라우팅과 필터링을 좀 더 세부적으로 컨트롤할 수 있게 해줌

      ```bash
      # 호스트의 물리적 네트워크 인터페이스에 서브 인터페이스를 생성하여 이를 이용할 수 있게 해줌
      $ docker network create -d macvlan \
      --subnet=192.168.50.0/24 \
      --gateway=192.168.50.1 \
      -o parent=eno1.50 macvlan50
      ```

  - `ipvlan mode`

    - `802.1q bridge mode`는 `L3 bridge` 였으나, `ipvlan`은 `L2 bridge`를 생성

    - `-o ipvlan_mode=12` 옵션을 통해서 생성할 수 있음

      ``` bash
      docker network create -d ipvlan \
      --subnet=192.168.210.0/24 \
      --subnet=192.168.212.0/24 \
      --gateway=192.168.210.254 \
      --gateway=192.168.212.254 \
      -o ipvlan_mode=l2 ipvlan210
      ```

      


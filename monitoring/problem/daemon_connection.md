# Docker Host와 Remote Client 연결 문제

어떤 호스트의 Docker Daemon에서 **Remote Connection**을 지원하도록 설정 변경이 필요

- `docker`는 기본적으로 보안 연결이 설정되어 있지 않기 때문에 문제가 발생할 수 있음: [해결책](#Solution: Security with TLS)

- `service`로서 도커를 실행시키는 대신 직접 터미널에서 아래 명령어 입력
  `dockerd -H unix:///var/run/docker.sock -H tcp://0.0.0.0:2375`

- `service`로서 도커를 실행시키고 remote client와 연결하는 방법[[1]]([https://100milliongold.github.io/2019/02/24/docker-remote-port-open-docker-%EC%9B%90%EA%B2%A9-API-%ED%99%9C%EC%84%B1%ED%99%94/](https://100milliongold.github.io/2019/02/24/docker-remote-port-open-docker-원격-API-활성화/)) ~링크참조~

  - `docker daemon`의 default port `2375` 개방

    ```bash
    sudo ufw enable
    sudo ufw allow 2375/tcp
    sudo ufw disable
    sudo ufw enable
    ```

  - `/lib/systemd/system/docker.service` 파일 수정

    ```
    ...
    [Service]
    ...
    EnvironmentFile=/etc/default/docker
    ExecStart=/usr/bin/dockerd -H fd:// $DOCKER_OPTS
    ...
    ```

  - `/etc/default/docker` 파일 수정

    ```
    ...
    DOCKER_OPTS="-H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock"
    ...
    ```

  - `docker` 리로드 및 재시작

    ```bash
    systemctl daemon-reload
    service docker restart
    ```

  - 테스트

    ```bash
    curl http://localhost:2375/version
    ```

    ```go
    package main
    
    import (
    	"context"
    	"fmt"
    
    	"github.com/docker/docker/api/types"
    	"github.com/docker/docker/client"
    )
    
    func main() {
        cli, err := client.NewClient(`tcp://{IPAddress}:2375`, `1.40`, nil, nil)
    	if err != nil {
    		panic(err)
    	}
    
    	containers, err := cli.ContainerList(context.Background(), types.ContainerListOptions{})
    	if err != nil {
    		panic(err)
    	}
    
    	for _, container := range containers {
    		fmt.Println(container.ID)
    	}
    }
    ```

### Solution: Security with TLS
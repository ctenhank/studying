# Docker Daemon

### Docker Daemon Execution [[2]][2]

- `docker daemon`은 설치 시 자동으로 서비스에 등록되어 `background`에서 실행됨
- `docker daemon`을 직접 실행하여서 디버깅이나 트러블 슈팅 등을 할 수도 있음

- 실행되고 있는 `docker daemon` 서비스를 시작/종료하는 법

  ```bash
  $ service --status-all
   ...
   [ - ]  docker
   ...
  # 서비스 종료
  $ service docker stop
  # 서비스 시작
  $ service docker start
  ```

- `docker daemon`을 서비스에서 (비)활성화하는 법

  ```bash
  # docker daemon을 서비스에서 활성화, 즉 재부팅시 자동으로 재실행됨
  $ systemctl enable docker
  
  # docker daemon을 서비스에서 비활성화, 즉 재부팅시 자동으로 재실행되지 않음
  $ systemctl disable docker
  ```

- `docker daemon` 실행

  ```bash
  # dockerd 명령어를 통해 실행하면 아래와 같은 로그들을 확인할 수 있음
  $ sudo dockerd
  INFO[2020-10-14T09:29:47.175319198+09:00] Starting up                                  
  ... 
  INFO[2020-10-14T09:29:47.798780006+09:00] API listen on /var/run/docker.sock           
  ```

### Docker Daemon Configuration


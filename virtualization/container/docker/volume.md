# Docker Volume

![types of mounts and where they live on the Docker host](https://docs.docker.com/storage/images/types-of-mounts.png)

### Features

- 도커 이미지로 컨테이너를 생성하면 이미지는 읽기 전용이 되며 컨테이너의 변경 사항은 컨테이너 계층(writable layer)에만 저장
- 이미지를 변경하지 않는다는 장점이 있지만, 컨테이너를 삭제하면 컨테이너 계층에 저장된 변경 사항은 삭제됨
- 이를 방지하기 위해 몇 가지 방법이 있음
  - docker volume
    - 도커가 관리하는 호스트 파일 시스템에 저장(`/var/lib/docker/volumes/`)
    - 도커 프로세스들이 아니면 이 파일 시스템을 수정하지 못함
  - bind mount
    - 호스트 파일시스템 어디든 저정할 수 있음
    - 도커와 관련없는 프로세스들도 이를 수정할 수 있음
  - tmpfs(only on Linux)
    - 호스트의 메모리에 저장
  - [named pipe(only on Windows)](https://en.wikipedia.org/wiki/Named_pipe)
- `docker volume`을 활용하는 방법은 여러 가지가 있음
  - 호스트와 볼륨 공유
  - 볼륨 컨테이너를 활용
  - 도커가 관리하는 볼륨 생성
- `docker run` 명령어에서 volume을 설정할 때 옵션
  - `-v`
  - [`--mount`](#--mount)
  - `Docker v17.06`  이전 버전에서는, `-v`는 단일 호스트의 컨테이너에 볼륨 할당하는 방법이고, `--mount`는 docker swarm service에서 볼륨 할당하는 방법
  - `Docker v17.06` 이후 버전부터는 `--mount`를 단일 호스트에서도 쓸 수 있고, 현재 도커에서는  `--mount`를 이용하기를 권장하고 있음 [[1]](https://docs.docker.com/storage/volumes/)

### Sharing Volume with Host

- 볼륨은 `docker run` 명령어에서 `-v HOST:CONTAINER` 옵션을 통해 지정할 수 있음

- 디렉토리 단위뿐만 아니라 단일 파일 단위의 공유도 가능

- 동시에 여러 개의 `-v` 옵션을 쓸 수 도 있음

  ```bash
  $ docker run -d \
  --name wordpressdb_hostvolume \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=wordpress \
  -v /home/wordpress_db:/var/lib/mysql \
  mysql:5.7
  ```

  ```bash
  $ docker run -d \
  -e WORDPRESS_DB_PASSWORD=password \
  --name wordpress_hostvolume \
  --link wordpressdb_hostvolume:mysql \
  -p 80 \
  wordpress
  ```

  ```bash
  $ ls /home/wordpress_db/
  auto.cnf    ca.pem           client-key.pem  ibdata1      ib_logfile1  mysql               private_key.pem  server-cert.pem  sys
  ca-key.pem  client-cert.pem  ib_buffer_pool  ib_logfile0  ibtmp1       performance_schema  public_key.pem   server-key.pem   wordpress
  ```

#### 호스트에 이미 디렉터리와 파일이 존재하고 컨테이너에도 존재할 때 두 디렉터리를 공유하면?

- 컨테이너의 디렉터리와 파일이 호스트의 것으로 덮어씌워짐
- 정확히 말하면 `-v` 옵션을 통한 호스트 볼륨 공유는 호스트 디렉터리를 컨테이너 디렉터리에 마운트하는 것

```bash
$ docker run -it \
--name volume_dummy \
alicek106/volume_test

root@469fde8802db:/# ls home/testdir_2/
test
```

```bash
$ docker run -it \
--name volume_overide \
-v /home/wordpress_db:/home/testdir_2 \
alicek106/volume_test

$ docker run -it --name volume_overide -v /home/wordpress_db:/home/testdir_2 alicek106/volume_test
root@f05ceb3f7617:/# ls home/testdir_2/
auto.cnf         client-key.pem  ibdata1             private_key.pem  sys
ca-key.pem       ib_buffer_pool  ibtmp1              public_key.pem   wordpress
ca.pem           ib_logfile0     mysql               server-cert.pem
client-cert.pem  ib_logfile1     performance_schema  server-key.pem

```

### Volume Container

- 이미 `-v` 옵션으로 볼륨을 사용하는 컨테이너를 다른 컨테이너와 공유하는 것

- 컨테이너를 생성할 때 `--volumes-from` 옵션을 설정하면 `-v or --volume` 옵션이 적용된 컨테이너의 볼륨 디렉터리를 공유할 수 있음

  ```bash
  $ docker run -it \
  --name volumes_from_container \
  --volumes-from volume_overide \
  ubuntu:18.04
  
  root@bab94123bf33:/# ls home/testdir_2/
  auto.cnf    ca.pem           client-key.pem  ib_logfile0  ibdata1  mysql               private_key.pem  server-cert.pem  sys
  ca-key.pem  client-cert.pem  ib_buffer_pool  ib_logfile1  ibtmp1   performance_schema  public_key.pem   server-key.pem   wordpress
  ```

### Docker Volume

- `docker volume`  명령어를 통해 도커 엔진이 관리하는 볼륨을 생성할 수 있음

- 도커 볼륨을 이용하고 있는 컨테이너가 삭제되더라도 도커 볼륨은 삭제되지 않음

- 여러 개의 컨테이너가 볼륨을 동시에 공유할 수 있음

  ```bash
  $ docker volume create --name myvolume
  myvolume
  
  $ docker volume ls
  DRIVER              VOLUME NAME
  local               myvolume
  
  $ docker run -it --name myvolume_1 \
  -v myvolume:/root/ \
  ubuntu:18.04
  root@d4a65d11fa97:/# echo hello, volume! >> /root/volume
  ```

  ```bash
  $ docker run -it --name myvolume_2 \
  -v myvolume:/root/ \
  ubuntu:18.04
  root@9a4d053f8b98:/# cat /root/volume 
  hello, volume!
  ```

- `docker inspect` 명령어를 통해 실제로 어디에 저장되는지 알 수 있음

  ```bash
  $ docker inspect --type volume myvolume
  [
      {
          "CreatedAt": "2020-10-14T15:54:19+09:00",
          "Driver": "local",
          "Labels": {},
          # the location saved the data of volume
          "Mountpoint": "/var/lib/docker/volumes/myvolume/_data",
          "Name": "myvolume",
          "Options": {},
          "Scope": "local"
      }
  ]
  
  $ sudo ls /var/lib/docker/volumes/myvolume/_data
  volume
  $ sudo cat /var/lib/docker/volumes/myvolume/_data/volume
  hello, volume!
  ```

- `docker volume` 명령어 대신 `docker run -v VOLUME:CONTAINER` 명령어를 통해 도커 볼륨을 생성할 수 있음

  > VOLUME은 존재하지 않는 볼륨 이름으로 설정하고, 만약 주어지지 않으면 무작위 16진수 형태 이름을 가짐

  ```bash
  $ docker run -it \
  --name volume_auto \
  -v autoVolume:/root \
  ubuntu:18.04
  ```

  ```bash
  $ docker volume ls
  DRIVER              VOLUME NAME
  local               autoVolume
  ```

### Stateless and Statefull Container

|         |                          Stateless                           |                     Statefull                      |
| ------- | :----------------------------------------------------------: | :------------------------------------------------: |
| Meaning | 컨테이너가 아닌 외부에 데이터를 저장하고, 그 데이터로 동작하는 것 | 컨테이너가 데이터를 저장하고 있어 상태가 있는 경우 |

### --mount

- 







## Reference

[1]: https://docs.docker.com/storage/volumes/ "Choose the -v or --mount flag"
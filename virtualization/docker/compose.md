# Docker Compose

<img src="img/docker-compose.png" alt="Docker Compose" style="zoom:50%;" />

- `docker-compose`는 여러 개의 컨테이너를 하나의 서비스로 정의해 컨테이너 묶음으로 관리할 수 있게 함
- 여러 개의 컨테이너 옵션과 환경을 정의한 파일을 읽어 컨테이너를 순차적으로 생성하는 방식으로 동작
- `docker-compose` 설정 파일은 `docker run` 명령어 옵션을 그대로 사용할 수 있음
- 각 컨테이너의 의존성, 네트워크, 볼륨 등을 함께 정의할 수 있음
- 스웜 모드의 서비스와 유사하게 설정 파일에 정의된 서비스 컨테이너 수를 유동적으로 조절 가능
- 컨테이너 서비스 디스커버리도 자동으로 이뤄짐

### Installation

[참고](https://docs.docker.com/compose/install/)

#### Problems

1. Can only use in super user mode(`sudo su`)



## How to use?

### Basic Usage

`docker-compose` read YAML files, extension `.yml`,  which defined settings of container

```bash
# Example
# docker run commands for executing a service
# it's same as below docker-compose.yml file
$ docker run -d  --name mysql \
alicek106/composetest:mysql \
mysqld

$ docker run -d -p 80:80 \
--link mysql:db --name web \
alicek106/composetest:web \
apachectl - DFOREGROUND
```

- **Writing a `docker-compose.yml` file**

  - [details of YAML file grammer in docker-compose](yaml.md)
  - it doesn't work using `tab` for indentation, so you should use `2 or 4 spaces` 
  - Basic grammar: `version`, `services`, `SERVICE`

  ```yaml
  #docker-compose.yml file as same as above example commands
  version: '3.0'
  services:
    web:
      image: alicek106/composetest:web
      ports:
        - "80:80"
      links:
        - mysql:db
      command: apachectl -DFOREGROUND
    mysql:
      image: alicek106/composetest:mysql
      command: mysqld
  ```

- `docker-compose up` command

  - Basically it executes yaml files, `docker-compose.yml`, on the current directory, if it didn't be given specific files in the command using option `-f`

  ```bash
  # result using docker-compose
  root:/test/docker-compose# docker-compose up -d
  WARNING: The Docker Engine you're using is running in swarm mode.
  
  Compose does not use swarm mode to deploy services to multiple nodes in a swarm. All containers will be scheduled on the current node.
  
  To deploy your application across the swarm, use `docker stack deploy`.
  
  Creating network "docker-compose_default" with the default driver
  Creating docker-compose_mysql_1 ... done
  Creating docker-compose_web_1   ... done
  
  # container Naming in docker-compose
  # - container Name: [PROJECT NAME]_[SERVICE NAME]_[COTANINER NUMBER]
  # - if don't write a [PROJECT NAME] in `docker-compose.yml`, it is replaced by current directory name
  root:/test/docker-compose# docker ps
  CONTAINER ID    IMAGE                         COMMAND     CREATED          STATUS         PORTS    NAMES
  f1359eab5f76    alicek106/composetest:mysql   "mysqld"    11 minutes ago   Up 11 minutes           docker-compose_mysql_1
  ```

  - Be able to give `PROJECT NAME` using option `-p PROJECT`, where between command `docker-compose` and sub-command `up`
    `docker-compose -p PROJECT up`

    ```bash
    root:/test/docker-compose# docker-compose -p testProject up -d
    WARNING: The Docker Engine you're using is running in swarm mode.
    
    Compose does not use swarm mode to deploy services to multiple nodes in a swarm. All containers will be scheduled on the current node.
    
    To deploy your application across the swarm, use `docker stack deploy`.
    
    Creating network "testproject_default" with the default driver
    Creating testproject_mysql_1 ... done
    Creating testproject_web_1   ... done
    ```

- `docker-compose down` command

  - To delete a project, consisted of services and containers, use command `docker-compose down`


    ```bash
    root:/test/docker-compose# docker-compose down
    Stopping docker-compose_mysql_1 ... done
    Removing docker-compose_web_1   ... done
    Removing docker-compose_mysql_1 ... done
    Removing network docker-compose_default
    ```

  - Also, be able to a specific project using option `-p` as same as `docker-command -p PROJECT up`

### docker-compose with Docker Swarm

- The command `docker stack` is added in docker engine
  (version: DE >= 1.13, YAML >= 3, docker-compose >= 1.10)

- **stack** is set of containers created by YAML file

- **stack** deploys the containers on `docker swarm`, specifying cluster

- stack is created by `swarm-kit`, use `docker service scale SERVICE=NUMBER` to adjust number of containers, not `docker-compose scale`

- stack's default network is `overlay` network compared to docker-compose, which default is `bridge` network

  ```yaml
  # docker-compose.yml
  root:/test/docker-compose# cat docker-compose.yml
  version: '3.0'
  services:
    web:
      image: alicek106/composetest:web
      ports:
        - "80:80"
      links:
        - mysql:db
      command: apachectl -DFOREGROUND
    mysql:
      image: alicek106/composetest:mysql
      command: mysqld
  ```

  ```bash
  # deploy services using docker stack
  root:/test/docker-compose# docker stack deploy -c docker-compose.yml mystack
  Ignoring unsupported options: links
  
  Creating network mystack_default
  Creating service mystack_web
  Creating service mystack_mysql
  
  # stack list
  root@dohan:/home/dohan/test/docker-compose# docker stack ls
  NAME                SERVICES            ORCHESTRATOR
  mystack             2                   Swarm
  
  # specified service list
  root@dohan:/home/dohan/test/docker-compose# docker stack services mystack
  ID                  NAME                MODE                REPLICAS            IMAGE                         PORTS
  qna9uzyhan5n        mystack_mysql       replicated          1/1                 alicek106/composetest:mysql   
  v1igzbkkq4bx        mystack_web         replicated          1/1                 alicek106/composetest:web     *:80->80/tcp
  ```

  
























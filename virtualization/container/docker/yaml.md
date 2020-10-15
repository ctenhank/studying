# YAML Grammar used in docker-compose

- it doesn't work using `tab` for indentation in YAML file grammar, so you should use `2 or 4 spaces` [[1]](https://stackoverflow.com/questions/19975954/a-yaml-file-cannot-contain-tabs-as-indentation)

### YAML Version

- There are many verision of yaml, it's better using the newest version

#### Usage

```yaml
version: '3.0'
```

### Service

- Basically defines services using key, `services`, then defines for each service using the service name

  #### Basic Usage

  ```yaml
  version: '3.0'
  services:
    my_container_1:
      image: ...
    my_container_2:
      image: ...
  ```

- Many options for service:

  `image`, `links`, `environment`, `command`, `depends_on`, `ports`, `build`, `extends`

- **image**

  - a image of container. 

  - if there is no container in your local, it automatically pulls the image from `docker registry`

    ```yaml
    services:
      my_container_1:
        image: alicek106/composetest:mysql
    ```

- **links**

  - same as `docker run --link`, is able to access other service only using service name. 

  - also can use alias using `[SERVICE:ALIAS]`

    ```yaml
    services:
      web:
        links:
          - db
          - db:database
          - redis
    ```

- **environment**

  - same as `docker run {--env, -e}`, specifies environment variable inner of container

  - be able to use `dictionary`, `array` 

  - the assignment operation can use either `=` or `:`

    ```yaml
    services:
      web:
        environment:
          - MYSQL_ROOT_PASSWORD=mypassword
          - MYSQL_DATABASE_NAME:mydb
    ```

- **command**

  - command executed in afuture container, executed by command `docker run`

  - be able to use `array`

    ```yaml
    services:
      web:
        environment:
          image: alicek106/composetest:web
          command: apachectel -DFOREGROUND
          				or
          command: [apachectel, -DFOREGROUND]
    ```

- **depends_on**

  - means dependecies on certain containers that created and executed at first

  - `docker-compose up --no-deps SERVICE`
    specify the option `--no-deps` in `docker-compose up` to create specific container without dependency

    ```yaml
    services:
      web:
        image: alicek106/composetest:web
        depends_on:
          - mysql
      mysql:
        image: alicek106/composetest:mysql
    ```

    

  > `links`, `depends_on` only specifies sequence of exections, not checking state which container is ready.
  >
  > For example, database and web server
  >
  > The database is executed earlier than web server. Although database is executed earlier, it didn't complete initializing yet before executing web  server. It may make the web server not be working well.
  >
  > To solve it, specify key, `entrypoint` to check the state of container.
  >
  > ```yaml
  > services:
  >   web:
  >     ...
  >     entrypoint: ./sync_script.sh mysql:3306
  > ```
  >
  > ```sh
  > #  sync_script.sh
  > until (state-checking commands); do
  >   echo "depend container is not available yet"
  >   sleep 1
  > done
  >   echo "depends_on container is ready"
  > ```

- **ports**

  - specify a certain port as same as `docker run -p HOST:CONTAINER`

    ```yaml
    services:
      web:
        image: alicek106/composetest:web
        ports:
          - "8080"
          - "8081-8085"
          - "80:80"
          ...
    ```

- **build**

  - be able to use [`DockerFile`](DockerFile.md) , using specified image in the service

    ```yaml
    services:
      web:
        build: ./composetest
        # the name of image, builded in a DockerFile
        image: aliceck106/composetest:Web
        or
        build: ./composetest
        context: ./composetest
        dockerfile: myDockerFile
        args:
          HOST_NAME: web
          HOST_CONFIG: self_config
    ```

- **extends**

  - inherits attributes of other service in either current YAML file or other

    ```yaml
    # docker-compose.yaml
    version: '3.0'
    services:
      web:
        extends:
          file: extend_compose.yml
          service: extend_web
    ```

    ``` yaml
    # extend-compose.yaml
    version: '3.0'
    services:
      extend_web:
        image: ubuntu14.04
        ports:
          - "80:80"
    ```

    ```yaml
    # extend in same file
    version: '3.0'
    services:
      web:
        extends:
          service: extend_web
      extend_web:
        image: ubuntu:14.04
        ports:
          - "80:80"
    ```

### Network

- Basically `docker-compose up` and `docker-compose scale` command uses `bridge type network`
- Automatically set service name to network alias of container, so be able to access container of the serivce using service name

- driver

  - Basically docker-compose use bridge network for created container

  - Specifiy other network using `driver` key and `driver_opts` key

    ```yaml
    version: '3.0'
    services:
      myservice:
        image: nginx
        networks:
          - mynetwork
    networks:
      mynetwork:
        driver: overlay
        driver_opts:
          subnet: "255.255.255.0"
          IPAdress: "10.0.0.2"
    ```

- ipam

  - IPAM(IP Address Manager) specifies subnet, ip range

    ```yaml
    ...
    networks:
      ipam:
        driver: mydriver
        config:
          subnet: 172.20.0.0/16
          ip_range: 172.20.5.0/24
          gateway: 172.20.5.1
    ```

- external

  - Use a existed network, not create a new network whenever create project using certain YAML file

    ```yaml
    services:
      web:
        image: alicek106/composetest:web
        networks:
          - alicek106_network
    networks:
      alicek106_network:
        external: true
    ```

### Volume

- driver

  ```yaml
  ...
  volumes:
    driver: flocker
      driver_opts:
        opt: "1"
        opt2: 2
  ```

- external

  - same as `network external`

    ```yaml
    services:
      web:
        image: alicek106/composetest:web
        volumes:
          - myvolume:/var/www/html
          
    volumes:
      myvolume:
        external: true
    ```

### Parsing  YMAL file

- `docker-compose config`
  check typos, file format, etc. about a YAML file

  ```bash
  # result
  root:/test/docker-compose# docker-compose config
  services:
    mysql:
      command: mysqld
      image: alicek106/composetest:mysql
    web:
      command: apachectl -DFOREGROUND
      image: alicek106/composetest:web
      links:
      - mysql:db
      ports:
      - published: 80
        target: 80
  version: '3.0'
  ```












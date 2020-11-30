```dockerfile
version: "2"
services:
  nextcloud:
    image: linuxserver/nextcloud:amd64-latest
    container_name: nextcloud
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Seoul
    volumes:
      - /srv/md0/docker/nextcloud/config:/config
      - /srv/md0/docker/nextcloud/data:/data
    ports:
      - 443:443
    depends_on:
      - nextcloud-mariadb
    restart: unless-stopped
  nextcloud-mariadb:
    image: linuxserver/mariadb:amd64-latest
    container_name: mariadb
    environment:
      - PUID=1000
      - PGID=1000
      - MYSQL_ROOT_PASSWORD=sslab1!
      - TZ=Asia/Seoul
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=sslab
      - MYSQL_PASSWORD=sslab1!
    volumes:
      - /srv/md0/docker/mariadb/config:/config
    ports:
      - 3306:3306
    restart: unless-stopped
```

```
version: '2'

networks:
  nextcloud_network:
    external: false

services:
  nextcloud:
    image: wonderfall/nextcloud:15
    container_name: nextcloudt
    depends_on:
      - db_nextcloud           # If using MySQL
      # - solr                   # If using Nextant
      # - redis                  # If using Redis
    environment:
      - UID=1000
      - GID=1000
      - UPLOAD_MAX_SIZE=10G
      - APC_SHM_SIZE=128M
      - OPCACHE_MEM_SIZE=128
      - CRON_PERIOD=15m
      - TZ=Asia/Seoul
      - ADMIN_USER=sslab            # Don't set to configure through browser
      - ADMIN_PASSWORD=sslab1!        # Don't set to configure through browser
      - DOMAIN=localhost
      - DB_TYPE=mysql
      - DB_NAME=nextcloud
      - DB_USER=sslab
      - DB_PASSWORD=sslab1!
      - DB_HOST=db_nextcloud
    ports:
      - "8888:8888"
    volumes:
      - /srv/md0/docker/nextcloud/data:/data
      - /srv/md0/docker/nextcloud/config:/config
      - /srv/md0/docker/nextcloud/apps:/apps2
      - /srv/md0/docker/nextcloud/themes:/nextcloud/themes
    networks:
      - nextcloud_network

  # If using MySQL
  db_nextcloud:
    image: mariadb:10
    container_name: mariadb2
    volumes:
      - /srv/md0/docker/nextcloud/db:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=sslab
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=sslab
      - MYSQL_PASSWORD=sslab1!
    networks:
      - nextcloud_network

  # # If using Nextant
  # solr:
  #   image: solr:6-alpine
  #   container_name: solr
  #   volumes:
  #     - /docker/nextcloud/solr:/opt/solr/server/solr/mycores
  #   entrypoint:
  #     - docker-entrypoint.sh
  #     - solr-precreate
  #     - nextant
  #   networks:
  #     - nextcloud_network

  # # If using Redis
  # redis:
  #   image: redis:alpine
  #   container_name: redis
  #   volumes:
  #     - /docker/nextcloud/redis:/data
  #   networks:
  #     - nextcloud_network
```


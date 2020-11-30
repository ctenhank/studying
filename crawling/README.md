# Crawling Earthquake Data from Korea Meteorlogical Administration

기상청 홈페이지에서 지진 관련 데이터를 가져와 자체 시스템 데이터베이스에 저장한다.

- url: https://www.weather.go.kr/weather/earthquake_volcano/
- 어떤 주기(매일 혹은 특정 주기)마다 한 번씩 프로그램을 실행하여 해당 `url`에 존재하는 지진 데이터들을 가져와서 자체 데이터베이스 시스템에 저장한다.
  - 기존에 존재하는 데이터와 새로운 데이터는 다음과 같이 구분한다.
    - 단순히 번호 한 개의 데이터만으로 구분
    - 발생 시각 및 규모, 깊이, 최대 진도, 위도, 경도, 위치로 구분
- 새로운 데이터의 위도와 경도 기점으로 40km 이내의 데이터들을 모아서 따로 저장하여 표현하며, 이는 `entrypoint`로 나타내어 이용가능할 수 있게끔 한다.



## Components

- Crawler

- Database1(saved)

  - Using Container of cassandra database using python client
    https://hub.docker.com/_/cassandra

    > ## Make a cluster
    >
    > Using the environment variables documented below, there are two cluster scenarios: instances on the same machine and instances on separate machines. For the same machine, start the instance as described above. To start other instances, just tell each new node where the first is.
    >
    > ```
    > $ docker run --name some-cassandra2 -d --network some-network -e CASSANDRA_SEEDS=some-cassandra cassandra:tag
    > ```
    >
    > For separate machines (ie, two VMs on a cloud provider), you need to tell Cassandra what IP address to advertise to the other nodes (since the address of the container is behind the docker bridge).
    >
    > Assuming the first machine's IP address is `10.42.42.42` and the second's is `10.43.43.43`, start the first with exposed gossip port:
    >
    > ```
    > $ docker run --name some-cassandra -d -e CASSANDRA_BROADCAST_ADDRESS=10.42.42.42 -p 7000:7000 cassandra:tag
    > ```
    >
    > Then start a Cassandra container on the second machine, with the exposed gossip port and seed pointing to the first machine:
    >
    > ```
    > $ docker run --name some-cassandra -d -e CASSANDRA_BROADCAST_ADDRESS=10.43.43.43 -p 7000:7000 -e CASSANDRA_SEEDS=10.42.42.42 cassandra:tag
    > ```

  - 데이터베이스에 이미지 저장할 때, 오브젝트로 주고받는게 나을까? 아니면 파일로 저장해두고 이용하는 것이 나을까?

- Database2(sensor data)



## Improvement

#### Using `multiprocessing` module of python standard library

##### Before

```python
start_time = time.time()
for page in pages:
    # get data using found pages
    row, col = crawl_data(page)
    rows.append(row)
    cols.append(col)
print("%s seconds"% (time.time()-start_time))

##### RESULT: 9.800392389297485 seconds
```

##### RESULT 

```python
start_time = time.time()
with Pool(processes=4) as p:
    ret = p.map(crawl_data, pages)
    # print(p.map(crawl_data ,pages))
print("TOTAL TIME: %s"% (time.time() - start_time))
##### TOTAL TIME: 2.6447207927703857
```



## Problems

- 기상청 홈페이지가 인덱스 1200개까지밖에 지원을 안해줌






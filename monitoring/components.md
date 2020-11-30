# Container Monitoring System

컨테이너 모니터링 시스템은 기본적으로 다섯 가지 컴포넌트들로 이루어져 있다.

- 서비스 디스커버리
- 데이터 콜렉터
- 데이터베이스
- 대시보드
- 알림

### 서비스 디스커버리

 서비스 디스커버리는 서비스 및 컨테이너들을 분산 시스템에서 운용하는 어플리케이션이다. 도커, 쿠버네티스 등 다양한 어플리케이션이 존재하며 현재 **도커**, 정확히는 **도커 스웜**만을 지원한다.



### 데이터 콜렉터

 데이터 콜렉터는 서비스 디스커버리 API를 이용하여 노드, 서비스, 컨테이너들의 `log`, `metric` 등 다양한 정보들을 모으는 컴포넌트이다. 현재 서비스 디스커버리 **도커**의 API를 이용하여 개발 중에 있다. 



### 데이터베이스

데이터베이스는 데이터 콜렉터가 모으는 데이터들을 저장한다. 시계열 데이터에 특화된 **influxdb**를 이용하고 있다.

### influxdb

**시계열 데이터**에 특화된 오픈소스 데이터베이스 플랫폼으로, **golang**으로 구현되었다. influxDB가 기본으로 사용하는 포트는 **8086**이다. 또한 influxDB는 기존 RDBMS와는 다른 용어들을 이용하고 있다. 이는 `database`, `field key`, `field set`, `field value`, `measurement`, `point`, `retention policy`, `series`, `tag key`, `tag set`, `tag value`, `timestamp`가 있다.[[1]][1]

이에 대해서 예를 가지고 쉽게 이해해보자.

#### Example: Butterflies and Honeybees

이 예는 두 과학자 `langstroth`, `perpetua`가 2015년 8월 18일 자정부터 아침 6시 12분까지 지역 `1`, `2`에서 나비와 꿀벌의 수를 세알린 데이터이다. 즉, 인구 조사(census) 데이터이다.

| timestamp            | butterflies | honeybees | location | scientist  |
| -------------------- | ----------- | --------- | -------- | ---------- |
| 2015-08-18T00:00:00Z | 12          | 23        | 1        | langstroth |
| 2015-08-18T00:00:00Z | 1           | 30        | 1        | perpetua   |
| 2015-08-18T00:06:00Z | 11          | 28        | 1        | langstroth |
| 2015-08-18T00:06:00Z | 3           | 28        | 1        | perpetua   |
| 2015-08-18T05:54:00Z | 2           | 11        | 2        | langstroth |
| 2015-08-18T06:00:00Z | 1           | 10        | 2        | langstroth |
| 2015-08-18T06:06:00Z | 8           | 23        | 2        | perpetua   |
| 2015-08-18T06:12:00Z | 7           | 22        | 2        | perpetua   |

앞서 말했던 것과 같이 influxDB는 시계열 데이터에 특화된 데이터베이스인데, 이를 위해 모든 데이터에 대해서 시간을 저장한다. 이는 각 데이터의 **첫 컬럼**, `time`에 저장되며 `rfc3399` 등 다양한 설정 값이 존재한다.

그 다음 열 `나비`와 `꿀벌` 컬럼은 `field`라고 불리는데, 이는 `field key`와 `field value`로 이루어진다. **`field key`**는 어떤 데이터를 의미하는지 나타내주는 문자열, 즉 `나비`, `꿀벌` 문자열을 의미한다. **`field value`**는 `field key`에 대한 데이터 값, 즉 `나비`에서는 `12`-`7`의 데이터들, `꿀벌`에서는 `23`-`22`의 데이터들을 의미한다. `field value`의 데이터 타입은 `string`, `float`, `integer`, `boolean` 값이 될 수 있으며, 이러한 값들은 `timestamp`와 관련이 있다.

또한 이러한 `field` 값들은 예제에서는 하나의 쌍으로 `row`를 이루고 있는데, 예를 들어서 첫 번째 `row`는 `나비=12, 꿀벌=23`, …, 마지막 `row`는 `나비=7, 꿀벌=22` 등으로 이루어져 있다. 이러한 하나의 `row`를 이루고 있는 `field key`와 `field value`들의 묶음을 **`field set`**이라 한다.

**`field`들은 influxDB 데이터 구조에서 반드시 필요하다.** 즉, `field`가 없으면 데이터를 저장할 수 없다. 또한 `field `값은  `index`하지 않는다. 예를 들어서 데이터 쿼리를 할 때 `field` 값을 기준으로 읽으면, 모든 데이터를 읽고나서 비교까지 해야하기 때문에 성능이 매우 느려질 수 있다. 따라서 이러한 `filtering`할 수 있는 `index`는 **`tag`**로 한다.

`tag` 또한, `tag key`, `tag value`로 이루어져 있는데, 위의 예에서는 `과학자`, `위치`이다. `tag key`와 `tag field` 값들은 **문자열로 저장**되며 `metadata`를 기록한다.

**`tag set`**은 가능한 모든 `tag key-value` 값들의 조합인데, 위의 예에서는 다음과 같다.

- `location=1`, `scientist=langstroth`
- `location=2`, `scientist=langstroth`
- `location=1`, `scientist=perpetua`
- `location=2`, `scientist=perpetua`

**`tag`는 반드시 필요한 것은 아니지만,** `index`할 때 이용하기 때문에 이들을 활용하는 것이 쿼리를 좀 더 빠르게 할 수 있는 좋은 방법이다. 이는 `tag set`기준으로 정렬하면 모든 데이터를 필요한 정보만 찾을 수 있기 때문이다.

**`measurement`**는 `tag`, `field`, `time` 컬럼들의 컨테이너 역할을 한다. 따라서 `measurement` 이름은 `field`에 저장되는 데이터 값들을 설명해줄 수 있다. `measurement`는 **RDBMS**에서는 **table**과 유사하다. 또한 동일한 `measurement`는 다른 `retention policies`를 가질 수 있는데, 이는 influxdb가 얼마나 그 데이터들을 유지하는가**(duration)** 또는 그 데이터가 클러스터에 얼마나 복사되어 저장되는가**(replication)**를 정할 수 있는 policy이다.

influxDB에서 **`series`**는 `measurement`, `tag set`, `field key` 값을 공유하는 **`point`**들의 집합이다. 위의 예에서는 다음과 같다.

| Series Number | Measurement | Tag Set                              | Field Key     |
| ------------- | ----------- | ------------------------------------ | ------------- |
| series 1      | `census`    | `location=1`, `scientist=langstroth` | `butterflies` |
| series 2      | `census`    | `location=2`, `scientist=langstroth` | `butterflies` |
| series 3      | `census`    | `location=1`, `scientist=perpetua`   | `butterflies` |
| series 4      | `census`    | `location=2`, `scientist=perpetua`   | `butterflies` |
| series 5      | `census`    | `location=1`, `scientist=langstroth` | `honeybees`   |
| series 6      | `census`    | `location=2`, `scientist=langstroth` | `honeybees`   |
| series 7      | `census`    | `location=1`, `scientist=perpetua`   | `honeybees`   |
| series 8      | `census`    | `location=2`, `scientist=perpetua`   | `honeybees`   |

**`point`**는 어떤 `series`에 대한 하나의 데이터 레코드를 나타낸다. 

| time                 | butterflies | honeybees | location | scientist  |
| -------------------- | ----------- | --------- | -------- | ---------- |
| 2015-08-18T00:00:00Z | 12          | 23        | 1        | langstroth |

앞서 본 모든 것들은 **`database`**에 저장된다. `database`는 다수의 사용자들과, 지속적인 쿼리문들, `retention policies`, `measurements`을 가질 수 있으며, `schemaless` database이다.

#### Features

- InfluxDB는 RDBMS의 Schema를 지원하지 않는다. 
  즉, 고정된 형태의 튜플뿐만 아니라, 새로운 유형의 포인트를 삽입할 수 있다.





기본적으로 InfluxDB 사용법은 RDBMS와 매우 유사하다. 데이터 삽입은 `insert`를 통해서, 데이터 쿼리는 `select`를 통해서 할 수 있다. 하지만 차이점은 influxDB에서는 데이터 삽입 시에 자동으로 `time` 값이 삽입된다. 물론 직접 `time` 값을 삽입할  수 있지만, 이는 influxdb에서 추천하지 않는다.

#### 데이터 삽입

데이터 삽입 명령문은 다음과 같다.

```
insert <measurement>[, <tag_key>=<tag_value>[, <tag_key>=<tag_value>, ...]] <field_key>=<field_value>[,<field_key>=<field_value>, ...] [<timestamp>]
```

#### 데이터 쿼리

데이터 쿼리는 RDBMS

## References

[1]: https://docs.influxdata.com/influxdb/v1.8/concepts/key_concepts/
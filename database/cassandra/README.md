# Cassandra

## Overview

![cassandra](data:image/jpeg;base64,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)



카산드라 데이터베이스는 자유-오픈 소스 **분산형** **NoSQL** 데이터베이스 관리 시스템 중 하나로, **단일 장애점** 없이 고성능을 제공하면서 수많은 서버 간의 대용량 데이터를 관리하기 위해 설계되었다.[[1]][1] 카산드라는 여러 데이터센터에 걸쳐 **클러스터**를 지원하며 **마스터리스(masterless) 비동기 레플리케이션**을 통해 모든 클라이언트에 대한 낮은 레이턴시 운영을 허용한다. Amazon DynamoDB의 분산 디자인과 Google Bigtable의 데이터 모델을 기반으로 설계되었다.

> **단일 장애점**
>
> 시스템 구성 요소 중에서 동작하지 않으면 전체 시스템이 중단되는 요소
>
> ![SoF](https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Single_Point_of_Failure.png/220px-Single_Point_of_Failure.png)

### Features[[2]][2]

- 확장성과 고가용성에 최적화된 분산형 데이터베이스
- Consisntent hashing을 이용한 Ring 구조와 Gossip protocol 구현으로, 각 노드 장비들의 추가 및 제거 등이 자유롭고, 데이터센터까지 고려할 수 있는 데이터 복제 정책을 사용해 안정성 측면에서 많은 장점을 가지고 있음
- 카산드라를 이용하면 Sharding을 고려할 필요 없고, Master-Slave와 같은 정책 없이도 장애에 대응할 수 있음
- 단점들도 있는데 Join이나 Transaction을 지원하지 않고, Index 검색도 매우 단출
- RDBMS 같은 Paing 구현이 힘들고, Keyspace, Table을 과도하게 생성할 시 Memory Overflow가 발생할 수 있음

### Data structure

![ds](https://image.toast.com/aaaadh/real/2016/techblog/apache1.png)

카산드라 데이터 구조는 비교적 간단한데 다음과 같다.

- 최상위 레벨에 논리적 데이터 저장소인 Keyspace

  > 기존에 database 라고 표현하기도 함

- Keyspace 아래에 형식(세로줄과 가로줄 모델)을 갖춘 데이터 구조 Table 존재

- Row가 어떻게 구성되어야 할 지에 대한 구조를 제공하는 Column

  > RDBMS에서는 속성(attribute), 필드(field)라고도 한다.
  >
  > 하지만, 필드는 필드와 필드 값은 한 열이나 한 컬럼 사이의 교차로 존재하는 단일 항목을 특정할 대 언급

- 일련의 관련 데이터인 Row

  > 기존에 레코드(Record) 또는 튜플(Tuple)이라고도 함

위와 같은 데이터 구조는 기존 RDBMS와 크게 다를 것 없으며, RDBMS를 사용해본 경험이 있다면 사용할 수 있을 것이다. 하지만 카산드라 DB의 장점은 살릴 수 없을 것이다.



### 카산드라는 어떻게 데이터를 저장할까?

![sd](https://image.toast.com/aaaadh/real/2016/techblog/apache2.png)

카산드라는 기본적으로 Ring 구조로 구성되는데, 각 Ring을 구성하는 **각 노드(A, B, …)에 데이터를 분산하여 저장**한다.

#### 데이터 분산 기준은 무엇일까?

* **Partition Key 또는 Row Key** 라고 불리는 데이터의 해시 값을 기준으로 데이터를 분산

  1. 각 노드가 Ring에 참여하면, 카산드라 `conf/cassandra.ymal`에 정의된 각 설정 값을 통해 각 노드마다 고유의 해시 값 범위를 부여 받는다.
  2. 외부에서 데이터 요청이 오면 해당 데이터 Partition Key(Row Key)의 해시 값을 계산하여 해당 데이터가 어느 노드에 저장됐는지, 되는지 확인할 수 있다.
  3. 이렇게 계산된 해시 값을 **토큰(Token)**이라 한다.

* Partition Key와 Row Key는 전자는 CQL에서 사용하는 용어이고, 후자는 카산드라 데이터 레이어 사용하는 용어

  이는 카산드라 DB의 역사를 보면 알 수 있다.

  - 처음부터 CQL(Cassandra Query Language)가 존재했던 것은 아님
  - 초기에는 Thrift Protocol을 이용한 Client API를 제공했지만, 어떤 한계들 때문에 Cassandra 1.2 이후로 CQL 문법이 추가되고, 3.0 버전부터는 아예 Deprecated 되어 사라짐
  - 이 시기에 **Super Column**이라 하는 Column 안에 Column이 있는 자료구조가 아예 스펙에서 제외되어 **Collection**이라는 것으로 새롭게 대체됨
  - 또한 기존 Column Family라고 불리는 자료구조는 **Table**로 명칭이 변경됨

### Cassandra 초창기 데이터 구조

![init ds](https://image.toast.com/aaaadh/real/2016/techblog/apache3.png)

**초창기** 카산드라 데이터 구조는 위 그림과 같으며, 다음과 같이 동작한다.

- 데이터 구조
  	[Keyspace] > [Column Family] > [Row] > [Column(Column Name + Column Value)]
- Keyspace와 Column Family에 대한 정보는 모든 카산드라 노드들의 메모리에 저장됨
- 실제 데이터들인 Row들은 각 Row Key를 가지고 계산된 해시 값(토큰)을 기준으로 각 노드에 분산 저장됨
- Row에 속하는 Column들은 Column Name을 기준으로 정렬되어 저장됨



### Cassandra 1.2 데이터 구조

![1.2 ds](https://image.toast.com/aaaadh/real/2016/techblog/apache4.png)

**Cassandra 1.2**에 들어서면서, 데이터 구조는 위 그림과 같으며, 다음과 같이 동작한다.

- 데이터 구조
  	[keyspace] > [Table] > [Row] > [Column(Column Name + Column Value) ]
- 이때 등장한 CQL은 이를 있는 그대로 표현하지 않고, 한 단계 더 추상화한다.
  ![cql ds](https://image.toast.com/aaaadh/real/2016/techblog/apache5.png)
  
  - CQL에서 Row와 Column은 RDBMS의 Tuple, Attribute와 유사함을 알 수 있음
  - 하지만 CQL에서는 반드시 최소 1개 이상의 Column을 **Primary Key**로 지정해야 함
  - **Primary Key로 지정된 Column들 중에서 Partition Key로 지정된 Column Value를 기준으로 데이터를 분산함**
  
    > 이 부분을 예제를 통해서 이해해보자!

#### 위 내용의 이해를 돕기를 위한 예제

1. 먼저 Keyspace인 `test_keyspace`에 `test_table_ex1` 이라는 **테이블 생성**해보자

   ```cql
   CREATE TABLE test_keyspace.test_table_ex1 ( 
       code text, 
       location text, 
       sequence text, 
       description text, 
       PRIMARY KEY (code, location)
   );
   ```

   - **테이블**은 각각 `code`, `location`, `sequence`, `description`이라는 **Column**을 가짐
   - Column 중 `code`, `location`을 **Primary Key**로 지정
     - Column 중 Primary Key 지정이 수행되면서, CQL 문법은 다음과 같이 동작한다.
       - 지정된 Primary Key 중에서 가장 첫 번째의 `code`는 **Partition Key(Row Key)**로 지정
       - 지정된 Primary Key 중에서 두 번째 `location`은 **Cluster Key**로 지정

2. 생성된 테이블 `test_table_ex1`에 다음과 같이 다섯 건의 데이터를 삽입해보자

   ```cql
   INSERT INTO test_keyspace.test_table_ex1 (code, location, sequence, description ) VALUES ('N1', 'Seoul', 'first', 'AA');
   INSERT INTO test_keyspace.test_table_ex1 (code, location, sequence, description ) VALUES ('N1', 'Gangnam', 'second', 'BB');
   INSERT INTO test_keyspace.test_table_ex1 (code, location, sequence, description ) VALUES ('N2', 'Seongnam', 'third', 'CC');
   INSERT INTO test_keyspace.test_table_ex1 (code, location, sequence, description ) VALUES ('N2', 'Pangyo', 'fourth', 'DD');
   INSERT INTO test_keyspace.test_table_ex1 (code, location, sequence, description ) VALUES ('N2', 'Jungja', 'fifth', 'EE');
   ```

3. 삽입된 데이터를 확인해보기 위해 다음과 같은 명령어를 입력해보자

   ```cql
   Select * from test_keyspace.test_table_ex1;
   ```

   그 결과는 다음과 같다.

   ```cql
   // RESULT IS BELOW:
   //  code | location | description | sequence
   //-------+----------+-------------+----------
   //	  N1 | Gangnam  |			BB|	  second
   //	  N1 | 	 Seoul  |			AA|	   first
   //	  N2 |  Jungja  |			EE|	   fifth
   //	  N2 |  Pangyo  |			DD|	  fourth
   //	  N2 | Seongnam |			CC|	   third
   ```

4. 이를 `bin/cassandra-cli`로 출력하면 어떻게 될까?

   ```cql
   use test_keyspace;
   list test_table_ex1;
   
   Using default limit of 100
   Using default cell limit of 100
   -------------------
   RowKey: N1
   => (name=Gangnam:, value=, timestamp=1452481808817684)
   => (name=Gangnam:description, value=4242, timestamp=1452481808817684)
   => (name=Gangnam:sequence, value=7365636f6e64, timestamp=1452481808817684)
   => (name=Seoul:, value=, timestamp=1452481808814357)
   => (name=Seoul:description, value=4141, timestamp=1452481808814357)
   => (name=Seoul:sequence, value=6669727374, timestamp=1452481808814357)
   -------------------
   RowKey: N2
   => (name=Jungja:, value=, timestamp=1452481808833644)
   => (name=Jungja:description, value=4545, timestamp=1452481808833644)
   => (name=Jungja:sequence, value=6669667468, timestamp=1452481808833644)
   => (name=Pangyo:, value=, timestamp=1452481808829751)
   => (name=Pangyo:description, value=4444, timestamp=1452481808829751)
   => (name=Pangyo:sequence, value=666f75727468, timestamp=1452481808829751)
   => (name=Seongnam:, value=, timestamp=1452481808823137)
   => (name=Seongnam:description, value=4343, timestamp=1452481808823137)
   => (name=Seongnam:sequence, value=7468697264, timestamp=1452481808823137)
   
   2 Rows Returned.
   Elapsed time: 67 ms.
   ```

   이때, 결과값으로 출력들 중 일부가 `value` 값이 없다.

   ```cql
   -------------------
   RowKey: N1
   => (name=Gangnam:, value=, timestamp=1452481808817684)
   => (name=Seoul:, value=, timestamp=1452481808814357)
   -------------------
   RowKey: N2
   => (name=Jungja:, value=, timestamp=1452481808833644)
   => (name=Pangyo:, value=, timestamp=1452481808829751)
   => (name=Seongnam:, value=, timestamp=1452481808823137)
   ```

   이들은 잘못된 데이터가 아니라, Cassandra가 CQL로부터 입력된 데이터를 내부적으로 변환하여 사용하는 데이터이므로, 이 부분을 제외해보자.

5. 이 부분을 제외하면 다음과 같다.

   ```cql
   use test_keyspace;
   list test_table_ex1;
   
   Using default limit of 100
   Using default cell limit of 100
   -------------------
   RowKey: N1
   => (name=Gangnam:description, value=4242, timestamp=1452481808817684)
   => (name=Gangnam:sequence, value=7365636f6e64, timestamp=1452481808817684)
   => (name=Seoul:description, value=4141, timestamp=1452481808814357)
   => (name=Seoul:sequence, value=6669727374, timestamp=1452481808814357)
   -------------------
   RowKey: N2
   => (name=Jungja:description, value=4545, timestamp=1452481808833644)
   => (name=Jungja:sequence, value=6669667468, timestamp=1452481808833644)
   => (name=Pangyo:description, value=4444, timestamp=1452481808829751)
   => (name=Pangyo:sequence, value=666f75727468, timestamp=1452481808829751)
   => (name=Seongnam:description, value=4343, timestamp=1452481808823137)
   => (name=Seongnam:sequence, value=7468697264, timestamp=1452481808823137)
   
   2 Rows Returned.
   Elapsed time: 67 ms.
   ```

   위 결과 값을 분석해보자

   - Primary Key 중 첫 번째 Column인 `code`는 **RowKey**로 지정
   - Primary Key 중 두 번째 Column인 `location`은 **Column Name**인 **ClusyerKey**로 지정
   - Primary Key로 입력하지 않은 Column들의 **Name은 ClusterKey와 조합되어 표현**
     - `(ClusterKey:ColumnKey, value=)`
     - Primary Key로 입력하지 않은 Column Value들은 byte로 변환되어 저장되므로, 문자열을 정수로 표현함

### Virtual Node

앞서 살펴본 내용들은 카산드라가 어떻게 데이터를 분산하는 지를 정리했는데 복기해보면 다음과 같다.

1. 사용자가 카산드라 데이터베이스 데이터를 **CRUD** 수행

   > CRUD(Create;Read;Update;Delete)

2. 이때, 해당 데이터에서 **Partition Key**로 지정된 Column들의 Value들의 조합이 **Row Key**가 됨

3. 조합된 Row Key을 해싱을 수행하여 토큰을 계산한 뒤, 해당 토큰의 범위에 속한 노드를 찾아 CRUD를 수행

다음과 같이 수행하려면 무엇보다도 먼저, 각 노드별 토큰 범위가 할당되어 있어야 한다.

#### 초창기 카산드라

![vn ring](https://image.toast.com/aaaadh/real/2016/techblog/apache7.png)

먼저 그림을 통해서 살펴보자.

카산드라는 Ring 구조를 이루고 있으며, 각 노드는 연속한 3 개의 토큰 범위에 대한 저장 의무를 가진다. 초창기에는 직접 수작업이나 스크립트를 이용해 해시 값의 범위를 구해 카산드라의 각 노드의 `conf/cassandra.yaml`에 `initial_token`이라는 옵션에 해당 해시 값을 지정해줘야 했다. 즉, 카산드라 구동 시 `initial_token`에 지정된 값을 읽어 자신이 담당하는 해시 값을 계산했다. 이때 만약 특정 노드를 추가, 제거해야 할 때는 특정 노드에 데이터가 몰리지 않도록 수작업으로 `initial_token`을 다시 계산하여 `conf/cassandra.yaml`을 갱신한 뒤 카산드라를 재구동했다. 그리고 `bin/nodetool` 유틸리티의 `move`, `remove`, `decommission`, `cleanup`과 같은 명령어를 통해 수작업으로 기존 데이터를 리밸런싱 했다.

#### Cassandra 1.2 

![1.2 vn](https://image.toast.com/aaaadh/real/2016/techblog/apache8.png)

앞선 버전에서의 노드 추가와 제거를 위해서는 수작업으로 해야했던 것에 비해, 카산드라 1.2 버전에는 `virtual node`라는 기능이 추가됐다. `virtual node`는 하나의 실제 카산드라 노드 안에 여러 대의 가상 노드를 두고, 아주 잘게 나눠진 토큰 범위를 가상 노드들에게 할당하여 데이터를 분산한다는 개념이다. `virtual node`의 이점은 다수의 가상 노드들을 통하여 좀 더 데이터를  균일하게 분산하기 쉽고, 데이터가 이미 여러 대의 노드에 분산되어 있으므로 노드 추가, 제거시 데이터 이동, 복제, 리밸런싱에 높은 성능 향상을 가져다 준다. 따라서 하나의 노드에 몇 대의 가상 노드를 운영할 것인지에 대한 옵션이 바로 `conf/cassandra.yaml`의 `num_tokens` 항목이다. 이렇게 `virtual node`를 사용할 경우, 노드 추가, 제거 시 매번 수작업으로 토큰을 생성하여 옵션에 넣어줄 필요 없이, 링에 속한 모든 노드들이 알아서 `gossip protocol`을 통해 의논하여 토큰 범위를 결정하고 리밸런싱까지 처리해준다.



## CQL, Cassandra Query Language

### keyspace

키스페이스는 카산드라 데이터베이스 오브젝트의 논리적인 집합인데, 데이터베이스 오브젝트는 다음과 같다.

- 테이블
- 사용자 정의 타입
- 사용자 정의 함수
- 기타 등등

또한 이는 RDBMS의 데이터베이스 또는 네임스페이스 개념과 유사하며, 그 키스페이스에 저장된 모든 데이터의 replication behavior를 제어한다.

```cql
// 키스페이스 생성
CREATE KEYSPACE demo WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

// 키스페이스 리스트 확인
DESCRIBE KEYSPACES;

// demo 키스페이스에 테이블 생성
CRAETE TABLE demo.users (
	lastname text PRIMARY KEY,
    firstname text
    email text
)

// demo 사용
USE demo;

// 예제 생성
INSERT INTO users (lastname, firstname, email) VALUES ('Round', 'Craig', 'craig@example.com');
cqlsh:demo> INSERT INTO users (lastname, firstname, email) VALUES ('Pratico', 'Cassi', 'cassi@example.com');
cqlsh:demo> INSERT INTO users (lastname, firstname, email) VALUES ('Polson', 'Lino', 'lino@example.com');

// 직접 입력하지 않고, csv 파일이 있다면 다음과 같이 수행할 수 있다.
COPY demo.users (lastname, firstname, email) FROM '~/users.csv' WITH HEADER = TRUE;

// 데이터 읽는법
SELECT * FROM users;

// 특정 데이터를 읽어보자
SELECT * FROM users WHERE lastname = 'Polson';

// 특정 데이터를 업데이트 해보자
UPDATE users SET email = 'lpolson@example.com' WHERE lastname = 'Polson';

// 특정 데이터를 삭제해보자
DELETE FROM users WHERE lastname='Polson';
```

## References

[1]: https://ko.wikipedia.org/wiki/%EC%95%84%ED%8C%8C%EC%B9%98_%EC%B9%B4%EC%82%B0%EB%93%9C%EB%9D%BC
[2]: https://meetup.toast.com/posts/5
# Performance analysis of cloud application

## Topic

끊임없이 바뀌는 로드가 계속해서 어플리케이션의 성능 특성을 변화시키기 때문에, 리소스 사용량과 지연속도를 이해하고 개선하는 것이 어려운 것을 보여줌

Q. 어떤 요인으로 인해서 끊임없이 로드가 바뀌는가 ?

Q. 성능 특성이 무엇인가?



## 1. Introduction

1. 대규모 클라우드 어플리케이션에서의 성능 문제는 상당히 중요

   - latency: 사용자 만족도 및 사용률에 영향
   - resource usage: 회사의 비용에 영향

2.  이전 연구(Facebook, Kraken)에서 QPS로 측정되는 user base 변화에 따라 클라우드 어플리케이션의 로드가 변한다고 보여줌.
   따라서 이 QPS를 이용하여 성능 분석과 개선을 하였음

3. 하지만 실제로 자신들의 클라우드 어플리케이션 Gmail을 분석해 본 결과, load는 QPS 변화보다는 **load mixture** 변화에 의해 영향을 크게 받음을 알게 됨

   **Q. load mixture가 무엇인가?**

   load는 두 가지가 존재

   - 사용자에 의해 발생되는 load
   - 시스템에 의해 발생되는 load

   여기서 사용자에 의해 발생되는 load mixture를 보면,

   > 어떤 사용자의 메일박스가 다른 사용자 보다 네 배 더 큰 규모를 가지고 있으면, 이에 대한 운용 비용은 기본적으로 적은 것보다 훨씬 비쌈
   >
   > (메일박스에 250개를 가지고 있는 유저, 메일박스에 1000개의 메일을 가지고 있는 유저)
   >
   > > **내 생각**
   > >
   > > load mixture의 종류에는
   > >
   > > 1. 동일한 종류의 request를 처리하는데 있어 load
   > > 2. 다른 종류의 request를 처리하는데 있어 load
   > >
   > > 이 둘 중에서 load mixture가 정확하게 의미하는 바는 1인가 2인가?
   > > A. 2번 다양한 종류의 request

4. 계속해서 바뀌는 load mixture는 성능 분석에 있어서 두 가지 암시를 가짐

   1. 코드 변화에 따른 성능에 대한 영향을 판단하기 위해서는 우리들은 반드시 많은 시점으로부터 데이터를 수집하고 분석.

      > 어느 한 시점에서는 우리들에게 오직 하나의 mixture of load에 대한 데이터만 줌

   2. 성능 문제를 재현하기 위해서는 우선 성능 문제를 발생시키는 combinations of load(load mixture)를 재현

      > 우리들은 이를 synthetics test를 통해서 이를 해볼 수 있지만, 때때로 우리들은 실제 사용자에게 제공하는 시   스템의 데이터를 수집하고 분석할 필요가 있음

5.  실제 사용자에게 제공하는 시스템에서 실험하는 것은 두 가지 이유로 어려움

   1.  우리들은 실제 사용자가 생성하는 load를 통제하지 못함.
      따라서, 통계학적으로 중요한 결과를 얻기 위해 **무작위의 수천만 사용자에게 제공하는 시스템에서 실험**

      > **내 생각**
      >
      > 왜 실제 사용자가 생성하는 load를 통제하지 못할까?

   2. 본질적으로 위험(하나의 실수가 사용자에게 부정적인 영향을 끼칠 수 있음).
      따라서, 실제 실험을 수행하기 전에 실험의 가능한 결과를 예측하기 위해 **통계** 사용

   이게 항상 옳은 것은 아님: 때때로 그 데이터 분포가 명백하지 않다

6. 실제 사용자에게 제공하는 시스템에서 좋은 성능 데이터를 수집하기 위해서 우리들은 두 가지 테크닉을 개발

   1. ***Coordinated bursty tracing***

      - 명시적인 조정 없이 모든 소프트웨어 계층에 걸쳐 coordinated bursts of traces를 수집

        > 전통적인 샘플링 또는 버스티에 대한 접근은 카운터를 두거나[[1]](https://dl.acm.org/doi/abs/10.1145/583854.582432)[[2]](http://hirzels.com/martin/p apers/fddo01-bursty-tracing.pdf) , 
        >
        > 샘플링 결정 전파[[3]](https://dl.acm.org/doi/abs/10.1145/3132747.3132749)[[4]](https://research.google/pubs/pub36356/)에 의존하는 반면, 
        >
        > 이는 burst의 시작과 끝을 조정하기 위해 시간을 사용

      - 모든 계층은 동시에 burst를 수집하기 때문에, 단일 계층이 아닌 전체 어플리케이션 스택에 걸쳐 추론할 수 있음

      - 많은 버스트를 수집함으로써, 우리들은 성능 조사로부터 유효한 결론을 도출할 수 있는 load mixture에 대한 무작위 샘플을 얻음

      > Q. **소프트웨어 계층**은 어떤 것이 있는가?
      >
      > Q. **coordinated bursts of traces**가 무엇인가?
      >
      > Q. burstiness
      >
      > > [[wikipedia]](https://en.wikipedia.org/wiki/Burstiness)
      > >
      > > In [statistics](https://en.wikipedia.org/wiki/Statistics), **burstiness** is the intermittent increases and decreases in activity or [frequency](https://en.wikipedia.org/wiki/Frequency) of an event.[[1\]](https://en.wikipedia.org/wiki/Burstiness#cite_note-Lambiotte-1)[[2\]](https://en.wikipedia.org/wiki/Burstiness#cite_note-2) One of measures of burstiness is the [Fano factor](https://en.wikipedia.org/wiki/Fano_factor)—a ratio between the [variance](https://en.wikipedia.org/wiki/Variance) and [mean](https://en.wikipedia.org/wiki/Mean) of counts.
      > >
      > > Burstiness is observable in natural phenomena, such as [natural disasters](https://en.wikipedia.org/wiki/Natural_disaster), or other phenomena, such as [network](https://en.wikipedia.org/wiki/Computer_network)/[data](https://en.wikipedia.org/wiki/Data)/[email](https://en.wikipedia.org/wiki/Email) network traffic[[3\]](https://en.wikipedia.org/wiki/Burstiness#cite_note-3)[[4\]](https://en.wikipedia.org/wiki/Burstiness#cite_note-4) or [vehicular traffic](https://en.wikipedia.org/wiki/Traffic_flow).[[5\]](https://en.wikipedia.org/wiki/Burstiness#cite_note-5) Burstiness is, in part, due to changes in the [probability distribution](https://en.wikipedia.org/wiki/Probability_distribution) of inter-event times.[[6\]](https://en.wikipedia.org/wiki/Burstiness#cite_note-6) Distributions of bursty processes or events are characterised by [heavy, or fat, tails](https://en.wikipedia.org/wiki/Fat-tailed_distribution).[[1\]](https://en.wikipedia.org/wiki/Burstiness#cite_note-Lambiotte-1)
      > >
      > > Burstiness of inter-contact time between nodes in a [time-varying network](https://en.wikipedia.org/wiki/Time-varying_network) can decidedly slow spreading processes over the network. This is of great interest for studying the spread of information and disease. [[7]](https://en.wikipedia.org/wiki/Burstiness#cite_note-7)

   2. ***Vertical context injection***

      - 소프트웨어 계층 간 상호작용은 많은 성능 문제를 일으키기 때문에, 우리들은 한 계층에서의 trace event를 다른 계층에서의 event와 연결 할 수 있어야함

        > Q. 왜 소프트웨어 **계층 간 상호작용**은 성능 문제를 야기할까?
        >
        > Q. **성능 문제**는 어떤 종류가 있을까?

      - Vertical context injection은 관련 고수준 이벤트에 대한 무해한 시스템 콜 순서를 양식화 함으로써 해결

        > Q. 무해한 시스템 콜?
        >
        > ​	영향을 끼치지 않는다는 말인가?

      - 이러한 시스템 콜들은 커널 트레이스에 시스템 호출 이벤트를 삽입하고, 커널 트레이스는 우리가 분석하여 상위 레벨 이벤트와 하위 레벨 이벤트를 모두 인터리빙하는 트레이스를 생성

      - 이전 연구[[4]](https://research.google/pubs/pub36356/)[[5]](https://www.usenix.org/conference/nsdi-07/x-trace-pervasive-network-tracing-framework)와 달리, 우리들은 소프트웨어 스택 계층에 trace context의 전파를 필요로 하지 않음

      위 두 테크닉을 Gmail, Google Driver 등 많은 Google application에 이용

   

## 2. Our challenge: constantly varying load

- 클라우드 어플리케이션의 성능 분석에 있어 주요 어려운 점들은 끊임없이 바뀌는 load 때문

  <img src="/home/dohan/Pictures/PACA/figure1.png" alt="figure1" style="zoom: 67%;" />

- 논문에서의 그래프는 일주일(6 Aug ~ 13 Aug) 간 시간마다 또는 날마다 변하는 변수 값을 보여줌

- 여기서 Scale은 QPS뿐만 아니라 다른 response size per request 등 다양한 변수에 대해 scaled constant*(정확한 수치는 Google 소유의 정보이므로 공개하지 않음)*

- 위의 그래프에서는 QPS의 변동(실제 사용자는 오후에 많음)을 예상할 수 있지만, mix of request이 크게 변동된 것으로 예상하지 않음

  > while one expects fluctuation in QPS, one does not expect the mix of requests to fluctuate significantly.
  >
  > Q. mix of request가 무슨 말인가?
  >
  > 1. 하나의 request가 많음
  > 2. 다양한 request가 섞임

  <img src="/home/dohan/Pictures/PACA/figure2.png" alt="figure2" style="zoom:67%;" />

- 이 그래프는 ruquest(query)의 한 특성인, 요청당 응답 크기가 일주일 동안 시간에 따라 변화한다는 것을 보여주며, 
  앞서 보여준 그래프에서 시간에 따른 초당 쿼리 수의 변화와 같이 query의 특성들이 시간에 따라 지속적으로 변화함을 보여줌

  > request는 query
  >
  > query는 다양한 특성들을 가질 수 있음:
  >
  > 1. number of query
  >
  > 2. query size
  >
  > 3. response size
  >
  >    ​	...



### 2.1 Variations in rate and mix of user visible requests(UVR)

<img src="/home/dohan/Pictures/PACA/figure3.png" alt="figure3" style="zoom:67%;" />

- 위의 그래프는 동일한 기간 동안 UVR의 QPS와 response size의 변화를 보여줌

- **UVR**은 아래와 같은 request:

  - 사용자가 발생시키는 request(clicking on a message)
  - 사용자 클라이언트가 발생시키는 백그라운드 request(background sync by IMAP client)
  - 메시지 전송

-  figure1과 달리 figure3에서는 ***QPS curve***가 좀 더 사이클 패턴에 가까움

  - 12시 이전, 이후에 가장 높은 QPS, 그 이전과 이후에 오르고, 떨어짐을 볼 수 있ᅌᅳᆷ
  - 주말보다 주중에 더 높은 QPS

-  figure2과 달리 figure3에서는 ***byte per response curve***도 좀 더 평평함

  - figure3에서는 최대/최소 값이 20% 차이
  - figure2에서는 최대/최소 값이 100% 차이

- 왜 그런가?

  1. 메일 전송(smaller response size)과 사용자 활동(larger)의 혼합(mix)은 하루에 걸쳐 바뀌고, 이는 the average response size per request에 영향

     > - 메일 전송과 사용자 활동의 차이는 무엇인가?
     >
     > - 왜 메일 전송이 더 작은 응답 크기를 가질까?

     - 많은 bulk mail sender는 매일 특정 시간에 대량의 email을 보내고, 그 시간은 반드시 interactive user의 활동과 상관관계가 있는 것이 아님

  2. 사용자의 interactive / sync request의 혼합(mix)는 하루에 걸쳐 바뀜

     <img src="/home/dohan/Pictures/PACA/figure4.png" alt="figure4" style="zoom:67%;" />

     * 위 그래프는 IMAP request에 대한 Web client request의 scaled ratio 대한 그래프

     - IMAP request

       - Synchronization request

         > give me all messages in this folder

     - Web client request

       - interactive request

         > user clicks on a message

       - prefetch request

     - 따라서, 보통 IMAP request는 interactive request보다 훨씬 더 큰 response size를 가짐

     - IMAP request는 email client를 어떤 것을 쓰냐에 따라서 달라짐

       > 예를 들어, 
       >
       > 한 사용자는 Gmail application만 이용할 수 있고,
       > 또 다른 사용자는 IMAP-based email application(Blue mail, Naver mail, Thunderbird, ..)을 이용할 수 있음

     

### 2.2 Variations in rate and mix of essential non-UVR work

* UVR request 외에 필수적인 non-UVR work:
  * Continuous validation of data

    - 시스템의 거대한 규모 때문에, 어떤 종류의 실패가 발생할 수 있음
      소프트웨어 실패 뿐만 아니라, 하드웨어 실패까지 직면할 수 있음
    - 이로 인해, 전반적인 데이터의 변질이 발생할 수 있고, 이를 위한 지속적인 검증이 필요

  * Software updates

    - 시스템은 많은 서로 상호작용하는 구성요소로 이루어지고, 이런 필요에 따라 구성요소들은 업데이트 주기를 가짐
    - 모든 구성요소의 엡데이트를 조정하는 것은 비현실적이고, 바람직하지 않다. 따라서, 조정 없이 필요할 때 구성요소를 업데이트할 수 있어야 함
    - Dynamic software updating보다는 간단한 방법을 취하는데, ᅂᅩᆼ시에 몇 개의 프로세스를 재시작함으로써 소프트웨어를 업데이트 함;
      이를 위해 시스템은 자동으로 사용자들을 업데이트 될 서버에서 다른 서버로 옮기므로 서비스가 중단되지 않음

  * Repairs

    - 하드웨어와 소프트웨어 버그는 언제든 발생할 수 있음

      > 예를 들어,
      >
      > 메세지 토큰나이저가 어떤 메세지의 이메일 주소를 토큰화를 정확하지 않게 한다면, 사용자는 그 영향받은 이메일 주소를 사용하지 못할 수 있ᅌᅳᆷ

    - 시스템 규모 때문에 그런 FIX는 몇 주 또는 그 이상 걸릴 수 있고, 그에 따라 load가 부하됨

  * Data management

    - Gmail은 Bigtable를 기본으로 사용하는데, 이는 key-value pair 스택을 유지하고, 주기적으로 각

<img src="/home/dohan/Pictures/PACA/figure5.png" alt="figure5" style="zoom:67%;" />

* 위 그래프는 Non-UVR 또한 계속해서 바뀌는 것을 보여주고, 가능한 UVR이 낮을 때 Non-UVR을 수행하려고 함
  - 이는 사용자에 대한 영향을 최소화하고, UVR을 위해 예약된 리소스를 사용할 수 있기 때문
* 위 그래프를 분석하자면, 대략 UVR이 전체 CPU 사용량의 20%, Non-UVR 전체 사용량의 80%를 차지하는 것을 알 수 있음
  * 따라서 UVR과 Non-UVR을 따로따로 성능 분석하는 것은 부적절함

### 2.3 Variation due to one-off events

- **one-off event**란 예상치 못한 일에서 발생:

  - 하드웨어 또는 소프트웨어 중단

  - 즉시 수행되어야 하는 작업

    >  한 데이터센터의 데이터가 다른 데이터센터로 전송해야 하는 경우가 발생

<img src="/home/dohan/Pictures/PACA/figure6.png" alt="figure6" style="zoom:67%;" />

-  Lightning struck Google's Belgian datacenter four times and potentially caused corruption in some disks
  예기치 못한 이벤트 발생으로 데이터 변질 발생할 수 있고, 이에 대한 조치가 필요

  1. 그 데이터센터의 모든 데이터를 DROP
  2. 다른 데이터센터의 변질되지 않은 데이터로부터 재 구성

  조치로 인해, 이벤트에 영향받지 않은 데이터 센터의 CPU 사용량이 증가

- one-off event는 최적화하여 상호작용할 수 있ᅌᅳᆷ

### 2.4 Variation in load makes it difficult to use a synthetic environment

<img src="/home/dohan/Pictures/PACA/figure8.png" alt="figure8" style="zoom:67%;" />

- 위 세 가지 요인들을 합성하면 종종 complex distribution with a long-tail이 나옴
-  이 경우에는 synthetic test를 하는데, 이는 사용자와는 계측기를 추가하고, 코드 로직을 변경하고, 필요에 따라 재실행시킬 수 있음.
  따라서 빠르게 할 수 있고, 성공한다면 이를 쉽게 단순화 시킬 수 있음
-  하지만, 실제 사용자에게 위와 같은 실험을 한다면 실험이 사용자 데이터를 손상시킬 수 있음.
  따라서, 코드 리뷰, 테스트, 점진적으로 실험을 해야하기 때문에 synthetic test보다 훨씬 느릴수 밖에 없음

- 주의깊은 모델링에도 불구하고, 테스트 환경에서의 latency distribution과 실제 사용자들의 latency distribution이 다름

  > 왜?
  >
  > 1. 연속적으로 변화하는 load를 어떤 synthetic environment에서도 모델링하기 어려움
  > 2. 대형 분산 시스템은 시스템과 사용자에 대한 경험적 관찰에 기초한 많은 최적화를 통합

-  그렇지만, synthetic environment는 많은 심각한 성능 비효율성을 디버깅하는데 있어 중요 
  이는 직접적으로는 사용하지는 못하지만, 그 관계성에 있어서는 종종 유용

-  반드시 실제 사용자에게 제공하는 시스템에서 실험을 해봐야 함

### 2.5 Effect of continuously-varying load

- 계속해서 바뀌는 load mixtures는 리소스 사용량과 지연시간 둘다에 영향을 줌

<img src="/home/dohan/Pictures/PACA/figure9.png" alt="figure9" style="zoom:67%;" />

- 위 그래프를 보면, QPS와 latency의 관계가 명백하지 않음을 보여줌



## 3. Our approach

- Synthetic environments에서 쉽게 성능 현상들을 재현할 수 없기 때문에, 대부분의 실험들을 실제 사용자들에 수행
- 3.1절에서는 어떻게 우리가 이것을 하는지 설명
- 3.2절에서는 어떻게 성공적으로 통계를 사용하여 실험의 결과와 우리가 부딪치는 함정을 예측할 수 있는지를 설명
- 3.3절에서는 지속적으로 변화하는 load 시스템에서 저속 또는 리소스 집약적인 운영의 원인을 디버깅해야 하는 두 가지 상황 설명

### 3.1 Running experiments in a live serving system

- 계속해서 바뀌는 로드로 인해 실제 사용자에게 제공하는 시스템에서 실험해야 하는 경우가 있음

-  하나의 데이터센터에 대한 사용자들을 무작위로 선택해 두 개의 파티션으로 나누고, 하나는 테스트 파티션 다른 하나는 통제 파티션으로 나눔
  또한 각 파티션은 동일하면서 독립적인 프로세스 셋을 이용(한 데이터센터의 모든 프로세스를 하나 더 만들어 할당함). 
  또한 각 프로세스는 동일한 숫자의 무작위로 선정된 사용자에게 서비스를 제공

  *과학 실험과 같이 일정하게 유지시키는 통제 변인과, 어떤 실험을 가하는 독립(조작) 변인으로 나눔*

- 두 파티션의 샘플의 차이점을 없애기 위해 많은 수의 법칙들을 적용(따로 나오지 않음)

<img src="/home/dohan/Pictures/PACA/figure10.png" alt="figure10" style="zoom:67%;" />

- 위 그래프는 아직 실험이 진행되지 않은 상태에서의 latency를 보여줌
- 이 때, 각 파티션에 대한 프로세스들의 latency 차이가 발생하는 이유는 sampling의 수에 따른 차이인데, 이는 Gmail의 운용비용 특성때문이다. 99% pecentile 사용자는 median보다 4배 이상 더 큰 메일박스를 가지고 있고 이에 따라, 운용 비용이 훨씬 더 큼. 샘플링 수가 적으면, 사용자에 대한 분배가 적절치 않기 때문에, 샘플링 수를 늘림으로써 이를 해결할 수 있ᅌᅳᆷ

### 3.2 Using statistics to determine the impact of a change

- 변경사항은 부하에 따라 시스템 성능에 다르게 영향을 줄 수 있기 때문에
  - 거대한 샘플로부터 성능 데이터를 수집
  - 한 주를 걸쳐 성능 데이터를 수집하되, 휴가 시즌에 대해서는 데이터를 무시.
  - one-off event를 발생시켜 데이터를 수집
  - 테스트 파티션을 통제 파티션과 동일한 시간에 비교하고, 비교를 부적절하게 만드는 다른 요인이 없음을 보장(one-off hevent, 이전 실험의 영향)
-  위와 같이 데이터를 수집하고 분석을 위해 통계학적인 방법을 사용할 수 있지만, 많은 방법들은 분석을 위해 데이터 분포 또는 데이터 독립성 등을 가정하기 때문에 항상 명백하게 나타나는 것은 아님. 
  

#### 3.2.1 Example 1: Data is near normal

#### 3.2.2 Example 2: Data is near normal but not independent

### 3.3 Temporal and operation context

-  클라우드 어플리케이션의 latency 또는 resource usage를 효율적으로 만들기 위해서는 두 가지 context를 고려해야 함
  1. Temporal context
     - 클라우드 어플리케이션은 계속해서 부하가 바꾸기 때문에 이를 고려해야 함
     - Temporal context는 request가 처리되고 완료하는 시간 동안에 공존하는 모든 활동(관련없는 활동도 포함)
     -  관련없는 활동은 request 처리 성능을 악화(cache eviction)시킬 수 있지만, 
       각 프로세스는 같은 컴퓨터에서 컨테이너 환경으로 분리되어 실행되기 때문에 거의 발생하지 않는다.
     - 따라서 request 처리하는데 관련있는 프로세스의 Temporal context에만 관심이 있음
  2. Operation context
     - 클라우드 어플리케이션의 단일 request는 다른 컴퓨터에서 실행되는 많은 프로세스들이 포함될 수 있음
     - 이에 더해 각 프로세스는 많은 소프트웨어 계층에서 바이너리를 실행하며, 종종 독립적인 팀에 의해 개발됨
     - 한 request는 아래와 같은 것들을 포함할 수 있음
       - 프로세스 사이에 RPC
       - 사용자-수준 소프트웨어 계층 사이에 functional call
       - user-level와 kenel 사이에 system call
     - 따라서, request는 느릴 수 있음
       - 특정 호출은 지나치게 느릴 수 있음
       - 특정 호출의 argument는 느려지는 것을 야기시킬 수 있ᅌᅳᆷ
       - 각각의 호출은 빠르지만, 지나치게 많은 다른 request가 추가될 수 있음
     - 한 request에 대한 관련된 call들의 정보들을 포함하고 있기 때문에 이를 operation context라 함



- 클라우드 어플리케이션의 latency 또는 resource usage를 효율적으로 만들기 위해서는 두 가지 context를 고려해야 함
  1.  Temporal Context
     - Request를 완료하는 동안에 request를 처리하는 데 관련되어 있고 공존하는 모든 활동
  2.  Operation Context
     - 하나의 request는 다른 컴퓨터에서 실행되는 많은 프로세스들과 연관 될 수 있고, 각 프로세스는 많은 소프트웨어 계층에서 바이너리를 실행할 수 있음
     - 즉, 하나의 request는 다른 프로세스 간의 RPC, user-level 소프트웨어 계층 간의 Functional Call, 커널과 user-level 사이의 System call들을 포함
     - 따라서 request는 아래가 원인이 되어 느릴 수 있ᅌᅳᆷ
       - 특정 call이 느림
       - 특정 call에 대한 argument가 느리게 만듬
       - 각 call들은 빠르나 지나치게 많은 수가 느리게 함
     - 어떤 request를 구성하고 있는 call들로 이루어진 full tree를 만들 수 있음. 이를 Operation Context라 부름
- 위와 같은 두 개의 Context를 이용하여, 어떤 request에 대해 최적화를 수행할 수 있음

#### 3.3.1 Coordinated bursty tracing

- 이런 Context에 대한 정보를 얻기 위해서 Coordinated Bursty Tracing을 함

- Burst의 시작과 끝을 결정하기 위해 wall-clock time을 사용하는 coordinated bursty tracing을 사용

- coordinated을 통해 사용자 요청 서비스에 참여한 모든 컴퓨터와 모든 계층(프로세스)에서 동시에 추적을 수집할 수 있다는 것을 의미

- burst는 인접한 시간 간격이기 때문에, 우리들은 이러한 trace들을 operation context로 만들 수 있음

- burst-tracing을  64비트 부호없는 정수로 burst-config 설정하는데, burst-config는 지속 기간(duration)과 버스트 간격(period)를 정함

  (1)^m^(0)^n^ (base 2), 2^(m+n)^ ms 마다  2^n^ 만큼 tracing 함

* 이렇게 일정 기간 동안 많은 버스트를 수집하여 전체 그림을 얻을 수 있음
* 즉 적절한 burst-config를 선택하면 시간이 지남에 따라 분산되어 여러 가지 load와 load mixe에 걸쳐 분산될 수 있음
* 이에 대한 5가지 challenges가 있음:
  1. 다른 컴퓨터에 걸친 clock들이 잘 조정되어 있음을 가정
  2.  request에 관련된 모든 프로세스에 대해 coordinated bursty tracing을 확인하고 허용해야 함, 그렇지 않으면 부적절한 operation context를 얻을 수 있음.  
     이는 사용자들을 두 개의 파티션으로 나누고, 파티션의 프로세스들은 동일한 파티션의 프로세스들만 의사소통할 수 있기 때문에, 점진적으로 프로세스들의 셋을 확인할 수 있음
  3. CBT는 시간을 기반으로 하기 때문에, request 중간에 시작되거나 끝날 수 있음. 이를 위해 burst period를 최소 10배에 해당하는 버스트 기간을 선택
  4. 주어진 버스트에 실제로 관심 이벤트가 포함될 수도 없을 수도 있어 이를 알아내야 함. 
  5. CBT와 어떤 Tracing도 시스템 행동에 작은 변화를 줄 수 있음. 만약 충분히 심하다면, 그런 작은 변화는 성능 분석을 잘못 이끌 수 있음. 이는 우리가 수집하는 trace에 달려 있는데, 이는 서로 다른 계층에 대한 추적은 비용이 매우 다르기 때문에, 수량화할 수 없음. 아직 그런 상황을 겪지도 않았음.

#### 3.3.2 Vertical context injection

- 버스트에는 다른 계층의 트레이스가 포함되기 때문에 하나의 트레이스에 있는 이벤트와 다른 트레이스에 있는 이벤트를 연결할 필요가 있음
- 좀 더 구체적으로 말하자면, 모든 trace들로부터 지식을 결합한 전체적인 trace를 얻길 원함
- 

## Graph

- Target: Gmail

- Y-Axis

   Value axis, thousands of processes serving tens of millions

- X-Axis
   Time axis over the course of a week starting on Sunday, time in US Pacific time

- Purpose
  see that load on our system changes continuously: from day to day and from hour to hour by more than a factor of two



## Terminologies

- **[codebase](https://en.wikipedia.org/wiki/Codebase)**
  **codebase** (or **code base**) is a collection of [source code](https://en.wikipedia.org/wiki/Source_code) used to [build](https://en.wikipedia.org/wiki/Software_build) a particular [software system](https://en.wikipedia.org/wiki/Software_system), [application](https://en.wikipedia.org/wiki/Application_software), or [software component](https://en.wikipedia.org/wiki/Software_componentry).
  Typically, a codebase includes only human-written [source code](https://en.wikipedia.org/wiki/Source_code) files; thus, a codebase usually does not include source code files generated by tools (generated files) or binary library files (object files), as they can be built from the human-written source code. However, it generally does include configuration and property files, as they are the data necessary for the build.

  - monolithic codebase
    - google
    - facebook
  - distributed codebase
    - linux kernel

- **RPC(Remote Process Call)**

  [RPC](https://nesoy.github.io/articles/2019-07/RPC) 

  **질문**

  1. RPC는 무엇인가?
  2. RPC의 장단점
  3. RPC는 어떤 경우에 이용하면 될까?

-  **Synthetic Test**

  a method of understanding a user’s experience of your application by predicting behavior

  행동 예측을 통해 어플리케이션 사용자 경험을 이해하는 방법

- **load mixture**

- performance characteristics**
  - static characteristics
  - dynamic characteristics



## Comparing

* [Kraken](https://www.usenix.org/system/files/conference/osdi16/osdi16-veeraraghavan.pdf)

  Facebook analysis









## Background

-  유명한 클라우드 어플리케이션은 수 만개의 RPC requests와 거대한 코드베이스로 이루어진 대규모 분산 시스템
  Example) 구글, 페이스북, ...
-  거대한 규모로 때문에 실용적인 데이터 없이 성능 최적화는 비효율적이기 쉬움
  이미 복잡한 시스템에 아무런 이익 없이 복잡도를 추가할 수 있음
  - **왜 복잡도가 추가될까?** 
  - **성능 최적화를 했는데 왜 아무런 이익이 없을까?**



## Problem

- Gmail(10억 명의 실질적인 유저를 가지고 있는 어플리케이션)을 위한 실용적인 데이터를 수집할 때 있는 어려움, 도전들을 설명
- Gmail로 생산되는 데이터를 이용하여 로드와 로드의 특성은 지속적으로 변함을 보여줌
- **로드와 지속적인 로드 변화** 때문에 Gmail 성능을 synthetic test로 모델링하기 어렵고, 생산 데이터 분석을 하기도 어렵다
- 실용적인 데이터 수집을 위한 두 가지 기술 소개:
  -  Coordinated Bursty Tracing  
    Gmail stack의 모든 레이어에 대한 동시다발적인 폭발적인 이벤트 증가에 대한 포착 수헹
  -  Vertical Context Injection
    holistic trace를 통해 high-level 이벤트를 low-level event와 결합하여, 우리들의 소프트웨어 스택에 이에 대한 정보를 명시적 전파하는 것을 요하지 않음



## Introduction

-  거대한 규모의 클라우드 어플리케이션은 수십억 명의 실질 유저가 있어서, 이들의 성능은 매우 중요

  - latency는 사용자 만족도와 참여율에 영향을 끼치고
  - resource usage는 그 어플리케이션 운용 비용을 결정

   **Questions**

  클라우드 어플리케이션 성능은 어떤 것이 있나?

- 지연속도와 리소스 사용량의 이해와 개선은 끊임없이 바뀌는 부하(load)가 이 어플리케이션의 성능 특성을 지속적으로 변화시키기 때문에 어려움

-  이전에는 사용자 기반 변화 때문에 클라우드 어플리케이션 부하가 바뀐다고 했지만[[Kraken]](https://www.usenix.org/system/files/conference/osdi16/osdi16-veeraraghavan.pdf), 
  여기서는 성능 분석에서 가장 큰 어려운 점은 QPS(Query Per Second) 변화 때문이 아니라 load mixture 변화 때문이라는 것을 Gmail을 통해 보여줌

- 클라우드 어플리케이션 부하는 지속적으로 변하는 사용자와 시스템에 의해 생성되는 다양한 부하의 혼합물임

-  비록 우리들은 사용자에 의해 발생하는 부하에 대해서만 고려하지만, 다른 사용자들에 의해 발생되는 부하에 잇어서 중요한 변화임
  example) 어떤 사용자 메일박스는 다른 사용자보다 훨씬 더 거대한 네 자리 수이고, 이에 대한 Operation은 작은 메일 박스보다 기본적으로 더 비쌀 것임

- 이런 시간에 의해 바뀌는 mixture of load는 성능 분석에 있어서 두 가지 암시를 가짐:

  1.  코드 변경이 성능에 미치는 영향을 판단하기 위해서, 많은 시점의 데이터를 수집하고 분석해야 함;
     어떠한 단일 시점에서는 하나의 mixture of load에 대한 데이터를 제공
  2.  성능 문제를 재현하기 위해서는 우선 성능 문제를 초래하는 부하의 조합들을 재현해야 함
     가끔 synthetic test 할 때 이를 하면서, 시스템에서 실제 사용자에게 제공하는 데이터를 수집하고 분석한다

- 실제 사용자에게 서비스를 제공하는 시스템에서 실험하는 것은 두 가지 이유로 어려움:

  1. 실제 사용자가 생산하는 부하를 제어하지 않기 때문에, 우리들은 통계적으로 중요한 결과를 얻기 위해 매우 많은 무작위의 사용자 샘플에 각 실험을 할 필요가 있음
  2. 실제 사용자에게 섭ᄉᆜ를 제공하는 시스템에서의 실험은 위험을 내재하고 있기 때문에, 우리들은 가능한 실제 실험을 수행하기 전에 통계를 이용해 실험에 대한 결과를 예측

- 따라서 실제 사용자에게 서비스를 제공하는 시스템으로부터 풍부한 성능 데이터 얻기 위해 두 가지 기법을 개발해옴

  1. coordinated bursty tracing
  2. sca



## PPT

USENIX NSDI(Networked Systems Design and Implementation) 18, 19, 20를 조사

- 18, 19, 20 기술 동향
- best paper



클라우드 어플리케이션의 성능 분석에 관하여 발표

이 논문은 대규모 클라우드 어플리케이션의 성능 분석에 관하여 다루고 있음

기존의 성능 분석

성능 분석이 왜 어렵나?

그래 어떻게 하고 있는가?

결론은?

이 논문의 장점은?

이 논문의 단점은?



클라우드 어플리케이션에서 성능 분석은 굉장히 중요하다.



1. 계속해서 바뀌는 부하는 시스템의 성능 분석은 매우 어려움
2. 쉽게 Synthetic environment를 재현하기 힘듬
3. 실제 사용자에게 실험을 수행해야 함
4. 이를 위한 방법
   - 어떻게 실험을 실행하는가?
   - 어떻게 성공적으로 통계를 사용하여 실험 결과와 우리가 직면할 수 있는 위기를 예측할 수 있는가?
   - 저속과 리소스 집중적인 동작을 디버그 할 필요가 있는 두 가지 context 설명
     - Temporal context
       Coordinated Bursty Tracing
     - Operation context
     - 









## Reference

[[1]](https://dl.acm.org/doi/abs/10.1145/583854.582432)


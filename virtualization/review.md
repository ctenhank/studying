# An Updated Performance Comparison of VM and LXC

## Abstract

- 클라우드 어플리케이션은 VM을 통해서 Isolation과 resource control을 통해서 이때까지 구현되거나 실행되었지만, 이는 몇 단계의 추상화 레벨 때문에 성능 저하 초래 
- 컨테이너 기반 가상화는 또 다른 하나로부터 어플리케이션을 고립시키면서 어플리케이션 전개를 단순화시킴 
- 이 논문에서는 VM에 대해서 알아보고 LXC와 대조하면서 컨테이너가 대부분의 경우 더 낫다는 것을 보여줌

## Introduction

- Isolation과 resource control은 클라우드 컴퓨팅 환경에서 중요한 두 요구사항임

  > Isolation은 하나의 워크로드 실행이 동일한 시스템의 다른 워크로드 실행을 영향을 끼치지 않음을 의미
  > resource control은 한 워크로드에 특정 리소스 셋을 제약하는 능력, 기능을 의미

- In the cloud setting, while performance isolation is desirable, it is often secondary to functional and security isolation wherein one workload cannot learn anything or affect the correctness of another workload.

- VM에서 Isolation은 각 VM 안에 워크로드를 실행하고, VM 그 자체에 리소스 제약을 가해서 달성했지만, 이는 성능 비용이 발생한다.
- VM은 클라우드 컴퓨팅에서 매우 널리 쓰이므로, VM 성능은 전체 클라우드 성능에 굉장히 중요한 구성요소이다. 하지만 VM은 하이퍼바이저와의 오버헤드가 발생할 수 밖에 없는 구조이다.
- 따라서 컨테이너 기반 가상화는 VM 대안으로 사용할 수 있다. 비록 네임스페이스와 같은 컨테이너 기반 컨셉들은 꾀나 오래되었지만, 최근에 되어서야 운영체제 메인으로 채택되고 표준화되었고, 컨테이너 사용하여 isolation과 resource control 기능을 제공하는 르네상스로 ꥶᅮ어짐
- 리눅스는 무료라는 점과 거대한 생태계, 하드웨어 지원, 성능, 신뢰성 등으로 클라우드에서 가장 선호되는 운영체제이다.
- 컨테이너를 구현하는데 있어 필요한 커널 네임스페이스 기능은 2006에 논의되어 채택되었으며, 그 이후 도커가 등장했다.
- 이 논문에서는 Isolation과 resource control을 달성하는 두 가지 다른 방법 VM, LXC에 대해서 소개하고, 하드웨어에 워크로드 셋을 실행함으로써 비교한다.
- 또한, CPU, 메모리 대역폭, 지연속도 , 네트워크, I/O, 실사례 redis, mysql 등에 벤치마크하여 비교한다.

## Background

### Motivation

 리눅스 환경은 Principle of least privilege와 the least common mechanism principle이 잘 구현되어 있지 않았다. 파일시스템, 프로세스, 네트워크 스택 등 대부분 Unix  Object는 모든 사용자들이 전역적으로 볼 수 있었서 *configuration isolation*이 부족했다. 즉, 다수의 어플리케이션의 의존성 충돌을 해결하기가 힘들었다. 따라서 이 문제를 해결하고자 OS를 dedicated server 또는 VM에 각 어플리케이션을 설치하여 배치를 단순화시켰다. 

 기업 자체에서 클라우드를 쓰는 것과 달리 IaaS, PaaS에서 공급자와 고객은 독립적인 관계가 있다. 이는 성능 이상(초과 신청)를 해결하기 어렵기에, 공급자는 보통 고정된 CPU, 메모리 용량의 unit을 제공한다.  그리고 공유되는 하드웨어에서 다수의 사용자가 실행시키기 때문에 보안 문제도 중요하다.

 또한, IBM의 평균 리소스 사용량이 10~15% 밖에 안되어 이 사용량을 늘리기 위해서 하기도 함

### KVM

- Kernel Virtual Machine은 리눅스가 프로세스 안에서 수정되지 않은 게스트 OS를 실행시킴으로써 type 1 하이퍼바이저처럼 행동할 수 있게하는 기능이다.
- ㄷ
# Virtualization

## Concepts



## Objective

* resource utilization
* security
* isolation(reduction dependencies)



Full-Virtualization

Para-Virtualization





## Technology

- **isolation**
- **multitenancy**
- **resource control**





## Virtual Machine

- VMware
- Xen
- KVM
- Hyper-V



- 하이퍼바이저 배치는 동일한 클라우드에 다른 운영체제나 운영체제 버전이 실행될 때 적용하는 것이 좋다.
- VM은 OS의 완벽한 구현 및 실행이므로 어떤 OS더라도 어떤 bare metal에서도 실행시킬 수 있다.



## Container

- Unix chroot
- FreeBSD, Solaris jail
- Solaris zones
- Solaris-11 container
- LXC
- Docker



- container는 application들이 한 OS의 라이브러리, 바이너리들을 공유하기 때문에 상당히 하이퍼바이저보다 크기가 작고, 이는 하나의 물리적 호스트에 수 백개의 container들을 배치할 수 있게 한다. 또한, container는 host OS를 사용하기 때문에, 컨테이너를 재시작할 때 OS를 재시작할 필요가 없다.
- 컨테이너는 이미 실행되고 있는 OS의 한 부분을 제공하는데, 그 OS에 직접적으로 어플리케이션을 실행하는 것처럼 OS 구조에 접근할 수 있다.
- ***컨테이너를 security isolation에 이용하는 것은 좋지 않은 방법이다. docker에서는 하나의 호스트 또는 하나의 VM 당 하나의 Docker만 이용하기를 권장하고 있다.***



### Docker

- 도커는 LXC를 프로세스 실행을 고립시키기 위해 커널, 어플리케이션 수준의 API와 함께 확장했다.

  > CPU, 메모리, I/O, 네트워크 등

- 도커는 또한 운영체제 기반의 어플리케이션 관점을 완전히 고립시키기 위해 리눅스 커널 네임스페이스를 이용한다.

  > 프로세스 트리, 네트워크, 사용자 ID, 파일 시스템

- 도커 컨테이너는 base image를 이용하여 생성되는데, 이는 OS의 기초적인 것들과 다른 응용 프로그램들로 이루어 질 수 있다.

- Dokcerfiles를 다양한 명령어를 이용하여 수동/자동으로 실행할 수 있고, 이를 통해 base image를 새로운 image로 형성 또는 만들 수 잇다.

- 컨테이너는 VM에서 실행할 수 있다.



## Kubernetes

 실행하고 있는 시스템의 상세한 부분으로부터 어플리케이션 컨테이너를 디커플링하는 것이다. 구글 클라우드 플랫폼은 쿠버네티스에 리소스의 homogenous set을 제공하고, 차례로 쿠버네티스는 그 리소스들을 사용하기 위해 컨테이너들을 스케쥴링한다. 이러한 디커플링은 어플리케이션 개발을 단순화시키는데 이는 사용자가 코어와 메모리와 같은 추상화된 리소스를 요청하기 때문이고, 또한 이는 데이터센터 동작을 단순화한다.





review:

[On the Evolution of Virtualization and Cloud Computing: A Review](https://d1wqtxts1xzle7.cloudfront.net/55865607/CC.pdf?1519245018=&response-content-disposition=inline%3B+filename%3DOn_the_Evolution_of_Virtualization_and_C.pdf&Expires=1600061804&Signature=cg2oh25oQEhSohQYuEdD-W~OScFENS7JlOqV8W1KrRDmsZs-Pmha08lvEH7pn-REBLmkFP1RvteYKEDtkv-l1CxYoiJn5JEgbV45O5hMTV8XLWH4s7xkjjPVMJHv0ZWZMInmWPLyysAUgRuxmCWt-0XwU8yA5~-S-EP8uDOfFRSuKE2AiSz2W24LFgmMp2BO3suGjHWOCVVG09ePyYpZf4bF2r9QvQusMW3i4e41bIupqVKWrsGUW8OnNxIeS4z2NORZKUIoycvt8h9LtywbkngY-ImU8krdSj-IjQOL340FLYUU3sytbi9-8i1BwO2hkzaqiuwzx45m-0QAxo2vqw__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA)

[Virtualization Technology Literature Review](https://computerresearch.org/index.php/computer/article/view/317/317)

[A Review on Virtualization: A Cloud Technology](https://d1wqtxts1xzle7.cloudfront.net/38268921/A_Review_on_Virtualization_A_Cloud_Technology.pdf?1437649168=&response-content-disposition=inline%3B+filename%3DA_Review_on_Virtualization_Cloud_Technol.pdf&Expires=1600061916&Signature=HJwc~86Ir~-7PQlZUHArjefJ1DCCMYBuLA7pi490gIuxZMqeCRsFF88JB4YVELPQqxJ0iozKqRhl2tndHG5-y5h6iR0k6lHmz-kWHNzTJGWonSvkUseZalBqcBilaJ105bzNy6g~PyGtaS4zD--cMjbIKOFJQc543TwdPSY8F~xrGiYhGeioDX2JGrDFKhsFT4C9sxUK9NNpcNTGupa1s5R5nbg3mE0cralI9emq0o1L5BxZhRj~tmOuagIx-BF~aebZwwoYybTb4DZcLHNnawCY1LUQMzHUjjssCOisA80NaApDUenB2g6n9XlxPgQNog3dKUe5YEBMfsVQuvHr9Q__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA)

[Network Virtualization: Technologies, Perspectives, and Frontiers](https://ieeexplore.ieee.org/abstract/document/6272301)

[A survey of network virtualization](https://www.sciencedirect.com/science/article/pii/S1389128609003387)

[Data Center Network Virtualization: A Survey](https://ieeexplore.ieee.org/abstract/document/6308765)

[OS-level Virtualization and Its Applications](https://dspace.sunyconnect.suny.edu/bitstream/handle/1951/44896/000000243.sbu.pdf?sequence=3)

[Analysis of Virtualization Technologies for High Performance Computing Environments](https://ieeexplore.ieee.org/abstract/document/6008687)


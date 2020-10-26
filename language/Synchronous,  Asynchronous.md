# Synchronous,  Asynchronous, Blocking, Non-Blocking

- I/O 연산은 CPU 연산에 비해서 훨씬 느린 특성을 가지고 있음

  > SSD 스토리지를 이용한 작업 수행을 예제로 들어보자
  >
  > 현재 1.4GBps 속도가 SSD 중에서 가장 빠른지는 모르겠지만 빠르다고 소개되어 있다. 
  > 이 속도는 50GB 데이터를 약 5분만에 옮길 수 있다.
  > 다시 이 속도를 초 단위로 환산하면, 초당 167MB 데이터를 옮길 수 있는 것
  > 그리고 1 기가헤르츠 클럭 프로세스는 초당 1,000,000,000 처리 사이클을 수행할 수 있다.
  >
  > 대충 상상해보면, I/O 겨우 167MB 옮기는데 반면 64비트 프로세스는 약 8GB 명령어 또는 데이터를 처리할 수 있음

- CPU연산과 I/O연산에 대한 가장 단순한 모델인 동기 입출력는 통신 중에 프로그램 진행을 막아 리소스를 낭비시킴

### Synchronous vs Asynchronous

- 동기적으로 어떤 것을 실행한다는 것은 또다른 작업을 수행하기 전에 먼저 하던 것을 끝날때까지 기다려야 한다는 것
- 비동적으로 어떤 것을 실행한다는 것은 하던 것을 요청하고 응답이 올 때까지 주기적으로 체크하거나 신경쓰지 않음

|                                              | Synchronous Execution                                        | Asynchronous  Execution                                      |
| -------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 사전적 의미[[1]](https://www,dictionary.com) | occurring at the same time; coinciding in time; contemporaneous; simultaneous. | *Digital Technology*. (of a computer or other electrical machine) having each operation started only after the preceding operation is completed. |
|                                              |                                                              |                                                              |

### Blocking vs Non-Blocking


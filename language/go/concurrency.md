# Concurrency in Golang

- Go는 **Communicating Sequential Processes (CSP)** 스타일의 Concurrent 프로그래밍 모델을 사용[[1]](http://golang.site/go/article/1-Go-프로그래밍-언어-소개)

### Concurrency?

<img src="https://iamluminousmen-media.s3.amazonaws.com/media/concurrency-and-parallelism-are-different/concurrency-and-parallelism-are-different-2.jpg" alt="concurrency" style="zoom:67%;" />

- 일정 시간 간격으로 여러 개의 task를 수행하는 것

  > ex. multi-tasking

- 더 자세한 내용은 [링크](../Concurrency, Parallelism.md)에서 참조

### Concurrency in Golang

>  Do not communicate by sharing memory; instead, share memory by communicating.

#### Do not communicate by sharing memory

- 프로그래밍 언어에서 코드를 동시적으로 실행시킬 때 여러 개의 [쓰레드](../../os/thread.md)들을 이용

- 쓰레드 사이의 **Communication**이란

  - 쓰레드들은 복잡하게 구현되면서 병행적 수행을 함

  - 서로 공유할 데이터 구조/변수/메모리 등이 무엇인지 파악

  - 공유할 때 `race condition`이 발생하지 않게 동시성 객체(ex. 뮤텍스 등)을 이용

    > 쓰레드가 동시간에 한 곳에서 `write` 할 수 없으니 이를 해결하기 위한 방안

- Communcation은 `race condition`, `unknown expceptions`, `deadlock` 등을 야기시킬 수 있음

  > 위의 컨셉들에 대한 자세한 내용은 [쓰레드](../../os/thread.md)를 확인

#### Share memory by communcating

- `Golang`에서는 공유 메모리 변수에 대해 `lock` 하는 대신 하나의 쓰레드에서 *다른 하나*로 변수에 저장된 값을 communcation 하게 만들어 줌

  > `golang`에서 *다른 하나*는 정확히 쓰레드는 아니고, 경량화된 쓰레드 `gorountine`이라고 함

- `Golang`에서는 순차적 통신 행위를 라이브러리 차원이 아니라 언어 차원에서 지원

  > **순차적 통신 행위**
  >
  > 데이터를 보내는 쓰레드와 받는 쓰레드가 전송이 완료될 때까지 아무것도 하지 않음

- `buffered channel`를 통해서 전송이 완료될 때까지 쓰레드들 간에 어떤 `lock`이나 `sync`를 맞출 필요가 없음


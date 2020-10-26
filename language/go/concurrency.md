# Concurrency in Golang

- Go는 **Communicating Sequential Processes (CSP)** 스타일의 Concurrent 프로그래밍 모델을 사용[[1]](http://golang.site/go/article/1-Go-프로그래밍-언어-소개)

### Concurrency?

<img src="https://iamluminousmen-media.s3.amazonaws.com/media/concurrency-and-parallelism-are-different/concurrency-and-parallelism-are-different-2.jpg" alt="concurrency" style="zoom:67%;" />

- 일정 시간 간격으로 여러 개의 task를 수행하는 것

  > ex. multi-tasking

- 더 자세한 내용은 [링크](../Concurrency, Parallelism.md)에서 참조

## Concurrency in Golang

>  Do not communicate by sharing memory; instead, share memory by communicating.

### Do not communicate by sharing memory

- 프로그래밍 언어에서 코드를 동시적으로 실행시킬 때 여러 개의 [쓰레드](../../os/thread.md)들을 이용

- 쓰레드 사이의 **Communication**이란

  - 쓰레드들은 복잡하게 구현되면서 병행적 수행을 함

  - 서로 공유할 데이터 구조/변수/메모리 등이 무엇인지 파악

  - 공유할 때 `race condition`이 발생하지 않게 동시성 객체(ex. 뮤텍스 등)을 이용

    > 쓰레드가 동시간에 한 곳에서 `write` 할 수 없으니 이를 해결하기 위한 방안

- Communcation은 `race condition`, `unknown expceptions`, `deadlock` 등을 야기시킬 수 있음

  > 위의 컨셉들에 대한 자세한 내용은 [쓰레드](../../os/thread.md)를 확인

### Share memory by communcating

- `Golang`에서는 공유 메모리 변수에 대해 `lock` 하는 대신 하나의 쓰레드에서 *다른 하나*로 변수에 저장된 값을 [`channel`](#Channel)을 통해 communcation 하게 만들어 줌

  > `golang`에서 *다른 하나*는 정확히 쓰레드는 아니고, 경량화된 쓰레드 [`goroutine`](#Goroutine)이라고 함

- 하나의 `goroutine`은 주어진 시간에만 데이터에 접근할 수 있음

  > 따라서 `race condition`이 발생하지 않음

- `Golang`에서는 순차적 통신 행위를 라이브러리 차원이 아니라 언어 차원에서 지원

  > **순차적 통신 행위**
  >
  > 데이터를 보내는 쓰레드와 받는 쓰레드가 전송이 완료될 때까지 아무것도 하지 않음

- `buffered channel`를 통해서 전송이 완료될 때까지 쓰레드들 간에 어떤 `lock`이나 `sync`를 맞출 필요가 없음



## Goroutine

![goroutine](https://miro.medium.com/max/5216/1*dD8qcmhpjUlKxZ1GHmX1AQ.png)

> They're called *goroutines* because the existing terms—threads, coroutines, processes, and so on—convey inaccurate connotations. A goroutine has a simple model: it is a function executing concurrently with other goroutines in the same address space. It is lightweight, costing little more than the allocation of stack space. And the stacks start small, so they are cheap, and grow by allocating (and freeing) heap storage as required.

- Go 런타임이 자체 관리하는 Lightweight 논리적 쓰레드

  > 동일한 주소 공간에 여러 `goroutine`들로 병행적으로(concurrently) 실행시키는 함수

- Go에서 `go` 키워드를 사용하여 `function`를 호출하면, 런타임 시 새로운 `gorountine` 실행
- `goroutine`은 비동기적으로([`asynchronously`](../Synchronous,  Asynchronous.md)) 함수 루틴을 실행하므로, 여러 코드를 동시에 실행하는데 사용
- `goroutine`들은 OS [`thread`](../../os/thread.md)들과 1:1 대응하지 않고, multiplexing으로 훨씬 적은 OS thread들을 사용
- 메모리 측면에서도 OS 쓰레드가 1 MB 스택을 갖는 반면 `goroutine`은 몇 KB 스택(필요시 동적 증가)을 가짐
- Go 런타임은 `goroutine`을 관리하면서 `channel`을 통해 `goroutine` 간의 통신을 쉽게할 수 있도록 함

### Goroutine with Anonymous Function

- `go` 키워드 뒤에 `anonymous function`를 바로 정의하면 익명함수를 비동기로 실행함

- `sync.waitGroup`

- `wait.Add(number)`

- `wait.Done()`

- `wait.Wait()`

  

## Channel

###  Features

- Go `channel`은 그 채널을 통해서 데이터를 주고 받는 통로
- 내장함수 `make()`를 통해 미리 생성되어야 하며, 채널 연산자 `<-` 를 통해 데이터를 주고 받음
- 흔히 `channel`은 `goroutine` 들 사이에 데이터를 주고 받는데 사용하는데, **상대편이 준비될 때까지 채널에서 대기**함으로써 별도의 `lock`을 걸지 않고 데이터를 동기화하는 사용
- 상대편이 준비될 때까지 채널에서 대기하는 속성을 이용해 `gorotuine`


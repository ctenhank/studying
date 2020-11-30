## Goroutine

### Overview

<img src="https://miro.medium.com/max/5216/1*dD8qcmhpjUlKxZ1GHmX1AQ.png" alt="goroutine" style="zoom: 15%;" />

> They're called *goroutines* because the existing terms—threads, coroutines, processes, and so on—convey inaccurate connotations. A goroutine has a simple model: it is a function executing concurrently with other goroutines in the same address space. It is lightweight, costing little more than the allocation of stack space. And the stacks start small, so they are cheap, and grow by allocating (and freeing) heap storage as required.[[1]][1]

 Golang에서 고루틴은 [동시성](concurrency.md)을 지원해주기 위한 가벼우면서 빠르고 사용하기 편리한 기본 단위이다. 고루틴은 [쓰레드](../os/thread.md) 개념과 유사하지만 차이점이 존재한다.  그러한 차이점이 고루틴을 쓰레드보다 500배 이상 가볍고, 더욱 빠르게 만든다. 쓰레드는 약 1MB 메모리 공간을 차지하는 반면 고루틴은 단 **2KB 메모리 공간**만 필요하다. 또한, 고루틴은 Golang 키워드 `go`만으로 매우 간단하게 사용할 수 있다. 

그리고 고루틴과 쓰레드에 대해 좀 더 자세히 알아보자.

## Goroutine and Thread[[2]][2]

고루틴과 쓰레드의 차이점은 크게 세 가지가 있다.

- Memory Consumption
- Setup and Teardown Costs
- Context Switching Costs

#### Memory Consumption

쓰레드와 고루틴은 기본적으로 자신만의 `stack` 공간을 가지고 필요에 따라 `heap`에 할당하여 메모리를 이용한다. 쓰레드는 다음 그림과 같이 각자 **자신만의 레지스터** 정보와 필요한 정보들을 가진다. 또한 쓰레드는 **Guard Page**[[3]][3][[4]][4]를 가지므로, 하나의 쓰레드를 생성할 때마다 약 1MB 메모리 공간이 필요하다.

<img src="https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/images/Chapter4/4_01_ThreadDiagram.jpg" alt="thread" style="zoom:50%;" />

반면 고루틴은 약 2KB[[5]][5]의 스택 공간만을 요구하고, 필요에 따라 힙 공간에 추가적으로 할당하기 때문에 처음부터 많은 메모리 공간이 필요 없다. 고루틴의 수에 따라 하나의 고루틴을 생성하기 위한 기본 요구 스택 공간은 점점 커지긴 하지만, 5000만개의 고루틴을 생성하더라도 `2695.37 bytes`밖에 차지하지 않는다.[[6]][6]

> 고루틴은 자신만의 레지스터를 가지지 않으면, 만약 고루틴이 블럭되어 교체되면 교체된 고루틴은 다시는 사용되지 않는가?

#### Setup and Teardown Costs

쓰레드는 기본적으로 **OS**에서 관리하는 유닛이기 때문에, 쓰레드 생성과 파괴는 **kernel mode**로 전환되는 과정이 필요하다. 반면 고루틴은 **Go Runtime**이 관리하기 때문에 쓰레드 처리 관련 비용이 들지 않아 매우 저렴하다.

#### Context Switching Costs

한 쓰레드는 블럭되거나 알 수 없는 원인에 의해서 교체될 시[[7]][7], 기본적으로 OS에 의해 다른 쓰레드로 스케쥴링된다. 쓰레드가 교체되면, 자신의 수 많은 레지스터들을 저장해야 하고, 다른 쓰레드의 레지스터 값을 CPU 레지스터에 입력해야 한다. 이 과정은 고루틴에 비해 상당히 많은 비용이 든다.

반면 고루틴은 Context Switching될 시, 단 **3개의 레지스터들만 교체**된다. 따라서 쓰레드에 비해 굉장히 빠른 속도로 Context Switching이 이루어진다. 고루틴의 교체되는 레지스터들은 프로그램 카운터, 스택 포인터, 데이터 레지스터이다.

### How goroutines are executed

Golang에서는 **Go 런타임**이 프로그램 시작부터 끝나는 시점까지 내내 고루틴을 관리한다. 런타임은 모든 고루틴을 일부 쓰레드들에 다중화하여 할당한다. 각 쓰레드는 어떤 시점에서 하나의 고루틴을 실행하며, 고루틴이 블럭되면 다른 고루틴으로 교체하여 실행시키기 때문에 쓰레드가 블럭되지는 않는다.

### Goroutines Blocking

고루틴은 다음과 같은 상황에서 블럭될 수 있다.

- 네트워크 입력
- sleeping
- channel 연산
- `sync` 패키지에 의한 블럭킹

고루틴이 블럭되더라도 런타임이 다른 고루틴을 실행시키기 때문에 쓰레드가 블럭되지는 않는다. 런타임에서 자동으로 고루틴을 쓰레드에 배정해주기 때문에 쓰레드를 다룰 필요없다. 또한 CPU가 쓰레드의 존재를 모르는 것과 같이 OS는 고루틴의 존재를 모른다. 따라서 OS 측면에서, Go 프로그램은 이벤트 기반 C 프로그램과 같이 동작한다.

## Usage

### Goroutine with Anonymous Function

- `go` 키워드 뒤에 `anonymous function`를 바로 정의하면 익명함수를 비동기로 실행함

- `sync.waitGroup`

- `wait.Add(number)`

- `wait.Done()`

- `wait.Wait()`



## References

[1]: https://golang.org/doc/effective_go.html#goroutines
[2]: https://stonzeteam.github.io/How-Goroutines-Work/
[3]:https://us-cert.cisa.gov/bsi/articles/knowledge/coding-practices/guard-pages
[4]: https://docs.microsoft.com/en-us/windows/win32/procthread/thread-stack-size
[5]: https://tpaschalis.github.io/goroutines-size/
[6]: https://stackoverflow.com/questions/8509152/max-number-of-goroutines/8534711#8534711
[7]: https://stackoverflow.com/questions/22511211/when-does-the-os-switch-threads-in-a-multithreaded-program
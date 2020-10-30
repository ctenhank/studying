# Golang Context

### Prerequisite

- Gorutine
- Channel

## Introduction

Golang Context를 알아보기 전에, Context에 대한 사전적 의미부터 알아보자.

> **Context** [[1]][1]
>
> 1. the parts of a written or spoken statement that precede or follow a specific word or passage, usually influencing its meaning or effect:*You have misinterpreted my remark because you took it out of context.*
> 2. the set of circumstances or facts that surround a particular event, situation, etc.

위의 사전적 의미를 보면, 

**Context**는 **이전**에 나온 언어표현[[2]][2] 또는 환경 등과 같은 표현과 연관있는 이후의 언어 표현 및 환경 등의 표현이 서로 맺고 있는 **관계**[[3]][3]를 말한다. 간단히 말하자면, **Context**는 **이전에 나온 표현과 이후에 나온 표현**의 서로 맺고 있는 **관계**, 즉 **맥락**을 말한다.

그럼 컴퓨터 세계에서 Context을 살펴보자.[[4]][4]

- Context Switch
- Bounded Context
- Context Menu
- etc.

컴퓨터 세계에서의 **Context**를 살펴보면 다른 의미로 쓰이는 것 같지만, 위에 대한 개념을 살펴보면 크게 다르지도 않다. 정말 그런지 확인하기 위해 위의 Context들 중 Context Switching에 대해서 간단히 알아보자.

#### Context Switch란?

먼저 wikipedia의 Context Switch의 정의를 살펴보면, 다음과 같다.

> In [computing](https://en.wikipedia.org/wiki/Computing), a **context switch** is the process of storing the state of a [process](https://en.wikipedia.org/wiki/Process_(computing)) or [thread](https://en.wikipedia.org/wiki/Thread_(computing)), so that it can be restored and resume [execution](https://en.wikipedia.org/wiki/Execution_(computing)) at a later point.[[5]][5]
>
> 저장하는 상태가 프로세스냐 쓰레드냐에 따라서 Process/Thread Context Switch라고도 한다. 이에 대한 차이점을 알고 싶다면 링크를 참조하자.[[6]][6]

이를 해석하면, 다음에 이어서 실행하기 위해 프로세스 또는 쓰레드의 상태를 저장하는 과정을 의미한다.

이를 쉽게 이해해보자.

우리가 현재 사용하고 있는 컴퓨터, 스마트폰 등은 동시에 여러 프로세스들을 실행하는 것 같지만, 실제로는 사람이 느낄 수 없는 **매우 짧은 시간 간격**으로 교체하면서 실행하고 있다. 따라서 교체할 때 CPU 레지스터나 캐시 메모리 등에 저장된 이전 프로세스와 관련된 데이터들은 따로 저장해두고, 다른 프로세스의 데이터들을 해당하는 장치들에 입력하여 그 프로세스를 실행해야 한다. 이런 저장하거나 입력해야하는 데이터들을 프로세스의 맥락, 즉 **Context**라 볼 수 있다.

> 물론, Multi-core CPU의 경우는 프로세스들을 말 그대로 동시에 실행할 수 있다. 하지만 우리가 일상적으로 사용하고 있는 컴퓨터에서는 적게는 수십 개, 수백 개 혹은 그 이상의 프로세스가 동시에 돌아가기 때문에, 한 코어가 짧은 시간동안 프로세스를 번갈아 가면서 실행하는 것은 동일하다.
>
> ubuntu 환경에서는 다음 명령어로 실행중인 프로세스 개수를 확인할 수 있다.
>
> ```bash
> ps -e | wc -l
> ```

## Golang Context

앞서 살펴 본 내용과 같이 Go에서도 **맥락(Context)**을 유지하기 위해 `context.Context` type을 제공한다. **Context**는 함수 또는 API[[7]][7] 간 `key-value` 형태로 값을 저장하여 쓸 수 있으며, **Context**의 종료 시간(`deadline` or `timer`) 또는 종료 신호를 설정하여 사용할 수 있다.

Context를 이용하려면 무조건 `Background()` 또는 `TODO()` 함수를 통해 **값을 저장할 수 없고, 절대 취소할 수 없는** `init Context`를 만들어야 한다. 만약 다른 함수 또는 API의 매개변수, 인자값을 통해 전해받았다면, 이는 초기의 다른 함수에서 `Background()`를 이용해서 `init Context`를 생성하고 넘겨준 것이다. 이후 `WithValue()`, `WithCancel()`, `WithTimer()`, `WithDeadline()` 함수들을 통해 **derived context**를 생성하여 용도에 맞게 활용할 수 있다.

### Golang Context Architecture

Golang Context 인터페이스와 구조체는 다음과 같다.

#### `type Context Interface`

```go
type Context interface {
	Deadline() (deadline time.Time, ok bool)
	Done() <-chan struct{}
	Err() error
	Value(key interface{}) interface{}
}
```

#### `type emptyCtx int`

```go
type emptyCtx int
```

#### `type cancelCtx struct`

```go
type cancelCtx struct {
	Context

	mu       sync.Mutex            // protects following fields
	done     chan struct{}         // created lazily, closed by first cancel call
	children map[canceler]struct{} // set to nil by the first cancel call
	err      error                 // set to non-nil by the first cancel call
}
```

#### `type canceler interface`

```go
type canceler interface {
	cancel(removeFromParent bool, err error)
	Done() <-chan struct{}
}
```

#### `type timerCtx struct`

```go
type timerCtx struct {
	cancelCtx
    
	timer *time.Timer // Under cancelCtx.mu.
	deadline time.Time
}
```

#### `type valueCtx struct`

```go
type valueCtx struct {
	Context
    
	key, val interface{}
}
```

#### `type CancelFunc func()`



### Golang Context Usage

Golang Context 사용법은 먼저 `emptCtx`를 `context.Background()` 또는 `context.TODO()` 함수로 생성해야 한다. 

```go
import (
    "context"
)
ctx := context.Background()
```

이후 `WithValue()`, `WithCancel()`, `WithTimer()`, `WithDeadline()` 함수들을 통해 **derived context**를 생성하여 용도에 맞게 활용할 수 있다.

#### `func WithValue()` 사용법

https://velog.io/@kimmachinegun/Go-context.WithValue-%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0





## References

[1]: https://www.dictionary.com/browse/context?s=t
[2]: http://encykorea.aks.ac.kr/Contents/Item/E0019457
[3]: https://dict.naver.com/search.nhn?dicQuery=%EB%AC%B8%EB%A7%A5&query=%EB%AC%B8%EB%A7%A5&target=dic&ie=utf8&query_utf=&isOnlyViewEE=
[4]: https://jaehue.github.io/post/how-to-use-golang-context/
[5]: https://en.wikipedia.org/wiki/Context_switch
[6]: https://stackoverflow.com/questions/5440128/thread-context-switch-vs-process-context-switch
[7]: https://www.quora.com/What-is-the-difference-between-an-API-and-a-function
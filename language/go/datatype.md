# Data type in Golang

- Boolean

  - keyword: `bool`

- String

  - keyword: `string`
  - 다른 데이터 타입으로 변경이 불가능(Immutable type)

- Integer

  - keyword: `int`, `int8`, `int16`, `int32`, `int64`, `uint*`

- Float and Compex type

  - keyword: `float32`, `float64`, `complex64`, `complex128`
  - `double`이라는 키워드는 없음

- Others

  - `byte`: `uint8`과 동일하며 바이트 코드에 사용
  - `rune`: `int32`와 동일하며 유니코드 코드포인트에 사용

  > `string`과 `byte`, `rune`의 차이점은 `string`은 `immutable type`이기 때문에 해당 변수를 새로 할당하지 않고서는 기존의 데이터를 재활용할 수 없다. 
  >
  > 예를 들어서  `var s string = "abc"`
  > "abc"라는 문자열을 유지한채로 새로운 문자열을 삽입하거나, "abc"에서 어떤 문자열들을 지울 수 없다.
  >
  > 따라서 만약 8비트 [문자열 인코딩](../../encoding.md)을 이용한다면 `byte` 문자열을 유니코드 문자열 인코딩을 이용한다면 `rune`타입을 이용하여 앞선 연산들을 수행할 수 있음

### String

문자열 리터럴은 `""`(Double Quote) 또는 ``(Back Quote)로 표현가능

- ``(Back Quote)

  - **Raw String Literal**라고도 불림

  - 문자열을 별도로 해결하지 않고, **Raw String** 그대로의 값을 가짐

  - 복수 라인의 문자열을 표현할 때 자주 사용됨

    >  ex. ``"abc\ndef"`가 있으면 `\n` 이 `NewLine`으로 해석되지 않음

- `""`(Double Quote)

  - **Interpreted String Literal**라고도 불림
  - 복수 라인에 걸쳐 사용할 수 없으며, 인용부호 안에 `\n`를 통해 수행할 수 있음
  - 여러 라인에 걸쳐 사용하려면 `+` 연산자를 통해 할 수 있음

  ```go
  package main
  
  func main() {
  	raw := `Hello world!\n
  Welcome to Go`
  
  	inter := "Hello world!\n" +
  		"Welcome to Go"
      println("RAW:")
  	println(raw)
      println("INTER:")
  	println(inter)
  }
  
  /* Output */
  RAW:
  Hello world!\n
  Welcome to Go
  INTER:
  Hello world!
  Welcome to Go
  ```

### Type Conversion

- `Golang`에서는 타입 변환을 하기 위해서는 반드시 데이터 타입을 명시해줘야 함

- 데이터 타입 변환을 위해서는 `T(v)`를 통해 할 수 있음, T는 데이터 타입, v는 변환될 값을 지정

  ```go
  func main() {
  	var i int = 3
      var u uint = uint(i)
      var f float32 = float32(i)
      println(i, u, f)
  }
  ```

- 다른 언어와는 달리 이미 데이터 타입이 명시된 변수의 타입은 변경할 수 없음

  ```go
  func main() {
  	var i int = 3
      // int로 데이터 타입이 명시된 변수 i를 float32 데이터 타입으로 변경하고 싶지만
      // 에러가 발생함
  	i = float32(i)
  	println(i)
  }
  ```


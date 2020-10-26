# Variable, Constant, Keyword in Golang

## Variable

- 변수는 키워드 `var`를 사용하여 선언하는데, `var` 키워드 뒤에 변수명을 적고, 그 뒤에 변수타입을 적음

  ```go
  var a int
  var f float32
  // 동일한 타입의 변수를 복수 개 선언할 수도 있음
  var b, c, d int
  ```

- 변수 선언문에서 변수 초기화를 할 수 있음

  ```go
  var a int = 1
  var f float32 = 11.
  var b, c, d int = 2, 3, 4
  ```

- 변수 선언 시 타입을 생략하면 Go는 할당되는 값을 보고 추론함

  ```go
  var n = 1
  var m = "string"
  ```

- 변수 선언 시 여러개를 묶어서 지정할 수 있음

  ```go
  var (
      a int = 1
      b string = "hello"
      c float32 = 3.
  )
  ```

- 선언된 변수가 Go 프로그램 내에서 사용되지 않으면 **에러 발생**시키므로 사용하지 않는 변수는 삭제해야 함

- 변수를 선언하고 초기화 하지 않으면 `default`로 `Zero Value`를 할당

  - 숫자형에는 `0`, bool 타입에는 `false`, 문자열에는 `""`를 할당

- 변수 선언하는 또 다른 방식 `:=` (Short Assignment Statement)가 있음 

  - `var`를 생략하고 선언할 수 있음
  - 이 표현은 `func`(함수) 내부에서만 사용할 수 있으며, 함수 밖에서는 `var`ᄅᆖᆯ 사용해야 함

## Constant

- 상수는 키워드 `const`를 사용하여 선언하는데, 선언 순서와 사용법은 [Variable](#Variable)과 동일

- 상수 선언 시 여러 개를 묶어서 지정할 때 `iota` 값을 이용하면 상수값을 0부터 순차적으로 할당할 수 있음

  ```go
  const (
      a = iota
      b
      c
  )
  ```

## Keyword

- Go언어는 총 25개의 reserved keywords를 가짐

  ```go
  break        default      func         interface    select
  case         defer        go           map          struct
  chan         else         goto         package      switch
  const        fallthrough  if           range        type
  continue     for          import       return
  ```


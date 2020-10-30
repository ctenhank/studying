# Function in Golang

## Function

- 함수는 여러 문장을 묶어서 실행하는 코드 블럭의 단위
- function은 `definition keyword`, `receiver`, `function name`, `parameter`, `return`, `code block`으로 구성

### Definition Keyword

- Go에서는 `func` 키워드를 통해 함수를 정의

  ```go
  func foo(a int, msg string, etc ...string){
      println("foo")
  }
  ```

### Function Name

- 첫번째 문자는 반드시 문자로이 시작되어야 하며, 그 이후에는 어떤 알파벳나 숫자든 상관없음

  > regx : `[_a-zA-Z][a-zA-Z0-9_]*` 

- 첫번째 문자가 **대문자**이면 그 함수는 `public` 함수로, 다른 패키지에서 이 함수를 이용할 수 있음

- 첫번째 문자가 **소문자**이면 그 함수는 `private` 함수로, 다른 패키지에서 이 함수를 이용할 수 없음

- 함수 이름은 대소문자 구분을 하고, 네이밍은 `CamelToe` 방식으로 표현

  > CamelToe 방식은 function 이름을 이루는 각 단어의 첫 글자를 대문자로 표현하는 방식

### Parameters

- function은 두 가지 방식으로 파라미터를 표현할 수 있음
  - 일반적인 함수
  - 가변인자 함수(Variadic Function)

#### Normal Function

- 다른 언어들과 달리 Go에서 함수 파라미터를 표현하는 방법은 변수 이름이 먼저 나온 후 데이터 타입이 나옴

  ```go
  // a라는 변수 이름이 데이터 타입인 int 보다 먼저 나옴
  func bar(a int, msg string) {
      
  }
  ```

#### Variadic Function

- 가변인자 함수라고도 불리며 이는 고정된 숫자의 파라미터가 아니라, 다양한 숫자의 파라미터를 전달하고자 할 때 `...`를 사용하여 가변인자라는 것을 표현

- 가변인자 타입으로 표현 앞의 변수에 할당됨

- 아래 예제에서 `_` 변수는 **Blank Identifier**라 하며 [사용하지 않는 변수](variable_constant.md)를 받을 때 사용하는 특수한 변수

  > Golang에서 변수를 선언했지만 사용하지 않으면 에러가 발생
  
  ```go
  func say(msg ...string) {
      for _, s := range msg {
          println(s)
      }
  }
  ```

#### Pointer

- Go에서 `parameter`에 `pointer` 자료형을 선언할 때는 다음과 같이 선언

  ```go
  func (c *Client) query(endpoint string, out interface{}, q *QueryOptions) (*QueryMeta, error) {
      ...
  }
  ```

  

#### Pass by Reference

- Go에서 파라미터를 전달하는 방식은 크게 `pass by value`, `pass by reference`로 나뉨

##### pass by value

```go
package main
func main() {
    main_msg := "Hello"
    say(main_msg)
}
 
func say(say_msg string) {
    println(say_msg)
}
```

- 위의 예제를 보면, `main` 함수의 `main_msg` 변수의 "Hello" 문자열 값이 `say` 함수의 `say_msg` 파라미터에 복사되어 전달됨
- 즉, 이는 `say` 함수에서 `say_msg` 값을 변경하더라도 `main` 함수의 `main_msg` 값은 변경되지 않음

##### pass by reference

```go
package main
func main() {
    main_msg := "Hello"
    say(&main_msg)
    println(main_msg) //변경된 메시지 출력
}
 
func say(say_msg *string) {
    println(*say_msg)
    *say_msg = "Changed" //메시지 변경
}
```

- 위의 예제를 보면, `main` 함수에서 `main_msg` 변수에 `&` 연산자(포인터 연산자)를 붙여 `say` 함수에 전달하는데 이는 `main` 함수의 `main_msg`  변수의 값이 복사되는 것이 아니라 변수의 주소 값을 전달해줌
- 따라서, `say` 함수에서 `say_msg` 값을 변경하면 `main` 함수의 `main_msg` 값도 변경됨

### Return

- Go에서는 함수는 리턴 값이 없을 수도, 하나일 수도, 복수 개일 수도 있음

  ```go
  func foo() {
      println("hello world")
  }
  
  func bar() int {
      return 1
  }
  
  func qux() (int, int) {
      return 2, 3
  }
  ```

- Go언어는 또한 `Named Return Parameter`라는 기능을 제공

  > 이는 리턴되는 값들을 리턴 파라미터들에 할당할 수 있는 기능
  > 즉, 어떤 변수를 선언하여 그 변수에 할당하여 리턴해줌

  ```go
  func sum(nums ...int) (count int, total int) {
      for _, n := range nums {
          total += n
      }
      count = len(nums)
      return
  }
  ```

### Receiver

다른 객체지향 프로그래밍에서는 하나의 클래스를 선언하여 그 안에 변수와 메서드들을 선언하는 것과는 달리 golang에서는 `struct`, `interface` 개념만을 이용한다. `struct`는 데이터 값만 선언할 수 있다.

```go
type mutatable struct {
    a int
    b int
}
```

따라서 다른 프로그래밍 언어와 달리 어떤 `struct`와 함수를 연관시키기 위해서는 다음과 같이 선언할 수 있다.

```go
// declaration as value 
func (m Mutatable) StayTheSame() {
    m.a = 5
    m.b = 7
}

// declaration as pointer
func (m *Mutatable) Mutate() {
    m.a = 5
    m.b = 7
}
```

이 두 가지 함수를 이용하면 다음과 같은 결과가 나타난다.

```go
func main() {
    m := &Mutatable{0, 0}
    fmt.Println(m)
    m.StayTheSame()
    fmt.Println(m)
    m.Mutate()
    fmt.Println(m)
}

// The output of the above program is :
// &{0 0}
// &{0 0}
// &{5 7}
```



## Anonymous Function

- 함수명을 갖지 않는 함수를 익명 함수(Anonymous Function)이라 함

- 익명함수는 보통 함수 전체를 변수에 할당하거나 다른 함수의 파라미터에 직접 정의되어 사용됨

  ```go
  package main
   
  func main() {
      sum := func(n ...int) int { //익명함수 정의
          s := 0
          for _, i := range n {
              s += i
          }
          return s
      }
   
      result := sum(1, 2, 3, 4, 5) //익명함수 호출
      println(result)
  }
  ```

- 위와 같이 변수에 익명 함수를 할당하면, 변수는 함수명과 같이 취급되며 `변수명(파라미터)` 형식으로 함수 호출 가능

### First-Class Function

- Go 언어에서 함수는 **일급함수**로서 Go의 기본 데이터 타입들과 동일하게 취급됨

- 다른 함수의 파라미터 또는 리턴 값으로 사용할 수 있음

- 함수를 다른 함수의 파라미터로 전달하기 위해서는 두 가지 방법이 존재

  - 변수에 익명함수를 할당하여 변수를 전달
  - 파라미터에 직접적으로 함수를 구현

  ```go
  package main
   
  func main() {
      //변수 add 에 익명함수 할당
      add := func(i int, j int) int {
          return i + j
      }
   
      // add 함수 전달
      r1 := calc(add, 10, 20)
      println(r1)
   
      // 직접 첫번째 파라미터에 익명함수를 정의함
      r2 := calc(func(x int, y int) int { return x - y }, 10, 20)
      println(r2)
   
  }
   
  func calc(f func(int, int) int, a int, b int) int {
      result := f(a, b)
      return result
  }
  ```

### type statement

- type 문은 `struct`, `interface` 등 사용자 정의 타입 또는 함수 원형을 정의하기 위해 사용됨

  ```go
  // 원형 정의
  type calculator func(int, int) int
   
  // calculator 원형 사용
  func calc(f calculator, a int, b int) int {
      result := f(a, b)
      return result
  }
  ```

- 이렇게 함수의 원형을 정의하고 함수를 타 메서드에 전달하고 리턴받는 기능을 `delegate` 기능이라 함

## Closure Function

- 클로저 함수는 함수 바깥에 있는 변수를 참조하는 함수값을 일컫음

- 이때 함수는 마치 바깥의 변수를 마치 함수 안으로 끌어들인 듯이 그 변수를 읽거나 쓸 수 있음

- `func 함수명(매개변수) func(매개변수) 자료형`

  ```go
  package main
   
  func nextValue() func() int {
      i := 0
      return func() int {
          i++
          return i
      }
  }
   
  func main() {
      next := nextValue()
   
      println(next())  // 1
      println(next())  // 2
      println(next())  // 3
   
      anotherNext := nextValue()
      println(anotherNext()) // 1 다시 시작
      println(anotherNext()) // 2
  }
  ```

- 위 예제와 같이 클로저 함수가 할당된 변수들은 각기 다른 함수의 실행 환경을 가지고 있음

## `defer` keyword

- `defer` 키워드는 특정 문장 혹은 함수를 `defer` 함수를 호출하는 함수가 리턴하기 직전에 실행하게 함

- `python`, `c#`, `java`에서는 `finally`와 같은 블럭으로 마지막에 `clean-up`하기 위해 사용

  ```go
  package main
   
  import "os"
   
  func main() {
      f, err := os.Open("1.txt")
      if err != nil {
          panic(err)
      }
   
      // main 마지막에 파일 close 실행
      defer f.Close()
   
      // 파일 읽기
      bytes := make([]byte, 1024)
      f.Read(bytes)
      println(len(bytes))
  }
  ```


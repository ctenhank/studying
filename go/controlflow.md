# Control Flow

## Condition Control

### `if` statement

- Go에서는 `c/c++`과 동일하게 `if`, `if-else`, `if-else if-else`와 같이 이용할 수 있음

- Go에서 `if` 조건문은 `()`를 사용하지 않아도 되지만 시작 브라켓 `{`은 반드시 `if`문과 같은 라인에 위치해야 함

- 다른 언어에서는 조건문을 숫자(`0` or `number`)로 표현할 수 있는 반면, Go에서는 반드시 **Boolean**이어야 함

  ```go
  if a == 1 {
      println("One")
  } else if a == 2 {  //같은 라인
      println("Two")
  } else {   //같은 라인
      println("Other")
  }
  ```

  

- 조건식을 사용하기 전에 Optional Statement을 실행할 수 있고, 이는 해당 `if` 문 블럭 내에서만 이용 가능

  > Optional Statement는 또한 `switch`, `for` 문 등 여러 문법에서 이용할 수 있음

  ```go
  if val := i * 2; val < max {
      println(val)
  }
   
  // 아래 처럼 Scope를 벗어나면 에러
  val++
  ```

### `switch` statement

- `switch` 문은 복잡한 `if` 문 유형들을 단순화하는데 유용

- Go에서는 다른 언어들과 다른 점들이 존재

  - `switch` 키워드 뒤에 expression이 없을 수 있음
    Go에서는 expression이 없으면 `true`라고 생각하고 첫번째 `case`로 이동

  - `case` 문에 expression을 쓸 수 있음
    다른 언어의 `case` 문은 일반적으로 리터럴 값만 갖지만, Go에서는 복잡한 expression 가능

  - `break` 키워드를 적지 않아도 됨
    다른 언어에서는 `break`를 쓰지 않는 한 다음 `case`로 넘어가지만 Go에서는 컴파일러가 자동으로 이를 추가해줌
    만약 다음 `case`로 넘어가고 싶으면 키워드 `fallthrough`를 통해 할 수 있음

  - `type` 값으로 `case`를 분기할 수 있음
    Go에서는 리터럴 값 뿐만 아니라 데이터 타입으로도 `case`를 분기할 수 있음

    ```go
    switch v.(type) {
    case int:
        println("int")
    case bool:
        println("bool")
    case string:
        println("string")
    default:
        println("unknown")
    }   
    ```

### Loop

- Go에서는 반복문을`for` 루프문으로만 가능

- 다른 언어와 비슷하게 `for 초기값; 조건식; 증감식 ` 형식을 따르지만 `괄호()`는 반드시 생략해야 함

- 경우에 따라 `초기값`, `조건식`, `증감식`은 생략 가능

  ```go
  package main
   
  func main() {
      sum := 0
      for i := 1; i <= 100; i++ {
          sum += i
      }
      println(sum)
  }
  ```

#### 조건식만 사용하는 for loop

```go
package main
 
func main() {
    n := 1
    for n < 100 {
        n *= 2      
        //if n > 90 {
        //   break 
        //}     
    }
    println(n)
}
```

#### Infinite for loop

```go
package main
 
func main() {
    for {ㅋ
        println("Infinite loop")        
    }
}
```

#### for range

- `collection`으로부터 한 `element`씩 가져와 차례로 문장들을 실행

- `for index, element:= range collection` 형식을 따름

  ```go
  names := []string{"홍길동", "이순신", "강감찬"}
   
  for index, name := range names {
      println(index, name)
  }
  ```

#### `break`, `continue`, `goto`

- 상황에 따라서 해당 키워드를 이용하여 좀 더 세부적으로 loop 문을 제어할 수 있음

- `break`: loop 종료

- `continue`: 계속해서 loop 실행

- `goto`: 특정 레이블로 가기

  ```go
  package main
  func main() {
      var a = 1
      for a < 15 {
          if a == 5 {
              a += a
              continue // for루프 시작으로
          }
          a++
          if a > 10 {
              break  //루프 빠져나옴
          }
      }
      if a == 11 {
          goto END //goto 사용예
      }
      println(a)
   
  END:
      println("End")
  }
  ```

  


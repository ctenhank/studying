# Collection in Golang

## Array

### Features

- 배열은 **연속적인 메모리 공간**에 **동일한 타입의 데이터**를 **순차적을 저장**하는 자료구조
- Go에서는 배열의 첫 번째 요소는 0번, 그 다음은 1번, 2번 등으로 인덱스를 매김

### Declaration

- 선언은 `var 변수명 [배열크기]자료형`과 같음

```go
var a [3]int
a[0] = 1
a[1] = 2
a[2] = 3
```

### Initialization

- 배열 선언과 동시에 초기화를 하면 `{}` 브라켓 안에 초기값을 순서대로 적으면 됨

- 또한, 배열크기에 `...`를 사용하여 생략하면 자동으로 초기화 요소 숫자만큼 배열크기가 정해짐

  ```go
  var a [3]int{1,2,3}
  var b [...]int{4,5}
  ```

### Mutli-Dimensional Array

- Go는 다차원 배열을 지원하는데 배열크기 부분을 복수 개로 설정하여 선언

  ```go
  var multiArray [2][3]int{
      {1,2,3},
      {4,5,6}
  }
  ```



## Slice

- Array는 고정된 배열크기 안에 동일한 타입의 데이터만 연속적으로 저장하지만, 배열의 크기를 동적으로 증가시키거나 부분 배열을 발췌하는 등의 기능은 없음
- `slice`는 배열에 기초하여 만들어졌지만, 고정된 크기를 미리 지정하지 않고, 차후 그 크기를 동적으로 변경하거나 부분 발췌가 가능함
- `slice`는 실제 배열을 가리키는 포인터 정보와 `length`, `capacity`만을 가짐

### Declaration

- Array와 동일한게 `var v []T` 형식으로 하되, 크기는 지정하지 않음

  ```go
  var a []int
  a = []int{1, 2, 3}
  ```

- 내장함수 `make()`를 이용하여 `slice`를 생성할 수 있는데 이는 `slice`의 length와 capacity를 지정할 수 있음

  - **length**는 길이를 의미하고, **capacity**는 최대 길이를 의미
  - 위 두 가지 값을 지정하면 모든 요소가 `Zero Value`인 슬라이스를 만듬
  - **capacity**를 지정하지 않으면 **length**과 같은 값을 자동으로 지정함
  - 내장함수 `len()`, `cap()`을 통해 위 두 가지 값을 확인할 수 있음

  ```go
  s := make([]int, 5, 10)
  ```

  - 만약 length와 capacity를 지정하지 않으면, 기본적으로 길이와 용량이 0인 슬라이스를 만듬

    - 이를 `Nil Slice`라 하며, `nil`과 비교하면 `true`를 반환

    ```go
    func main() {
        var s []int
     
        if s == nil {
            println("Nil Slice")
        }
        println(len(s), cap(s)) // 모두 0
    }
    ```

### Sub-slice

- Go에서는 슬라이스 일부를 발췌하여 부분 슬라이스를 만들 수 있음

- `Slice[inclusive:exclusive]` 형식으로 만들 수 있음

  > inclusive는 부분 슬라이스의 처음 인덱스이며, exclusive는 마지막 인덱스

- 예를 들어, 인덱스 2번부터 4까지 데이터를 갖는 부분 슬라이스를 만들려면 **[2:4]**가 아니라 **[2:5]**라 써야함

  ```go
  s := []int{0, 1, 2, 3, 4, 5}
      s = s[2:5]  
      fmt.Println(s) //2,3,4 출력
  ```

- `inclusive` 또는 `exclusive`를 생략할 수 있는데 자동으로 슬라이스의 처음 인덱스 또는 마지막 인덱스를 가리킴

  ```go
  s := []int{0, 1, 2, 3, 4, 5}
  s = s[:4]     // 0, 1, 2, 3
  s = s[1:]      // 1, 2, 3
  ```

### Slice append and copy

- `slice`는 내장함수 `append()`를 통해 자유롭게 여러 개의 새로운 요소를 추가하거나 `slice`들을 병합할 수 있음

- `append(slice, e0, e1, ...)` 형식을 가짐

  - 첫 번째 파라미터에는 새로운 요소를 추가 할 슬라이스
  - 두 번째 파라미터부터는 추가할 요소의 값들

- 두 개 이상의 슬라이스를 병합하는 방법은 아래와 같음

  - 슬라이스의 특정 요소만 추가

    `append(sliceA, sliceB[0], ...)`

  - 슬라이스 전체를 병합, 전체 병합할 슬라이스 뒤에 `...` 문자를 추가해줌

    `append(sliceA, sliceB...)`

- 동작 원리는 다음과 같음

  - `capacity`가 남아 있는 경우
    `length` 값을 변경하여 데이터를 추가
  - `capacity`가 없는 경우
    - 현재 `capacity`의 2배에 해당하는 새로운 배열에 값들을 복제하고 다시 `slice`에 할당

### Internal Structure of Slice

- 슬라이스는 내부적으로 사용하는 배열의 부분 영역인 세그먼트에 대한 메타데이터만 가지고 있음
- 슬라이스는 크게 세 개의 필드로 구성되어 있음
  - 내부적으로 사용하는 배열에 대한 포인터 정보
  - 세그먼트 길이(length)
  - 세그먼트 최대 용량(capacity)

![Image](http://golang.site/images/basics/go-slice-internal.png)

## Map

### Features

- Map은 `key`에 대응하는 `value`를 신속히 찾는 **Hash table**을 구현한 자료구조

### Declaration

- 선언은 `var 변수명 map[key타입]value타입`과 같음

  ```go
  var idMap map[int]string
  ```

- 선언된 변수는 `reference` 타입이므로 `nil` 값을 가지며, 이를 `Nil Map`이라 부름

- `Nil Map`에서는 어떤 데이터도 쓸 수 없는데, `map`을 초기화하기 위해 여러 방법이 존재

  - `make()` 내장함수를 이용하는데, 이는 hash table 자료구조를 메모리에 생성하고 그 메모리를 가리키는 포인터 `runtime.hmap struct`를 리턴

    ```go
    idMap = make(map[int]string)
    ```

  - 리터럴(literal)을 사용해서 초기화할 수도 있음

    ```go
    tickers := map[string]string{
        "GOOG": "Google Inc",
        "MSFT": "Microsoft",
        ...
    }
    ```

### Usage

- `make()`함수를 통해 초기화 됐을 때는, 아무런 데이터가 없는 상태

- 데이터를 추가하기 위해서는 `map변수[key]=value`와 같이 할당

- 특정 `key`를 읽을 때는 `map변수[key]` 형식으로 읽으면 됨

  - `map`안에 찾는 `key`가 존재하지 않는다면 `reference`일 때는 `nil`, `value` 일때는 `zero` 리턴

- 특정 `key`와 `value`를 삭제하려면 `delete()` 함수를 이용

- `for` 루프를 사용하여 `map` 열거할 수도 있음

  ```go
  var m map[int]string
   
  m = make(map[int]string)
  //추가 혹은 갱신
  m[901] = "Apple"
  m[134] = "Grape"
  m[777] = "Tomato"
  
  // 키에 대한 값 읽기
  str := m[134]
  println(str)
  
  noData := m[999] // 값이 없으면 nil 혹은 zero 리턴
  println(noData)
  
  for key, val := range myMap {
      println(key, val)
  }
  
  // 삭제
  delete(m, 777)
  ```




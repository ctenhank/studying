# User-defined Data Type

### Struct in Golang

#### Features

- Go에서 `struct`는 user-defined data type을 표현하는데 사용
- Go에서는 일반적인 OOP 언어의 `class`, `object`, `inheritance` 개념이 없음
- `class` 개념은 Go에서는 `struct`로 표현되는데, `class`와 달리 Go의 `struct`는 필드값만 가짐
- `struct`는 mutable 개체로서 필드값이 변경될 경우 해당 개체 메모리에서 직접 변경됨
- `struct`를 다른 함수의 파라미터로 넘긴다면 `pass by value`에 따라 객체를 복사해서 전달하며, `pass by reference`로 전달하려면 `struct`의 포인터를 전달해야 함

#### Declaration

- Go에서는 `struct`를 정의하기 위해서는 Custom Type을 정의하는데 사용하는 `type` 문을 사용

  ```go
  // struct 정의
  // struct 이름이 person의 첫글자는 'p'이므로 패키지 외부에서는 사용할 수 없음
  type person struct {
      name string
      age  int
  }
  ```

#### Create struct object

- 선언된 `struct`  타입으로부터 객체를 생성하는 방법은 몇 가지가 있음

  - 아래 예제처럼 빈 객체를 먼저 생성하고, 나중에 필드값을 채워넣는 방법

    - 객체의 필드에 접근하기 위해서는 `.`(dot) 연산자를 이용

    ```go
    // struct 정의
    type person struct {
        name string
        age  int
    }
     
    func main() {
        // person 객체 생성
        p := person{}
         
        // 필드값 설정
        p.name = "Lee"
        p.age = 10
         
        fmt.Println(p)
    }
    ```

  - 객체를 생성할 때, 초기값을 함께 할당하는 방법

    - 초기값을 할당할 때는 순서대로 넣는 방법과 필드명을 지정하고 그 값을 넣을 수도 있음

    ```go
    var p1 person 
    p1 = person{"Bob", 20}
    p2 := person{name: "Sean", age: 50}
    ```

  - Go 내장함수 `new()`를 사용하는 방법

    - `new()`를 사용하면 모든 필드는 `Zero Value`로 초기화하며 객체의 포인터를 리턴함
    - Go에서 객체 포인터 접근은 `c/c++`의 `->` 연산자와는 달리 `.`(dot) 연산자를 이용함

#### Constructor Function

- 때때로 구조체 필드가 사용되기 전에 초기화해야 하는 경우가 있음

  > 예를 들어 `struct`의 필드가 [`map`](collection.md/#Map)인 경우
  >
  > `map`은 무조건 초기화를 하여야 사용할 수 있는데, 초기화해서 `struct` 넘겨주면 이에 대해 신경 쓸 필요가 없음

  ```go
  package main
   
  type dict struct {
      data map[int]string
  }
   
  //생성자 함수 정의
  func newDict() *dict {
      d := dict{}
      d.data = map[int]string{}
      return &d //포인터 전달
  }
   
  func main() {
      dic := newDict() // 생성자 호출
      dic.data[1] = "A"
  }
  ```




### Method in Golang

#### Features

- 앞서 `struct`에서 살펴본 것과 같이 `method`는 `struct`와 별도로 분리되어 정의됨

- `method`는 특별한 형태의 `func` 함수인데, `func` 키워드와 함수명 사이에 `receiver`가 존재
  `func receiver func_name(parameters...) return_type {}`

- `receiver`는 그 함수가 어떤 struct를 위한 method인지 표시해주는 역할로 `struct_변수명 struct_type`로 구성

  ```go
  //Rect - struct 정의
  type Rect struct {
      width, height int
  }
   
  //Rect의 area() 메소드
  func (r Rect) area() int {
      return r.width * r.height   
  }
   
  func main() {
      rect := Rect{10, 20}
      area := rect.area() //메서드 호출
      println(area)
  }
  ```

#### Value vs Pointer Receiver

- `receiver`는 `value` 타입과 `pointer` 타입이 존재하는데, 이는 변수의 특징과 동일

  - `receiver`를 `value` 타입으로 선언했으면, `struct`의 데이터를 복사하여 전달
  - `receiver`를 `pointer` 타입으로 선언했으면, `struct`의 주소를 전달

  ```go
  // 포인터 Receiver
  func (r *Rect) area2() int {
      r.width++
      return r.width * r.height
  }
   
  func main() {
      rect := Rect{10, 20}
      area := rect.area2() //메서드 호출
      println(rect.width, area) // 11 220 출력
  }
  ```

  

### Interface in Golang

#### Features

- `struct`가 필드들의 집합체이면, `interface`는 `method`들의 집합체
- `interface`는 `type`이 구현해야 하는 `method prototype`들을 정의
- `interface`를 구현하려면 그 안의 모든 `method`들을 구현해야 함

#### Usage Interface

- `interface`를 사용하는 일반적인 예로 함수가 파라미터로 `interface`를 받아들이는 경우

- 이는 해당 `interface`를 구현하기만 하면 어떤 타입이든 입력 파라미터로 사용할 수 있다는 것

  ```go
  type Shape interface {
      area() float64
      perimeter() float64
  }
  
  //Rect 정의
  type Rect struct {
      width, height float64
  }
   
  //Circle 정의
  type Circle struct {
      radius float64
  }
   
  //Rect 타입에 대한 Shape 인터페이스 구현 
  func (r Rect) area() float64 { return r.width * r.height }
  func (r Rect) perimeter() float64 {
       return 2 * (r.width + r.height)
  }
   
  //Circle 타입에 대한 Shape 인터페이스 구현 
  func (c Circle) area() float64 { 
      return math.Pi * c.radius * c.radius
  }
  func (c Circle) perimeter() float64 { 
      return 2 * math.Pi * c.radius
  }
  
  func main() {
      r := Rect{10., 20.}
      c := Circle{10}
   
      showArea(r, c)
  }
   
  func showArea(shapes ...Shape) {
      for _, s := range shapes {
          a := s.area() //인터페이스 메서드 호출
          println(a)
      }
  }
  ```


#### Interface Type

- Go언어에서는 흔히 `empty interface`를 자주 사용하는데, 흔히 `interface type`이라고 함

- `interface type`은 `interface{}`와 같이 표현하며, `method`를 전혀 가지고 있지 않는 `interface` 

- 즉 어떤 `method`도 구현할 필요 없으니 어떤 타입이든 입력 파라미터로 사용할 수 있다는 의미

  > `c/c++`에서 `void*`, `C#`, `Java`에서는 `object`라 볼 수 있음

  ```go
  func main() {
      var x interface{}
      x = 1 
      x = "Tom"
   
      printIt(x)
  }
   
  func printIt(v interface{}) {
      fmt.Println(v) //Tom
  }
  ```

#### Type Assertion

- 만약 변수의 자료형이 `interface`라면, `x.(Type)`로 표현할 수 있음

- `x.(Type)`은 x가 Type에 속하는 지 **확인(assert)**하는 것으로 이를 **Type Assertion**이라 함

- Type에 속하지 않는다면 런타임 에러가 발생하고, 맞다면 해당 값을 할당

  ```go
  func main() {
      var a interface{} = 1
   
      i := a       // a와 i 는 dynamic type, 값은 1
      j := a.(int) // j는 int 타입, 값은 1
   
      println(i)  // 포인터주소 출력
      println(j)  // 1 출력
  }
  ```

  
























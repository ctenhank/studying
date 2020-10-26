# Errors

## Exception in Golang

### Features

- Go는 내장 타입으로 `error`라는 `interface` 타입을 가짐

- Go 에러는 이 `error interface`를 통해서 주고 받는데, 이 `interface`는 다음과 같은 하나의 `method`를 가짐

  ```go
  type error interface {
      Error() string
  }
  ```

- 개발자는 이를 통해 custom error type을 구현할 수 있음

### Handling Error Exception

- Go 함수가 결과와 에러를 함께 리턴한다면, 이 에러가 `nil`인지 체크해서 확인할 수 있음

- 아래 예제를 보면 `os.Open()` 함수는 리턴 값으로 첫 번째는 파일 포인터를, 두 번째는 `error interface` 반환

  ```go
  // os.Open() function
  func Open(name string) (file *File, err error) 
  
  func main(){
      path := '~/Downloads/SOMETHINGS'
      f, err := os.Open(path)
      // error가 nil이 아니라면 error가 발생했으니 그 error를 출력
      if err != nil {
          log.Fatal(err.Error())
      }
      // error가 발생하지 않음
      println(f.Name())
  }
  ```

- 또는 `error`의 `Type`을 확인해서 별도의 에러 처리를 하는 방식이 있음 

  ```go
  _, err := otherFunc()
  switch err.(type) {
  default: // no error
      println("ok")
  case MyError:
      log.Print("Log my error")
  case error:
      log.Fatal(err.Error())
  }
  ```

## `panic` and `recover` Function

### `panic()`

- `panic()` 함수는 현재 함수를 즉시 멈추고 현재 함수의 `defer` 함수들을 모두 실행한 후 즉시 리턴
- `panic` 모드 실행 방식은 다시 상위 함수에도 똑같이 적용되고, 계속해서 콜스택을 타고 올라가며 적용됨
- 마지막에는 프로그램이 에러를 내고 종료하게 됨

### `recover()`

- `recover()` 함수는 `panic()` 상태를 다시 정상상태로 되돌리는 함수

```go
package main
 
import (
    "fmt"
    "os"
)

// first
func main() {
    // 잘못된 파일명을 넣음
    openFile("Invalid.txt")
     
    // openFile() 안에서 panic이 실행되면
    // 아래 println 문장은 실행 안됨
    println("Done") 
}
 
// second
func main() {
    // 잘못된 파일명을 넣음
    openFile("Invalid.txt")
 
    // recover에 의해
    // 이 문장 실행됨
    println("Done") 
}
 
func openFile(fn string) {
    // defer 함수. panic 호출시 실행됨
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("OPEN ERROR", r)
        }
    }()
 
    f, err := os.Open(fn)
    if err != nil {
        panic(err)
    }
 
    defer f.Close()
}
```




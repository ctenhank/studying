# Exception in Golang

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

  


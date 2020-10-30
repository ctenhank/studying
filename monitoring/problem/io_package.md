# ReaderCloser

 중 17개의 함수는 **Golang** 표준 라이브러리 `io` 패키지를 이용한다.이 패키지에서 `io.Reader` 또는 그 외의 `io.Writer` 등 여러 인터페이스 및 메서드들을 이용되는데 이에 대해 알아볼 것이다.

> [`io`](../../language/go/packages/io.md) 패키지에 대해서 더 자세히 알아보고 싶으면 해당 링크에 들어간다. 

### Problem

`ContainerLogs` 함수를 구현하여 출력값을 받아 출력을 해보니 다음과 같이 출력된다.

```go
reader, err := cli.ContainerLogs(context.Background(), container.ID, types.ContainerLogsOptions{ShowStdout:true})
if err != nil{
    panic(err)
}
fmt.Printf("%+v\n", reader)

//------output--------
//&{body:0xc0002f0400 mu:{state:0 sema:0} closed:false rerr:<nil> fn:0x7685c0 earlyCloseFn:0x768540}
```

- 출력에서 `{…}`는 `map` 또는 `struct`를 의미하나?: `struct`를 의미한다.

  ```go
  m := make(map[int]string)
  m[0] = "str"
  m[5] = "5"
  t := test{0, 1, "abc", 1.0}
  fmt.Printf("%+v\n", t)
  fmt.Printf("%+v\n", m)
  
  //----output-----
  //{a:0 b:1 str:abc f:1}
  //map[0:str 5:5]
  ```

- `&{...}`는 무엇일까?

### Answer

#### `io.Copy()`

이를 해결하기 위해서는 여러 가지 방법이 있을 수 있지만, 우선 `io` 패키지의 `Copy(dst, src)` 란 함수를 이용한다.

```go
func Copy(dst Writer, src Reader) (written int64, err error)
```

`io.Copy` 함수는 `src`에서 `EOF`가 반환되거나 에러가 발생하기 전까지 `dst`로 복사한다. 함수가 종료되면 복사된 `byte`의 수와 에러를 반환해준다. 만약 `err==EOF || err==nil`이면 함수가 성공적으로 끝난 것이다. 여기서 `Reader` 인터페이스 `src`는 `io.WriteTo`라는 인터페이스를 구현하여 `dst`로 복사하는데, 이게 아니라면 `dst`가 `io.ReaderFrom`이라는 인터페이스 구현을 통해 복사할 수 있다.

위의 `io.Copy`를 함수를 이용해서 아래와 같이 구현하고 위의 이상한(?) 출력과 비교해보자.

```go
reader, err := cli.ContainerLogs(context.Background(), container.ID, types.ContainerLogsOptions{ShowStdout:true})
if err != nil{
    panic(err)
}

_, err = io.Copy(os.Stdout, reader)
if err != nil && err != io.EOF{
    panic(err)
}

fmt.Printf("%+v\n", reader)

/* Output
~/project/monitoring # git init
Initialized empty Git repository in /root/project/monitoring/.git/
~/project/monitoring # ls -a
.     ..    .git
*/
```



### `io.Copy` 함수 이용 방법들

`io.copy()`를 이용해 입력값들을 어떻게 출력할 것인가에 대해 고민해볼 수 있다. 

- `stdout`에 출력하는 방법
  [Answer](#Answer)와 동일하니 참고하자.

- **파일**에 저장하는 방법

  ```go
  reader, err := cli.ContainerLogs(context.Background(), container.ID, types.ContainerLogsOptions{ShowStdout:true})
  if err != nil{
      panic(err)
  }
  
  var fp *os.File
  fp, err = os.Create("logs")
  if err != nil {
      panic(err)
  }
  
  _, err = io.Copy(fp, reader)
  if err != nil {
      panic(err)
  }
  
  /*
  cat ./logs
  ~/project/monitoring # git init
  Initialized empty Git repository in /root/project/monitoring/.git/
  ~/project/monitoring # ls -a
  .     ..    .git
  */
  ```

- **변수**에 저장하는 방법

  변수에 저장하기 위해서는 `strings` 패키지의 구조체 `Builder`를 이용해야한다.

  ```go
  reader, err := cli.ContainerLogs(context.Background(), container.ID, types.ContainerLogsOptions{ShowStdout:true})
  if err != nil{
      panic(err)
  }
  
  var builder strings.Builder
  _, err = io.Copy(&builder, reader)
  if err != nil && err != io.EOF{
      panic(err)
  }
  fmt.Println(builder.String())
  ```

  #### 구조체 `Builder`에 대해 알아보자

  구조체 `Builder`는 다음과 같이 주소값 `addr`과 byte 슬라이스 `buf`와 구성되어 있다.

  ```go
  // A Builder is used to efficiently build a string using Write methods.
  // It minimizes memory copying. The zero value is ready to use.
  // Do not copy a non-zero Builder.
  type Builder struct {
  	addr *Builder // of receiver, to detect copies by value
  	buf  []byte
  }
  ```

  또한 `Builder`를 선언하면 자체적으로 다양한 많은 함수들을 지원하는데 다음과 같다. 그 중 `String()` 함수를 이용하면 `string  `값을 얻을 수 있다.

  ```go
  func (b *Builder) copyCheck() {
  	if b.addr == nil {
  		// This hack works around a failing of Go's escape analysis
  		// that was causing b to escape and be heap allocated.
  		// See issue 23382.
  		// TODO: once issue 7921 is fixed, this should be reverted to
  		// just "b.addr = b".
  		b.addr = (*Builder)(noescape(unsafe.Pointer(b)))
  	} else if b.addr != b {
  		panic("strings: illegal use of non-zero Builder copied by value")
  	}
  }
  
  // String returns the accumulated string.
  func (b *Builder) String() string 
  
  // Len returns the number of accumulated bytes; b.Len() == len(b.String()).
  func (b *Builder) Len() int
  
  // Cap returns the capacity of the builder's underlying byte slice. It is the
  // total space allocated for the string being built and includes any bytes
  // already written.
  func (b *Builder) Cap() int 
  
  // Reset resets the Builder to be empty.
  func (b *Builder) Reset() {
  
  // grow copies the buffer to a new, larger buffer so that there are at least n
  // bytes of capacity beyond len(b.buf).
  func (b *Builder) grow(n int) 
  
  // Grow grows b's capacity, if necessary, to guarantee space for
  // another n bytes. After Grow(n), at least n bytes can be written to b
  // without another allocation. If n is negative, Grow panics.
  func (b *Builder) Grow(n int) 
  
  // Write appends the contents of p to b's buffer.
  // Write always returns len(p), nil.
  func (b *Builder) Write(p []byte) (int, error) 
  
  // WriteByte appends the byte c to b's buffer.
  // The returned error is always nil.
  func (b *Builder) WriteByte(c byte) error 
  
  // WriteRune appends the UTF-8 encoding of Unicode code point r to b's buffer.
  // It returns the length of r and a nil error.
  func (b *Builder) WriteRune(r rune) (int, error) 
  
  // WriteString appends the contents of s to b's buffer.
  // It returns the length of s and a nil error.
  func (b *Builder) WriteString(s string) (int, error) 
  ```

  


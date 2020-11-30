# 

### Problems

`go get github.com/docker/docker`를 이용하면 `go get`은 해당 url, `github.com/docker/docker`의 **branch** 중에서 하나를 선택해서 다운로드한다. 다운로드된 태그, 즉 버전은 `v1.3.x`이다. 해당 버전의 소스코드를 확인해보면 NewClientWithOpts라는 함수가 정의되어 있지 않음을 확인할 수 있다.

#### Solution

`go get github.com/docker/docker@master` 명령문을 통해서 가장 최신 버전, 즉 현재 `master` branch 버전을 다운로드 받을 수 있다.[[1]][1]

## Reference

[1]: https://www.reddit.com/r/AskProgramming/comments/atmoqa/cant_compile_sample_golang_code_from_docker/


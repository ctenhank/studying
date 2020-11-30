# Command: `docker stats`

### `docker stats` 설정사항 구조체

```go
type ContainerStatsConfig struct {
	Stream    bool
	OneShot   bool
	OutStream io.Writer
	Version   string
}
```

- `Stream`, `Oneshot`은 계속해서 할 것인지 한 번만 할 것인지 정하는 것
- `OutStream`은 쓰는 `io` 변수
# Command Information

이 글은 모니터링 시스템 컴포넌트 중 서비스 디스커버리, 도커의 모니터링을 위해 필요한 명령어들 리스트들에 대한 것이다.

https://godoc.org/github.com/docker/docker/client#Client.ContainerList

### Single Mode(without `docker swarm`)

#### `docker diff`

```go
func (cli *Client) ContainerDiff(ctx context.Context, containerID string) ([]container.ContainerChangeResponseItem, error)
```

#### `docker inspect`

```go
func (cli *Client) ContainerInspect(ctx context.Context, containerID string) (types.ContainerJSON, error)
```

#### `docker ps`

```go
func (cli *Client) ContainerList(ctx context.Context, options types.ContainerListOptions) ([]types.Container, error)
```

#### `docker logs`

```go
func (cli *Client) ContainerLogs(ctx context.Context, container string, options types.ContainerLogsOptions) (io.ReadCloser, error)
```

#### `docker stats`

```go
func (cli *Client) ContainerStats(ctx context.Context, containerID string, stream bool) (types.ContainerStats, error)
```

#### `docker stats --no-stream`

```go
func (cli *Client) ContainerStatsOneShot(ctx context.Context, containerID string) (types.ContainerStats, error)
```

#### `docker top`

```go
func (cli *Client) ContainerTop(ctx context.Context, containerID string, arguments []string) (container.ContainerTopOKBody, error)
```

#### `docker event`

```go
func (cli *Client) Events(ctx context.Context, options types.EventsOptions) (<-chan events.Message, <-chan error)
```

#### `docker info`

```go
func (cli *Client) Info(ctx context.Context) (types.Info, error)
```



### `docker swarm` Mode

- [func (cli *Client) NodeInspectWithRaw(ctx context.Context, nodeID string) (swarm.Node, [\]byte, error)](https://godoc.org/github.com/docker/docker/client#Client.NodeInspectWithRaw)
- [func (cli *Client) NodeList(ctx context.Context, options types.NodeListOptions) ([\]swarm.Node, error)](https://godoc.org/github.com/docker/docker/client#Client.NodeList)
- [func (cli *Client) NodeRemove(ctx context.Context, nodeID string, options types.NodeRemoveOptions) error](https://godoc.org/github.com/docker/docker/client#Client.NodeRemove)
- [func (cli *Client) NodeUpdate(ctx context.Context, nodeID string, version swarm.Version, node swarm.NodeSpec) error](https://godoc.org/github.com/docker/docker/client#Client.NodeUpdate)

- [func (cli *Client) ServiceCreate(ctx context.Context, service swarm.ServiceSpec, options types.ServiceCreateOptions) (types.ServiceCreateResponse, error)](https://godoc.org/github.com/docker/docker/client#Client.ServiceCreate)
- [func (cli *Client) ServiceInspectWithRaw(ctx context.Context, serviceID string, opts types.ServiceInspectOptions) (swarm.Service, [\]byte, error)](https://godoc.org/github.com/docker/docker/client#Client.ServiceInspectWithRaw)
- [func (cli *Client) ServiceList(ctx context.Context, options types.ServiceListOptions) ([\]swarm.Service, error)](https://godoc.org/github.com/docker/docker/client#Client.ServiceList)
- [func (cli *Client) ServiceLogs(ctx context.Context, serviceID string, options types.ContainerLogsOptions) (io.ReadCloser, error)](https://godoc.org/github.com/docker/docker/client#Client.ServiceLogs)
- [func (cli *Client) ServiceRemove(ctx context.Context, serviceID string) error](https://godoc.org/github.com/docker/docker/client#Client.ServiceRemove)
- [func (cli *Client) ServiceUpdate(ctx context.Context, serviceID string, version swarm.Version, service swarm.ServiceSpec, options types.ServiceUpdateOptions) (types.ServiceUpdateResponse, error)](https://godoc.org/github.com/docker/docker/client#Client.ServiceUpdate)
- [func (cli *Client) SetCustomHTTPHeaders(headers map[string\]string)](https://godoc.org/github.com/docker/docker/client#Client.SetCustomHTTPHeaders)
- [func (cli *Client) SwarmGetUnlockKey(ctx context.Context) (types.SwarmUnlockKeyResponse, error)](https://godoc.org/github.com/docker/docker/client#Client.SwarmGetUnlockKey)
- [func (cli *Client) SwarmInit(ctx context.Context, req swarm.InitRequest) (string, error)](https://godoc.org/github.com/docker/docker/client#Client.SwarmInit)
- [func (cli *Client) SwarmInspect(ctx context.Context) (swarm.Swarm, error)](https://godoc.org/github.com/docker/docker/client#Client.SwarmInspect)
- [func (cli *Client) SwarmJoin(ctx context.Context, req swarm.JoinRequest) error](https://godoc.org/github.com/docker/docker/client#Client.SwarmJoin)
- [func (cli *Client) SwarmLeave(ctx context.Context, force bool) error](https://godoc.org/github.com/docker/docker/client#Client.SwarmLeave)
- [func (cli *Client) SwarmUnlock(ctx context.Context, req swarm.UnlockRequest) error](https://godoc.org/github.com/docker/docker/client#Client.SwarmUnlock)
- [func (cli *Client) SwarmUpdate(ctx context.Context, version swarm.Version, swarm swarm.Spec, flags swarm.UpdateFlags) error](https://godoc.org/github.com/docker/docker/client#Client.SwarmUpdate)

$$
1 + 3.3log_{10}n
$$




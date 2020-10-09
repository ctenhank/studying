# Docker

 도커는 컨테이너 가상화 기술인데, 매우 가벼운 가상머신(VM)과 같다. 컨테이너를 구축하는 것에다가, 개발자가 컨테이너와 컨테이너 안에 어플리케이션을 구축하고, 그러한 것들을 동료들과 공유할 수 있는 워크플로우를 제공해준다. 또한 개발 환경을 컨테이너 레이어로 설치하기 때문에 개발 배포에도 매우 효율적이다.

- 도커는 LXC를 프로세스 실행을 고립시키기 위해 커널, 어플리케이션 수준의 API와 함께 확장했다.(cgroups)

  > CPU, 메모리, I/O, 네트워크 등

- 도커는 또한 운영체제 기반의 어플리케이션 관점을 완전히 고립시키기 위해 리눅스 커널 네임스페이스를 이용한다.(namespaces)

  > 프로세스 트리, 네트워크, 사용자 ID, 파일 시스템

- 도커 컨테이너는 base image를 이용하여 생성되는데, 이는 OS의 기초적인 것들과 다른 응용 프로그램들로 이루어 질 수 있다.

- Dokcerfiles를 다양한 명령어를 이용하여 수동/자동으로 실행할 수 있고, 이를 통해 base image를 새로운 image로 형성 또는 만들 수 잇다.

- 컨테이너는 VM에서 실행할 수 있다.

- 도커는 사용자 모드 코드에 isolated enviroment 환경을 제공해주는데 



## Architecture

### Client

```go
type Client struct {
	// scheme sets the scheme for the client
	scheme string
	// host holds the server address to connect to
	host string
	// proto holds the client protocol i.e. unix.
	proto string
	// addr holds the client address.
	addr string
	// basePath holds the path to prepend to the requests.
	basePath string
	// client used to send and receive http requests.
	client *http.Client
	// version of the server to talk to.
	version string
	// custom http headers configured by users.
	customHTTPHeaders map[string]string
	// manualOverride is set to true when the version was set by users.
	manualOverride bool

	// negotiateVersion indicates if the client should automatically negotiate
	// the API version to use when making requests. API version negotiation is
	// performed on the first request, after which negotiated is set to "true"
	// so that subsequent requests do not re-negotiate.
	negotiateVersion bool

	// negotiated indicates that API version negotiation took place
	negotiated bool
}
```

### Deamon

```go
type Daemon struct {
	ID                string
	repository        string
	containers        container.Store
	containersReplica container.ViewDB
	execCommands      *exec.Store
	imageService      *images.ImageService
	idIndex           *truncindex.TruncIndex
	configStore       *config.Config
	statsCollector    *stats.Collector
	defaultLogConfig  containertypes.LogConfig
	RegistryService   registry.Service
	EventsService     *events.Events
	netController     libnetwork.NetworkController
	volumes           *volumesservice.VolumesService
	discoveryWatcher  discovery.Reloader
	root              string
	seccompEnabled    bool
	apparmorEnabled   bool
	shutdown          bool
	idMapping         *idtools.IdentityMapping
	// TODO: move graphDrivers field to an InfoService
	graphDrivers map[string]string // By operating system

	PluginStore           *plugin.Store // todo: remove
	pluginManager         *plugin.Manager
	linkIndex             *linkIndex
	containerdCli         *containerd.Client
	containerd            libcontainerdtypes.Client
	defaultIsolation      containertypes.Isolation // Default isolation mode on Windows
	clusterProvider       cluster.Provider
	cluster               Cluster
	genericResources      []swarm.GenericResource
	metricsPluginListener net.Listener

	machineMemory uint64

	seccompProfile     []byte
	seccompProfilePath string

	diskUsageRunning int32
	pruneRunning     int32
	hosts            map[string]bool // hosts stores the addresses the daemon is listening on
	startupDone      chan struct{}

	attachmentStore       network.AttachmentStore
	attachableNetworkLock *locker.Locker
}

```



### Object

- #### container

```go
type Container struct {
	StreamConfig *stream.Config
	// embed for Container to support states directly.
	*State          `json:"State"`          // Needed for Engine API version <= 1.11
	Root            string                  `json:"-"` // Path to the "home" of the container, including metadata.
	BaseFS          containerfs.ContainerFS `json:"-"` // interface containing graphdriver mount
	RWLayer         layer.RWLayer           `json:"-"`
	ID              string
	Created         time.Time
	Managed         bool
	Path            string
	Args            []string
	Config          *containertypes.Config
	ImageID         image.ID `json:"Image"`
	NetworkSettings *network.Settings
	LogPath         string
	Name            string
	Driver          string
	OS              string
	// MountLabel contains the options for the 'mount' command
	MountLabel             string
	ProcessLabel           string
	RestartCount           int
	HasBeenStartedBefore   bool
	HasBeenManuallyStopped bool // used for unless-stopped restart policy
	MountPoints            map[string]*volumemounts.MountPoint
	HostConfig             *containertypes.HostConfig `json:"-"` // do not serialize the host config in the json, otherwise we'll make the container unportable
	ExecCommands           *exec.Store                `json:"-"`
	DependencyStore        agentexec.DependencyGetter `json:"-"`
	SecretReferences       []*swarmtypes.SecretReference
	ConfigReferences       []*swarmtypes.ConfigReference
	// logDriver for closing
	LogDriver      logger.Logger  `json:"-"`
	LogCopier      *logger.Copier `json:"-"`
	restartManager restartmanager.RestartManager
	attachContext  *attachContext

	// Fields here are specific to Unix platforms
	AppArmorProfile string
	HostnamePath    string
	HostsPath       string
	ShmPath         string
	ResolvConfPath  string
	SeccompProfile  string
	NoNewPrivileges bool

	// Fields here are specific to Windows
	NetworkSharedContainerID string            `json:"-"`
	SharedEndpointList       []string          `json:"-"`
	LocalLogCacheMeta        localLogCacheMeta `json:",omitempty"`
}
```

- Image

```go
// V1Image stores the V1 image configuration.
type V1Image struct {
	// ID is a unique 64 character identifier of the image
	ID string `json:"id,omitempty"`
	// Parent is the ID of the parent image
	Parent string `json:"parent,omitempty"`
	// Comment is the commit message that was set when committing the image
	Comment string `json:"comment,omitempty"`
	// Created is the timestamp at which the image was created
	Created time.Time `json:"created"`
	// Container is the id of the container used to commit
	Container string `json:"container,omitempty"`
	// ContainerConfig is the configuration of the container that is committed into the image
	ContainerConfig container.Config `json:"container_config,omitempty"`
	// DockerVersion specifies the version of Docker that was used to build the image
	DockerVersion string `json:"docker_version,omitempty"`
	// Author is the name of the author that was specified when committing the image
	Author string `json:"author,omitempty"`
	// Config is the configuration of the container received from the client
	Config *container.Config `json:"config,omitempty"`
	// Architecture is the hardware that the image is built and runs on
	Architecture string `json:"architecture,omitempty"`
	// Variant is the CPU architecture variant (presently ARM-only)
	Variant string `json:"variant,omitempty"`
	// OS is the operating system used to build and run the image
	OS string `json:"os,omitempty"`
	// Size is the total size of the image including all layers it is composed of
	Size int64 `json:",omitempty"`
}

// Image stores the image configuration
type Image struct {
	V1Image
	Parent     ID        `json:"parent,omitempty"` //nolint:govet
	RootFS     *RootFS   `json:"rootfs,omitempty"`
	History    []History `json:"history,omitempty"`
	OSVersion  string    `json:"os.version,omitempty"`
	OSFeatures []string  `json:"os.features,omitempty"`

	// rawJSON caches the immutable JSON associated with this image.
	rawJSON []byte

	// computedID is the ID computed from the hash of the image config.
	// Not to be confused with the legacy V1 ID in V1Image.
	computedID ID
}
```



``` mermaid


```


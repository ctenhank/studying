# Linux Kernel Namespaces

### Overview

-   네임스페이스는 글로벌 시스템 리소스를 추상화로 감싸는데, 이는 그 네임스페이스에 속한 프로세스에게 자신의 격리된 글로벌 리소스 인스턴스를 가진 것처럼 보이게 해준다. 글로벌 리소스에서 네임스페이스 변경은 글로벌 네임스페이스 멤버인 프로세스들에게는 보이지만, 다른 프로세스들에게는 보이지 않는다.

  > A namespace wraps a global system resource in an abstraction that makes it appear to the processes within the namespace that  they  have  their ow n  isolated  instance  of the global resource.  Changes to the global resource are visible to other processes that are members of the  namespace,  but  are invisible to other processes.  One use of namespaces is to implement containers.[[1]](https://man7.org/linux/man-pages/man7/namespaces.7.html)

-  리눅스 커널은 총 7개의 네임스페이스를 제공

   [Mount Namespace](#Mount Namespace), [UTS Namespace](#UTS Namespace), [IPC Namespace](#IPC Namespace), [PID Namespace](#PID Namespace), [User Namespace](#User Namespace), [Network Namespace](#Network Namespace), [Cgroup Namespace](#Cgroup Namespace)

- 네임스페이스 생성과 삭제를 위해 세 가지 API 제공

  [clone](#clone), [setns](#setns), [unshare](#unshare)

-  모든 프로세스는 `/proc/$$/ns`에 각 네임스페이스에 대해 속해있으며, 네임스페이스는 **10 자리수 inode **이루어짐

  ```bash
  #example in my env
  $ uname -a
  Linux host 5.4.0-42-generic 46~18.04.1-Ubuntu SMP Fri Jul 10 07:21:24 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
  
  $ ls -al /proc/$$/ns
  total 0
  dr-x--x--x 2 root root 0 Oct  6 12:56 .
  dr-xr-xr-x 9 root root 0 Oct  6 12:56 ..
  lrwxrwxrwx 1 root root 0 Oct  6 12:56 cgroup -> 'cgroup:[4026531835]'
  lrwxrwxrwx 1 root root 0 Oct  6 12:56 ipc -> 'ipc:[4026531839]'
  lrwxrwxrwx 1 root root 0 Oct  6 12:56 mnt -> 'mnt:[4026531840]'
  lrwxrwxrwx 1 root root 0 Oct  6 12:56 net -> 'net:[4026532008]'
  lrwxrwxrwx 1 root root 0 Oct  6 12:56 pid -> 'pid:[4026531836]'
  lrwxrwxrwx 1 root root 0 Oct  6 12:56 pid_for_children -> 'pid:[4026531836]'
  lrwxrwxrwx 1 root root 0 Oct  6 12:56 user -> 'user:[4026531837]'
  lrwxrwxrwx 1 root root 0 Oct  6 12:56 uts -> 'uts:[4026531838]'
  ```

-  생성할 수 있는 최대 네임스페이스 개수는 /proc/sys/user 디렉토리에 파일들로 지정되어 있음

   >    *  The values in these files are modifiable by privileged processes.
   >
   >        *  The values exposed by these files are the limits for the user namespace in which the opening process resides.
   >
   >        *  The limits are per-user.  Each user in the same user namespace can create namespaces up to the defined limit.
   >
   >        *  The limits apply to all users, including UID 0.
   >
   >        *  These  limits  apply  in  addition  to  any  other per-namespace limits (such as those for PID and user namespaces) that may be
   >           enforced.
   >
   >        *  Upon encountering these limits, clone(2) and unshare(2) fail with the error ENOSPC.
   >
   >        *  For the initial user namespace, the default value in each of these files is half the limit on the number of threads that may be
   >           created (/proc/sys/kernel/threads-max).  In all descendant user namespaces, the default value in each file is MAXINT.
   >
   >        *  When a namespace is created, the object is also accounted against ancestor namespaces.  More precisely:
   >
   >           +  Each user namespace has a creator UID.
   >
   >           +  When  a namespace is created, it is accounted against the creator UIDs in each of the ancestor user namespaces, and the ker‐
   >              nel ensures that the corresponding namespace limit for the creator UID in the ancestor namespace is not exceeded.
   >
   >           +  The aforementioned point ensures that creating a new user namespace cannot be used as a means to escape the limits in  force
   >              in the current user namespace.

## Lifecycle

- 생성된 새로운 네임스페이스의 생명주기는 어떻게 되는가?
  1. 영구 지속
  2. 시스템 리부트 시 초기화
  3. 네임스페이스 내의 모든 프로세스 종료 시 일정기간 이후 삭제

## Details

### Mount Namespace

- 각 네임스페이스 인스턴스의 프로세스들이 볼 수 있는 마운트 포인트들을 격리시켜줌
- 이는 네임스페이스는 `/proc/$$/{mounts, mountinfo, mountstats}` 파일들로 정의가 되는데, 동일한 마운트 네임스페이스에 속한 프로세스들은 동일한 파일들로 구성된다.
-  프로세스는 `clone` 또는 `unshare`로 생성되므로, 마운트 네임스페이스는 caller's mount namespace의 복사본이며 마운트 네임스페이스에 대한 추가적인 변경은 caller의 것에 반영되지 않는다.

### UTS Namespace

- 

### IPC Namespace

- 

### PID Namespace

- 

### User Namespace

- 

### Network Namespace

- 

### Cgroup Namespace

- 



## API

### clone

1. 새로운 프로세스 생성

2. N(주어진 네임스페이스 FLAG, N <= 7)개의 네임스페이스를 생성

   > 동시에 여러개의 FLAG를 주기 위해서는 |(Vertical Var) 로 구분지어줌
   >
   > Example
   > clone CLONE_NEWCGROUP | CLONE_NEWIPC | ...

3. 새로운 프로세스를 각 네임스페이스의 멤버로 만들어줌

```c
#define _GNU_SOURCE
#include <sched.h>

int clone(int (*fn)(void *), void *child_stack,
      int flags, void *arg, ...
      /* pid_t *ptid, void *newtls, pid_t *ctid */ );
```



### setns

이미 존재하는 네임스페이스에 프로세스를 연결

```c
#define _GNU_SOURCE             /* See feature_test_macros(7) */
#include <sched.h>

int setns(int fd, int nstype);
/*
fd		: file descriptor that refers to one of the '/proc/[pid]/ns' files
nstype	: flag
*/
```



### unshare

기존에 실행되고 있는 프로세스를 새로 지정된 네임스페이스에 연결

## Reference

[1]: https://man7.org/linux/man-pages/man7/namespaces.7.html	"Linux Kernel Namespaces"
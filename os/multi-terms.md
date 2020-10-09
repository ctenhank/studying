# Multi-programming

- 초기 컴퓨터는 메모리에 하나의 프로그램만 실행됨
- 프로그램이 I/O 요청을 하거나 어떤 상황에 CPU를 사용하지 않을 경우가 발생
- CPU 낭비가 발생하는데, 이를 개선하고자 나온 개념이 메모리에 다수의 프로그램을 올리는 것
- 따라서 프로그램의 견고한 제어 및 메모리의 정밀한 구획화가 필요

# Multi-tasking

-  Multi-programming 개념에서 파생된 개념인 멀티태스킹은 일정 시간동안(매우 짧은시간) 프로그램들을 번갈아가면서 실행시킴으로써 사용자가 동시에 여러 프로그램이 실행되고 있다고 생각하게 만들어줌

# Multi-processing

-  단일 컴퓨터 시스템에서 하나의 CPU를 넘어서 두 개 이상의 CPU를 가지고 있으면, 실질적으로 다수의 프로그램을 동시에(번갈아가면서가 아니라) 실행시킬 수 있음

# Multi-thread

-  한 CPU가 하나의 프로세스를 처리하는데, 프로세스가 I/O 요청을 하거나, 이벤트가 발생할때 까지 대기하거나 등 사용하지 않을 수 있다. 따라서 논리적 개념인 쓰레드를 이용하여 어떤 요청에 대해서 응답(시스템 콜)이 발생하면 다시 그 일을 수행하게끔 할 수 있다. 이런 원리와 같이 다중 쓰레드를 이용하여 프로그램 효율성을 높일 수 있다.

-  그럼 I/O 요청이 있거나 대기 상황이 발생하면 다른 프로세스를 실행시키면 되지 않는가?
  1.  상황에 따라 어떤 프로세스가 빨리 끝낼 필요성이 있을 경우, 아니면 그 대기상황이 나머지 일을 처리하는데 영향이 없는 경우 등 다양한 상황이 발생할 수 있다.
  2.  그런 상황이 있을 때마다 바꾸면, Context Switch를 하기 위한 오버헤드가 너무 커서 오히려 비효율적일 수 있다. 따라서 일정시간동안 프로세스가 수행되게끔 설정하여, 멀티 쓰레드를 이용하면 더 효율적일 수 있다.
     Q. 그럼 Context Switch와 멀티쓰레딩을 수행하기 위한 시스템 콜 처리 등 둘 중 어느게 효율적인지 확실하게 알 수 있나?
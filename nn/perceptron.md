# Perceptron

### Concepts

* 퍼셉트론(Perceptron)은 다수의 신호를 입력으로 받아 하나의 신호를 출력을 말한다.
* 여기서 신호란 전류나 강물처럼 흐름이 있는 것이라 생각하면 좋다.
* 하지만 여기서 신호란 실제 전류나 강물과는 달리 흐른다/안 흐른다(0이나 1)의 두 가지 값만 가질 수 있다.
* 퍼셉트론은 다음 그림과 같다.

![image-20201207142653926](/home/dohan/project/studying/nn/img/image-20201207142653926.png)

* 퍼셉트론은 TLU(Threshold Logicl Unit) 또는 Node(노드) 라고 불린다.
* TLU는 Weight를 곱한 Input 값들의 합을 계산하는데, 활성화 함수(Activation Fuction)을 통해 출력(Output)할 지, 안 할지 정한다.
* 수식으로 표현하자면 다음과 같다. 

![image-20201208163119476](/home/dohan/project/studying/nn/img/image-20201208163119476.png)

* 위의 그림에서는 활성화 함수 중 한 가지인 Step function을 이용한다.

### Example

더 나은 이해를 위해 한 가지 예제를 보자.

<img src="/home/dohan/project/studying/nn/img/image-20201208163350917.png" alt="image-20201208163350917" style="zoom:50%;" />

1. 입력값 `x`가 들어왔을때, 가중치 `w`값과 `MatMul`, 즉 매트릭스 곱셈을 해준다.
2. 그 후 `B`, Bias(편향) 값을 더해준다.
3. 마지막으로 활성화 함수 중 하나인 `Sigmoid`을 통해 값으로 출력할 지, 안 할지 결정한다.

<img src="/home/dohan/project/studying/nn/img/image-20201208163616895.png" alt="image-20201208163616895" style="zoom:50%;" />

* 또한 가중치 `w`와 편향값 `B`는 노드가 입력 값을 어떻게 생각하는지에 대한 수치로 나타낸 것이라 볼 수 있다.

* 코드로 한 번 확인해보자(한 개의 입력)

  ![image-20201208163735088](/home/dohan/project/studying/nn/img/image-20201208163735088.png)

* 코드로 한 번 확인해보자(세 개의 입력)

![image-20201208163917035](/home/dohan/project/studying/nn/img/image-20201208163917035.png)

### Forward propagation

![image-20201208164000428](/home/dohan/project/studying/nn/img/image-20201208164000428.png)

* 위의 컨셉과 예제들에서 살펴본 것과 같이 입력 값을 가지고 가중치와 편향 값으로 어떤 계산을하고 활성화 함수로 출력까지 해주는 과정을 **Forward propagation**이라 한다.



### Backpropagation

> 살펴보기에 앞서 참고하기 좋은 [유튜브 영상](https://www.youtube.com/watch?v=XxMhC11bD8o&list=PLVNY1HnUlO2702hhjCldVCwKiudLHhPG0&index=2)이 있다.

난 앞서 살펴본 내용으로 다음과 같은 의문을 가졌다.

* 가중치 `w`와 편향값 `B`은 어떻게 입력에 대해 최적화될까?

위 두 가지 의문에 대해서, 만약 세상의 모든 문제가 위 예와 같이 간단하다면 손으로 직접 입력할 수도 있다. 하지만 대다수의 문제는 매우 복잡한 구조로 이루어 질테고, 그것을 사람의 손으로 일일이 구현하기에는 매우 힘들 것이라 본다.

따라서, 자연스럽게 다음과 같은 의문을 가졌다.

* 가중치와 편향값을 자동으로 구해줄 수 있는 방법은 없을까?

하지만 그 의문보다도 먼저 해야하는 것이 있다. 그것은 바로 다음과 같다

* 가중치와 편향값의 초갓값을 어떻게 설정 해야할까?

초깃값을 설정하는 방법에는 다양한 방법들이 있겠지만 간단하게 생각하자면 다음과 같다.

* 모든 초깃값들을 0으로 설정한다.
* 모든 초깃값들을 랜덤하게 설정한다.

첫 번째 방법인 초깃값들을 0으로 설정하면 어떤 문제가 발생할 수 있다.

> 출처: 밑바닥부터 시작하는 딥러닝1, 6.2.1 초깃값을 0으로 하면?

따라서, 초기갓들을 랜덤하게 설정한다. 

그럼 다시 "*가중치 `w`와 편향값 `B`은 어떻게 입력에 대해 최적화될까?*"에 대해서 살펴보자.





### Perceptron Implementation

퍼셉트론을 이용하여 AND, OR, NAND 게이트들을 구현해볼 것이다.

```python
# 임계값 theta를 통해 theta보다 작으면 출력이 없고, 크면 출력이 존재
def AND(x1, x2):
    w1, w2, theta = 0.5, 0.5, 0.7
    t = x1*w1 + x2*w2
    if t <= theta:
        return 0
    elif t > theta:
        return 1
```

위 코딩은 직관적이지만, 아래 코딩과 같이 편향을 추가하여 바꿔보자

```python
# 편향 추가: AND
import numpy as np
def AND(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.7
    t = np.sum(w*x) + b
    if t <= 0:
        return 0
    else:
        return 1

# NAND와 OR 게이트를 추가 구현했다.
def NAND(x1, x2):
    x = np.array([x1, x2])
    w = np.array([-0.5, -0.5])
    b = 0.7
    t = np.sum(w*x) + b
    if t <= 0:
        return 0
    else:
        return 1

def OR(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.2
    t = np.sum(w*x) + b
    if t <= 0:
        return 0
    else:
        return 1
```

* 위 구현에서는 앞선 나온 개념과 달리 b라는 bias, 즉 편향을 추가했다.
  * w1, w2는 각 입력 신호가 결과에 주는 영향력(중요도)을 조절하는 매개변수이다.
  * b는 뉴런이 얼마나 쉽게 활성화(결과로 1을 출력)하느냐를 조정하는 매개변수이다.
  
## 퍼셉트론의 한계
* 퍼셉트론은 AND, NAND, OR 게이트는 구현할 수 있지만, XOR 게이트는 구현할 수 없다.
* 이는 직선 하나로 나눈 영역만 표현하기에는 한계가 있기 때문이다. 다음 그림과 같다.

* 이러한 퍼셉트론의 한계는 다층 퍼셉트론을 이용하여 해결 할 수 있는데, 다음과 같다.

![image.png](attachment:c31d6dbc-7f2b-42d9-9dfb-b22a1e139360.png)

이러한 다층 퍼셉트론(Multi-Layer Percetpron)의 구조는 다음과 같다.
* 다층 퍼셉트론은 가장 간단한 표현은 위 그림과 같이 두 개의 계층, 즉 입력 레이어와 출력 레이어로 구성된다.
* 다층 퍼셉트론은 출력 레이어를 제외한 모든 레이어들은 각 노드 간에 fully-connected 구조를 가진다.

또한, XOR 게이트는 AND, OR, NAND 게이트로 표현할 수 있다.

![image.png](attachment:dbc06661-9f2d-4a89-95c7-5e06c6e37277.png)

## XOR 게이트 구현

```python
def XOR(x1, x2):
    t1 = NAND(x1, x2)
    t2 = OR(x1, x2)
    y = AND(t1, t2)
    return y
```



## 정리

* 퍼셉트론이라는 것을 이용하여 사람의 신경과 유사한 동작을 구현할 수 있다.
* 퍼셉트론은 입력을 주면 가중치와 편향을 이용한 정해진 규칙에 따라 값을 출력한다.
* 퍼셉트론과 다층 퍼셉트론을 이용하여 AND, OR, NAND, XOR 등 다양한 게이트들을 표현할 수 있다.
* NAND를 이용하면 복잡한 컴퓨터 시스템을 구현할 수 있다.

**그러므로 퍼셉트론을 이용하면 사람의 신경과 유사한 동작을 할 수 있고, 복잡한 컴퓨터 시스템을 구현할 수 있으니 인공지능을 구현할 수 있지 않을까?**
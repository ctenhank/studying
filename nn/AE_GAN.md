# AutoEndcoder & GAN

### Prerequisite

- #### PCA

## AutoEncoder(AE)

### Motivation

1. **첫 번째 예**

   >  다음과 같은 두 가지 일련의 숫자들이 존재한다. 
   >
   > - 40, 27, 25, 36, 81, 57, 10, 73, 19, 68
   > - 50, 25, 76, 38, 19, 58, 29, 88, 44, 22, 11, 34, 17, 52, 26, 13, 40, 20
   >
   > 사람들은 이러한 수열들을 어떻게 쉽게 기억할 수 있을까?

   얼핏 봤을 때, 첫 번째 수열이 두 번째 수열보다 기억하기가 더 쉬워보인다. 하지만 두 번째 수열은 **헤일스톤 수열(hailstone sequence)**이라고 불리는데, 짝수는 절반으로 줄어들고 홀수는 3을 곱하고 1이 더해지는 규칙이 있다. 따라서 수열을 구성하는 어떤 규칙, 즉 패턴이 존재한다면 더욱 기억하기가 쉬울 것이다.

2. **두 번째 예**

   > 위 논문에 따르면, 숙련된 체스 플레이어는 체스 판을 5초 동안만 바라보고도 전체 체스 말들의 위치를 외울 수 있다는 것을 알아냈다. 하지만 이는 체스 말들이 무작위로 놓여있을 때가 아니라 현실적인 위치, 즉 경험적으로 숙달된 어떤 체스 배치 패턴을 가지고 있는 체스판을 보았을 때 가능한 일이다.
   >
   > *Perception in  chess,*
   >
   > Sources: https://www.sciencedirect.com/science/article/pii/0010028573900042

앞선 두 가지 예와 같이, **AutoEncoder**는 “어떤 것이 단순히 무작위로 나열됐을 때보다 어떤 규칙이나 패턴을 가지고 있고,이 패턴을 찾게 되면 정보를 효율적으로 저장할 수 있다”라는 관점에서 동작한다.

### AutoEncoder Architecture

<img src="https://upload.wikimedia.org/wikipedia/commons/3/37/Autoencoder_schema.png" alt="autoencoder" style="zoom:50%;" />

> Source: https://upload.wikimedia.org/wikipedia/commons/3/37/Autoencoder_schema.png

위의 예제와 같이 **AE(AutoEncoder; 앞으로는 AE라고 축약해 표현함)**는 **입력 데이터**를 가지고 **내부 표현**으로 바꾸고(어떤 규칙을 찾고), 내부 표현(그 규칙)을 바탕으로 **새로운 출력 데이터(생성 모델; generatvie model)**를 만들어낸다. 즉, 단순히 **AE**는 입력 레이어를 출력 레이어로 복사하면서 배운다.

이 때 입력을 내부 표현으로 바꾸는 부분을 **Encoder(recognition newtork)**라 하며, 내부 표현을 출력으로 바꾸는 부분을 **Decoder(generative network)**라 한다. **AE**는 입력을 재구성하기 때문에 출력을 종종 **재구성(reconstruction)**이라고도 한다. 비용 함수는 재구성이 입력과 다를 때 모델에 벌점을 부과하는 **재구성 손실(reconstruction loss)**를 포함한다.

AE 특징, 구조 및 동작을 자세히 알아보기 전에 스스로 AE가 어떻게 동작할지에 대해서 생각해보자.

1. 입력 값을 이용해 어떻게 내부 표현, 즉 패턴을 찾을 수 있는가?
   - 내부 네트워크, 즉 encoder 부분의 크기를 제한
   - 입력 데이터에 **noise**를 추가한 후, 이를 다시 원본 입력 데이터로 복원
2. 패턴을 통해 어떻게 생성 모델을 만들어낼 수 있는가?

### Simple AutoEncoder

 오토인코더 구조에 대해 자세히 알아보기 전에 먼저 가장 단순한 오토인코더 구조를 살펴보자. 가장 간단한 오토인코더 구조는 기본적으로 입력과 출력 레이어, 그 사이에 단일의 히든 레이어로 구성되어 있다. 

![simple ae](https://www.researchgate.net/publication/318204554/figure/fig1/AS:512595149770752@1499223615487/Autoencoder-architecture.png)

> Source: https://www.researchgate.net/figure/Autoencoder-architecture_fig1_318204554

 이것만 보자면 **다중 레이어 퍼셉트론**과 동일하다고 볼 수 있다. 오토인코더와 다중 레이어 퍼셉트론(MLP)의 차이점은 `output layer`가 반드시 `input layer`와 **동일한 숫자의 뉴런**을 가져야 한다는 것이다. 또한 위의 그림은 내부 표현, 즉 히든 레이어가 입력 데이터보다 저차원(입력 7차원; 히든 4차원)이기 때문에, 이런 **AE**를 **과소완전(undercomplete)**라 한다.

 **Undercomplete AE**는 입력을 코딩으로 간단히 복사할 수 없으며, 입력과 똑같은 것을 출력하기 위한 다른 방법이 필요하다. 이는 입력 데이터에 가장 중요한 특성을 학습하도록 한다. 즉, 앞서 본 것과 같이 패턴을 찾는 것이다.

> 의문점
>
> 1. 왜 반드시 입력 레이어와 출력 레이어의 뉴런 수가 같아야할까?
> 2. 입력 레이어 데이터들의 값과 출력 레이어 데이터들의 값들은 무조건 (값과 순서) 동일해야 하는가?
> 3. 왜 Undercomplete AE는 입력을 코딩으로 간단히 복사할 수 없을까?

 

#### Undercomplete AE



## Generative Adversarial Network(GAN)

![gan](https://files.slack.com/files-pri/T25783BPY-F9SHTP6F9/picture2.png?pub_secret=6821873e68)

> Source: https://files.slack.com/files-pri/T25783BPY-F9SHTP6F9/picture2.png?pub_secret=6821873e68

`generator`와 `discriminator`로 구성되어 있다.

- **Generator**
  학습 데이터와 유사한 데이터를 생성해낸다.
- **Discriminator**
  `generator`를 통해서 만들어낸 데이터(`fake data`)와 인풋 데이터(`real data`)를 계속해서 반복적으로 학습한다.
# AutoEndcoder & GAN

### Prerequisite

- #### PCA

## AutoEncoder(AE)

오토인코더는 `unsupervised data`를 사용하여 입력 데이터의 효율적인 표현인 코딩을 학습할 수 있는 인공신경망을 의미한다.

<img src="https://upload.wikimedia.org/wikipedia/commons/3/37/Autoencoder_schema.png" alt="autoencoder" style="zoom:50%;" />

> Source: https://upload.wikimedia.org/wikipedia/commons/3/37/Autoencoder_schema.png

오토인코더는 단순히 input 레이어를 output 레이어로 복사하면서 배운다.

### Simple AutoEncoder

 오토인코더에 대해 자세히 알아보기 전에 먼저 가장 단순한 오토인코더 구조를 살펴보자. 가장 간단한 오토인코더 구조는 기본적으로 입력과 출력 레이어, 그 사이에 단일의 히든 레이어로 구성되어 있다. 이것만 보자면 다중 레이어 퍼셉트론과 동일하다고 볼 수 있다.

![simple ae](https://www.researchgate.net/publication/318204554/figure/fig1/AS:512595149770752@1499223615487/Autoencoder-architecture.png)

> Source: https://www.researchgate.net/figure/Autoencoder-architecture_fig1_318204554

 오토인코더와 다중 레이어 퍼셉트론(MLP)의 차이점은 `output layer`가 반드시 `input layer`와 동일한 숫자의 뉴런을 가져야 한다는 것이다. 또한 오토인코더 구조에서 히든 레이어 이전으로는 `Encoder`이라고 부르며, 이후로는 `Decoder` 라고 한다. 

#### Undercomplete AE



## Generative Adversarial Network(GAN)

![gan](https://files.slack.com/files-pri/T25783BPY-F9SHTP6F9/picture2.png?pub_secret=6821873e68)

> Source: https://files.slack.com/files-pri/T25783BPY-F9SHTP6F9/picture2.png?pub_secret=6821873e68

`generator`와 `discriminator`로 구성되어 있다.

- **Generator**
  학습 데이터와 유사한 데이터를 생성해낸다.
- **Discriminator**
  `generator`를 통해서 만들어낸 데이터(`fake data`)와 인풋 데이터(`real data`)를 계속해서 반복적으로 학습한다.
# Anaconda

데이터 사이언스를 위한 Python 응용 프로그램 중 하나

**핵심 기능**

* 패키지 관리

  ​	기존에 python pkg를 관리할 때, pip를 통해서 했다면 이는 Anaconda라는 응용 프로그램을 통해서 함

   	Q.  pip와 다른 것이 무엇인가?

  ​		pip는 단순히 패키지 관리 파이썬 모듈이었다면, Anaconda는 Cross-platform, Virtual Enviroment 등 다양한 기능들을 지원	

* 가상 환경

  ​	가상 환경을 쓰는 이유는 무엇인가? 

  패키지를 만들거나 응용 프로그램을 만들 때, 만약 하나의 통합된 환경에서 이런 저런 패키지를 설치하여 관리를 하다보면 상충되는 패키지가 존재할 수 있음

  예를들어, A1라는 패키지를 설치하고자 할 때, B, C라는 패키지가 필요

  ​	그리고, A2라는 패키지를 설치하고자 할 때, B, C라는 패키지가 필요

  두 개 다 동일한 패키지가 요구되지만, A1에 대한 B, C 패키지 버전은 A2에 대한 B, C 패키지 버전보다 다를 수 있다.

  이와 같이 하나의 통합 환경에서 패키지를 관리하게 되면, 상충되는 경우가 종종 발생할 수 있다.

  **결론으로**, 독립된 환경(가상 환경)에서 패키지를 따로 설치하여 패키지를 만들거나 응용 프로그램을 만들 때 효율적으로 만들 수 있다.



**Anaconda**

* `Anaconda`는 다양한 데이터 사이언스를 위한 수많은 모듈들이 존재하므로 무거울 수 밖에 없다.
* 이를 위해 `Anaconda`는 `miniconda`라는 핵심적인 모듈만 존재하는 버전도 존재한다.
* 설치는 docker를 이용한 miniconda를 할 예정 [miniconda dockerhub link](https://hub.docker.com/r/continuumio/miniconda3)

```bash
> docker pull continuumio/miniconda3
> docker run -it --name conda continuumio/miniconda3 bash
(base)> conda update conda
(base)> conda create -n vs-jupyter
(base)> conda init bash
(base)> exit
(base)> docker start conda
(base)> docker exec -it conda bash
(base)> conda activate vs-jupyter
(vs-jupyter)> conda install -c conda-forge jupyter
```



**Command**

```shell
conda install
conda create
conda init
conda activate
conda list
conda remove
```


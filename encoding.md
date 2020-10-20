# 문자 인코딩(Character Encoding)

- **인코딩(Encoding)**
   사용자가 입력한 문자나 기호들을 컴퓨터가 이용할 수 있는 신호로 만드는 것
  그 역은 **디코딩(Decoding)**이라 한다.



## ASCII

- 아스키라고 불리며, American Standard Code for Information Interchange 의 약자
- 최초의 문자 인코딩 방식
- 7비트로 구성되어 있으며, 영어, 숫자, 특수문자, 제어문자, 공백 등으로 이루어짐



**Q. 한 바이트 단위인 8비트가 아니라 7비트로 구성되어 있을까?**

- 첫 번째 비트는 **parity bit**로 오류 검사할 때 쓰임
-  입력 문자는 무조건 홀수로 만들어야 한다는 규칙이 있으면
  홀수면 첫 비트가 0, 짝수면 첫 비트가 1로 설정해 간단한 오류 검사용으로 쓰일 수 있음



### ANSI

- ASCII는 영어만 표현할 수 있다는 있음
- 첫 비트를 국가별 언어로 설정할 수 있게 만든 것이 **ANSI**



**한계**

* 비유럽국가(중국, 한국 등)에서 사용이 제한
* 해당 국가의 언어를 다른 국가에서 사용할 수 없음
   *한글을 이용하려면 추가적인 프로그램 설치가 필요했음*



## UNICODE

* 전 세계의 모든 문자를 컴퓨터에서 일관되게 표현하도록 설계된 산업 표준
* 총 16비트(=2바이트)로 구성되어 있으며, 대다수의 언어를 표현할 수 있음
* 더 자세한 설명은 [Unicode](https://en.wikipedia.org/wiki/Unicode)에서 참고



**한계**

​	16비트(65546개)로 모든 문자(수식, 고대 중국어 등)을 표현하기에는 부족함

**해결**

- 유니코드에서 **0xD800 ~ 0xDFFF** 부분을 이용하여 다른 문자를 표현
- 해당 범위 문자 표현 가능 개수는 2^11^ = 2048
- 2^11^를 2^10^ 로 표현하면 2개로 나타낼 수 있음
- 2^10^ * 2^10^ 는 1,048,576(약 100만)개까지 표현 가능
- 이를 [Surrogate Pair](###Surrogate-Pair)에서 설명



### Surrogate Pair

* 유니코드의 바이트 수를 늘리지 않고 **0xD800 ~ 0xDFFF**  범위를 나눠서 이용하기 때문에 붙은 이름
* **0xD800 ~ 0xDBFF**, **0xDC00 ~ 0xDFFF** 두 개의 영역으로 나눠 **Pair**를 이룸
* **0xD800 ~ 0xDBFF**는 High-Surrogate라고 불리며, **prefix bit**는 110110~2~
* **0xDC00 ~ 0xDFFF**는 Low-Surrogate라고 불리며, **prefix bit**는 110111~2~
* prefix bit로 상/하위를 구분할 수 있음
* 100만개 가량의 문자를 표현할 수 있기에, 이를 기존 2^16^ 개 단위로 영역을 나눔



### 영역(Plane)

* 원래 2바이트로 이루어진 영역을 **기본 다국어 평면(Basic Multilingual Plane; BMP)**
* 그 외의 추가적인 영역이 있는데 다양한 종류의 **보충 평면(Supplementary Plane; SP)** 존재
* 1번 보충 평면에서 16번까지 존재하고, 보충 평면의 역할에 따라 구분
* 이에 대한 자세한 설명은 [유니코드](http://www.unicode.org/Public/UNIDATA/Blocks.txt)를 참조



## 유니코드 변환 형식

- 유니코드(Uni-code)는 어떤 문자를 표현하기 위한 약속이지 인코딩하는 것은 아님
- 인코딩하는 방식 중 유니코드는 2가지 방식이 존재
- [국자 문자 세트 인코딩(Universal coded Character Set, UCS)](https://en.wikipedia.org/wiki/Universal_Coded_Character_Set)
- [유니코드 변환 형식 인코딩(UTF)](https://en.wikipedia.org/wiki/Unicode#UTF)



## UCS

* 국제 표준에 의해 정의되고 문자 인코딩의 **기초**가 되는 표준 문자 세트
* 현재 [UCS-2](https://en.wikipedia.org/wiki/Universal_Coded_Character_Set), [UCS-4]() 2가지가 존재하지만, UCS-4는 표준은 아님

* USC-2는 고정된 2바이트 길이로만 문자 인코딩이 가능하며, 보충 평면에 대해서는 인코딩이 불가능
* USC-4는 고정된 4바이트 길이로만 문자 인코딩이 가능

## UTF

* UTF는 Universal Coded Character Set + Transformation Format의 약자로 다양한 버전이 존재
* 버전: [UTF-8](https://en.wikipedia.org/wiki/UTF-8), [UTF-16](https://en.wikipedia.org/wiki/UTF-16), [UTF-32](https://en.wikipedia.org/wiki/UTF-32)
* 현재 비트는 21비트까지 지원(10FFFF = 2^21^)



### UTF-8

* UTF-8은 Universal Coded Character Set + Transformation Format - 8 bits
* **가변 길이** 문자 인코딩 방식으로, 유니코드 한 문자를 나타내기 위해 1 바이트에서 4 바이트까지 사용

#### 구조

| 코드 범위(십육진법) |         UTF-8 표현(이진법)          |                        설명                        |
| :-----------------: | :---------------------------------: | :------------------------------------------------: |
|    000000-00007F    |              0xxxxxxx               |                    ASCII와 동일                    |
|    000080-0007FF    |          110xxxxx 10xxxxxx          |           첫 바이트는 110 또는 1110 시작           |
|    000800-00FFFF    |     1110xxxx 10xxxxxx 10xxxxxx      |           나머지 바이트들은 10으로 시작            |
|    010000-10FFFF    | 11110zzz 10zzxxxx 10xxxxxx 10xxxxxx | UTF-8로 표시된 비트 패턴은 실제 코드 포인트와 동일 |

* 7비트 ASCII 문자와 혼동되지 않기 위해 모든 바이트들의 최상위 비트는 1
* 원래 UTF-8은 6바이트를 사용하여 U+7FFFFFFF까지 사용가능했으나 U+10FFFF까지로 표시 제한



### UTF-16

* UTF-16은 Universal Coded Character Set + Transformation Format - 16 bits
* UTF-16도 가변 길이 문자 인코딩 방식으로, 유니코드 한 문자를 나타내기 위해 2바이트 또는 4바이트를 사용

#### 구조

| 코드 범위(십육진법) |         UTF-16 표현(이진법)         |       설명       |
| :-----------------: | :---------------------------------: | :--------------: |
|    000000-00007F    |          00000000 0xxxxxxx          |                  |
|    000080-0007FF    |          00000xxx xxxxxxxx          |                  |
|    000800-00FFFF    |          xxxxxxxx xxxxxxxx          |                  |
|    010000-10FFFF    | 110110ZZ ZZxxxxxx 110111xx xxxxxxxx | ZZZZ = zzzzz - 1 |

ex) char = 0001 0000 1111 0010 0001 0100~2~

ZZ = 10000~2~ - 1~2~ = 1111~2~
UTF16(char) = **1101 10**11 1111 1100 **1101 11**10 0001 0100~2~

ex2) char = 0110 1100 1010 0010 1011~2~

ZZ = 0110~2~ -1~2~ = 0101~2~ 
UTF16(char) = **1101 10**01 0111 0010 1011 1110 0010 1011~2~



### UTF-32

UCS-4와 동일한 기능, 고정된 4바이트 길이의 문자 인코딩



## BOM

* Byte Order Mark로 CPU가 Big endian 또는 Small endian인지 판별
* 문서 맨 앞에 눈에 보이지 않는 특정 바이트
* U+EFBBBF
* U+FEFF
* U+FFFE
* U+0000FEFF
* U+FFFE0000
























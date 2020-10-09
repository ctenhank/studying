# Google Cloud Platform으로 Kubernetes 연습하기

### Instance group 만들기

1. 인스턴스 템플릿은 원하는대로 설정

2. 보안을 위해서 SSH 키를 생성하고 등록

   ```bash
   $ ssh-keygen -t rsa
   Generating public/private rsa key pair.
   # 암호 키 저장할 경로 입력
   Enter file in which to save the key (/home/dohan/.ssh/id_rsa): 
   # 비밀번호 입력
   Enter passphrase (empty for no passphrase): 
   # 비밀번호 확인
   Enter same passphrase again: 
   Your identification has been saved in /home/dohan/.ssh/id_rsa.
   Your public key has been saved in /home/dohan/.ssh/id_rsa.pub.
   The key fingerprint is:
   SHA256:a6W6hv57xnBV9H8JD9jM6vMdlG55Jdxuaw2VwW5EfwU dohan@dohan
   The key's randomart image is:
   +---[RSA 2048]----+
   |           .. Eo.|
   |            *. +o|
   |           o *+ =|
   |          . ..+*=|
   |        S...  +*=|
   |      . .+.   +o+|
   |     . ++  o   *=|
   |    . .o+   o oo=|
   |   ..o==     ..o |
   +----[SHA256]-----+
   # 만약 위에서 ssh 키 저장 위치를 변경했으면 해당 폴더에 이동하거나 그 폴더의 파일로 읽음
   $ vi id_rsa.pub
   # id_rsa.pub 안에 있는 퍼블릭 rsa 암호 키를 google instance template에 등록
   ```

3. 
# Kubernetes YAML

- 쿠버네티스 YAML 파일은 일반적으로 네 가지 항목으로 구성:
  `apiVersion`, `kind`, `metadata`, `spec`

### apiVersion

- YAML 파일에서 정의한 오브젝트의 API 버전
- `kubectl explain OBJECT` 명령어로 개별 오브젝트의 API 버전을 확인할 수 있음

### kind

- 리소스 종류, 즉 어떤 오브젝트인지 나타냄
- `kubectl api-resources` 명령어를 통해 오브젝트들을 확인할 수 있음

### metadata

- 라벨, 주석, 이름 ㄷㅡᅁᅪ 같은 리소스 부가 정보

### spec

- 리소스를 생성하기 위한 자세한 정보
- `containers`, `image`, `port`, ...




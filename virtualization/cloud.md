# Cloud

## Concepts

### Definition



### Characteristics

##### **resource pooling**

"provider's computing resources are pooled to serve multiple consumers using a multi-tenant model, with different physical and virtual resources dynamically assigned and reassigned according to consumer demand" [[1]][1]

##### **rapid elasticity**

"capabilities can be elastically provisioned and released, in some cases automatically, to scale rapidly outward and inward commensurate with demand"

### Bare metal server

 provide the referenced elasticity and automation to the rapid provisioning and assignment of physical servers, eliminating the overhead of a hyper-visor or container together to serve a remote physical server without [virtualization](./virtualization.md)

> Naver		https://www.ncloud.com/product/compute/baremetal
> IBM			https://www.ibm.com/kr-ko/cloud/bare-metal-servers
> Amazon	https://aws.amazon.com/ko/about-aws/whats-new/2019/02/introducing-five-new-amazon-ec2-bare-metal-instances/

### Service Model

- Iaas
- Paas
- Saas

### Deployment Model

- Private Cloud
- Public Cloud
- Hybrid Cloud
- Community Cloud 

## Application Examples

### Hypervisor

#### ESXi

- Terremark
- Savvis

#### Xen

- AWS

#### KVM

- AT&T
- HP
- Comcast
- Orange

#### Hyper-V

- Microsoft

### Container

- Google Cloud Platform
- IBM Softlayer
- Joyent

어떻게 두 가지 종류 가상화 Hypervisor, Container를 실제 데이터센터 및 클러스터링 컴퓨터에 적용할 수 있을까?



## References

[1]: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf	"P. Mell and T. Grance, The NIST Defintion of Cloud Computing: Recommendations of the National Institude of Standards and Technology, NIST Publications 800-145, 28 Sep. 2011"



[./virtualization.md]: 
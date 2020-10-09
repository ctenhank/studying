# Container

### Why use the container replaced the VM or traditional method?

- There are no performance loss comparing with VM(Virtual Machine)

  >  VMs use hypervisor to virtualize system resources and isolate tasks. So to communicate between VMs, VM and local computer,  VM and remote computers, messages must pass the hypervisor that cause overheads to system.  OOTH, the container has very low overhead becuase of using Linux kernel functions like chroot, namespaces and cgroups to virtualize and isolate, and sharing Linux kernel(libraries, modules, etc.) among containers.
- Easier application deployment

  >  It's difficult to deploy in VM, too larger than container that it is just full OS like windows, linux and MacOS. OOTH, the container uses the host OS's kernel, libraries and modules.

### What's disadvantages using container rather than VM?

- Security



### Why do most of companies and developers use Docker?

- Docker Image
- Docker Registry

## Concepts

- chroot
- Linux kernel namespaces
- cgroups




# Kubernetes Installation

### Installation Sequence

1. installation kubernetes[[1]](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

   ```bash
   sudo apt-get update && sudo apt-get install -y apt-transport-https gnupg2
   curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
   echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
   sudo apt-get update
   sudo apt-get install -y kubectl
   ```

2. initialize master node

   ```bash
   sudo kubeadm init --pod-network-cidr=POD_IP/SUBNET --apiserver-advertise-address=IP
   ```

3. configuration for using in normal user as well as super user mode

   ```bash
   mkdir -p $HOME/.kube
   sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
   sudo chown $(id -u):$(id -g) $HOME/.kube/config
   ## try your get pods command now
   kubectl get pods
   ```



### Problem

- kubectl server doesn't work(**Solved**: Not initialize master node)

  - Error Message

    > The connection to the server localhost:8080 was refused - did you specify the right host or port?

    ```bash
    kubectl version
    Client Version: version.Info{Major:"1", Minor:"19", GitVersion:"v1.19.2", GitCommit:"f5743093fd1c663cb0cbc89748f730662345d44d", GitTreeState:"clean", BuildDate:"2020-09-16T13:41:02Z", GoVersion:"go1.15", Compiler:"gc", Platform:"linux/amd64"}
    The connection to the server localhost:8080 was refused - did you specify the right host or port?
    ```

  - Solution

    - [reference 1](https://medium.com/@texasdave2/troubleshoot-kubectl-connection-refused-6f5445a396ed)

      ```bash
      mkdir -p $HOME/.kube
      sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
      sudo chown $(id -u):$(id -g) $HOME/.kube/config
      ## try your get pods command now
      kubectl get pods
      ```

    - open port 8080

      ```bash
      # for master node
      sudo ufw allow 6443
      sudo ufw allow 2379:2380
      sudo ufw allow 10250:10252
      
      # for worker node
      sudo ufw allow 10250
      sudo ufw allow 30000:32767
      ```



### Reference

[1]: https://kubernetes.io/docs/tasks/tools/install-kubectl/	"install and set up kubectl "


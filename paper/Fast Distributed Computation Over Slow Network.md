# Fast Distributed Computation Over Slow Network

### Keywords

`Design`, `Execution engine`, `Slow Network`, `Sol: federated execution engine architecture`



### Terminology

-  **Federated model training(= federated learning, collaborative learning)**[[1]][1]
  A technique of machine learning that trains an algorithm across multiple edge devices or server holding local data samples, without exchanging them
- Apache Spark, Apache Tez



## Abstract

- The execution engine of distributed computation stack, executing every single task of a job, designed for low latency and high bandwidth datacenter network. So in slow network or network not holded, CPUs are significantly underutilized

- To develop execution engine that can adapting to diverse network condition, `Sol: federated execution engine architecture`:
  1. To mitigate the impact of high latency, Sol proactively assigns tasks, but does so judiciously to be resilient to uncertainties
  2. To improve the overall resource utilization, Sol decouples communication from computation[<1>](#decouples communication from computation) internally instead of committing resources to both aspects of a task simultaneously



## Introduction

Execution engine orchestrates the execution of tasks across many distributed workers

### In origin(designed for data-center or in well-provisioned network)

* The absence of noticeable network latency has popularized the ***late-binding*** task execution model *in the control plane*, maximizes flexibility

  > **late-binding**
  >
  > pick the worker which will run a task only when the worker is ready to execute the task

* The availability of high bandwidth has led to ***tight coupling*** of a task's roles to hide design complexity *in the data plane*, whereby the same task reads remote input and computes on it too

  > **tight coupling**
  >
  > ?

### Problem(In network with high-latency, low-bandwidth or both)

* Many cases, many emerging workloads, have to run on networks with high latency, low bandwidth, or both[<2>](#high latency, low bandwidth)

* Large organizations often perform interactive SQL and iterative machine learning between on- and off-premise storage

* Under-provisioned networks can lead to large CPU underutilization in today's execution engines:

  1. In a high-latency network, ***late-binding*** suffers significant **coordination overhead**, because workers will be blocked on receiving updates from the coordinator; this leads to wasted CPU cycles and inflated completion times of latency-sensitive tasks.

     > Indeed, late-binding of tasks to workers over the WAN can slow down the job by 8.5 X - 30 X than running in LAN

  2. For bandwidth-intensive tasks, ***coupling*** the provisioning of communication and computation[<3>](#Coupling the provisioning of communication and computation) resources at the beginning of a task's execution leads to **head-of-line blocking**: bandwidth-sensitive jobs hog CPUs even though they bottleneck on data transfers, which leads to noticeable **queuing delays for the rest**



### Solution

Investigation the impact of low bandwidth and high latency on latency-sensitive interactive and iterative workloads

> Recent works have proposed solutions for bandwidth-sensitive workloads. But these are still primarily the ones designed for data-centers

1.  **Advocate early-binding control plane decisions** over the WAN to save expensive round-trip coordinations, while continuing to late-bind workers to tasks within the LAN for the flexibility of decision making
   - **Pipeline different execution phases** of the task
   -  In task scheduling, we subscribe tasks for remote workers in advance, which creates a trade-off:
     binding tasks to a remote site too early may lead to sub-optimal placement due to insufficient knowledge, 
     but deferring new task assignments until prior tasks complete leaves workers waiting for work to do, thus under-utilizing them
2. **Decoupling the provisioning of resources for communication and computation** within data plan task executions is crucial to achieving high utilization
   - By introducing **dedicated communication tasks for data reads**, Sol decouples computation from communication and can dynamically scale down a task's CPU requirement to match its available bandwidth for bandwidth-intensive communications
   - The remaining CPUs can be redistributed to other jobs with pending computation





























## Question

### Decouples communication from computation

- 

### High latency, low bandwidth

- The difference between high latency and low latency, between low bandwidth and high bandwidth

### Coupling the provisioning of communication and computation

- what's meaning for?

## References

[1]: https://en.wikipedia.org/wiki/Federated_learning	"Federated model training wikipedia"


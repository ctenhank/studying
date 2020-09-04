# A Distributed  Orchestration Algorithm for Edge Computing Resources with Guarantees

## Background

- **Edge Computing**
  [[1]][1]



## Abstract

- The coexistence of such variety of applications on the same infrastructure exacerbates ***the already challenging problem*** of coordinating resource allocation while preserving the resource assignment optimality

  > **Already challenging problem**
  >
  > 1. Each application can potentially require different optimization criteria due to their heterogeneous requirements
  > 2. We may not count on a centralized orchestrator due to the highly dynamic nature of edge networks

- To solve this problem, we present `DRAGON, a Distributed Resource AssiGnment and OrchestratioN algorithm` :

  > 1. Seeks optimal partitioning of shared resources between different applications running over a common edge infrastructure
  > 2. Guarantee both a bound on convergence time and an optimal (1-1/e)-approximation with respect to the Pareto optimal resource assignment



## Introduction

### In origin(in cloud-based environments)

The deployment of services is often delegated to a **centralized component**, named **Orchestrator**, that usually exploits a ***one-size fits-all policy*** to decide:

> 1. Where to place service components
> 2. How many resources have to be assigned to each of them
> 3. The set of metrics/events signaling that the service has to be rescheduled
>
> **One-size fits-all policy**
>
> e.g., energy saving, number of used nodes, load balancing

### Problem(at the edge of the network)

Such a centralized approach may be **sub-optimal or not applicable at the edge of the network**:

> 1. Such environment may be characterized by high churn rates, unpredictable changes in the network topology and even temporary network partitions; this may favor **distributed orchestration approaches** against a centralized orchestrator, which may not be even reachable.
> 2. The largely heterogeneous set of applications running at the edge of the network may have diverse and unpredictable objectives, not to mention the necessity to react differently to the same event, such as a load increase

### Challenges for coordinating such a plethora of applications without centralized orchestrator

- How could several processes, each operating with different goals and policies, converge to a globally optimal resource management over a shared edge infrastructure? 
- How could we avoid violations of global policies or feasibility constraints of several coexisting applications?
- How can we guarantee convergence to a distributed resource allocation agreement and performance optimality given the NP-hard nature of the service placement problem?

To answer and solve it, present **DRAGON**, leverages the max-consensus literature and the theory of sub-modular functions to enable a set of a applications, featuring diverse objectives and optimization metrics, to reach an agreement on how infrastructure resources have to be assigned, without the necessity of a centralized orchestrator

### Contributions

##### **Design contributions**

- Introduce the Applications Resources Assignment Problem
- Use linear programming to model its objective and constraints

##### **Algorithmic contributions**

- How it provides guarantees on both convergence time and expected resource assignment performance to a set of independent edge applications

##### **Evaluation contributions**

- Evaluate both performance scalability and convergence properties of DRAGON, comparing them with the traditional one-size fits-all approaches
- Show some use-cases

## Reference

[1]: https://en.wikipedia.org/wiki/Edge_computing "edge computing wikipedia"








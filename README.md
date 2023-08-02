# 🚗 Vehicle Insurance Simulation 📊

## Table of Contents
1. [Event Types](#event-types)
2. [Service Time Distributions](#distributions)
3. [Other Parameters](#parameters)
4. [Staffing and Queuing Discipline](#staffing-and-queuing-discipline)
5. [Outputs](#outputs)
6. [Branches](#branches)
7. [Authors](#authors)
8. [Documentation and Contribution](#documentation-and-contribution)

## Description

This repository contains a simulation project for a vehicle insurance organization. The project involves simulating various events that occur in the insurance process, each with its own service time distribution. Additionally, different scenarios such as the probability of a car arriving alone or a customer making a complaint are taken into consideration in the simulation.The simulation initializes in an empty state.

## <a name="event-types"></a>🎯 Event Types

Here's a list of our event types and their corresponding explanations:

| Code     | Description                       |
|:---------|:----------------------------------|
| A        | Arrival                           |
| DP       | Departure                         |
| DF       | Filling the case departure        |
| DC       | Completing the case departure     |
| DE       | Expert departure                  |
| DSC      | Submitting complaint departure    |
| PA       | Second car arrival                |
| OIN      | Moving from outside to inside     |
| ISEND    | Find out if simulation should end |

## <a name="distributions"></a>⏱️ Service Time Distributions

Service times for each event follow a certain distribution:

| Event/Distribution   | Parameters            |
|:---------------------|:----------------------|
| Arrival              | Depends on weather and time, Exponential |
| Photography service  | Exponential (lambda = 6) |
| Single car waiting   | Exponential (lambda = 30) |
| Filling the case     | Triangular (min = 5, mode = 6, max = 7) |
| Expert service       | Exponential (lambda = 9) |
| Case completion      | Triangular (min = 6, mode = 8, max = 9) |
| Complaint service    | Exponential (lambda = 15) |

## <a name="parameters"></a>🎲 Other Parameters

Here are some additional parameters considered in this simulation:

* Probability that a car arrives alone: 0.3
* Probability that a customer makes a complaint: 0.1

## <a name="staffing-and-queuing-discipline"></a>🏢 Staffing and Queuing Discipline

In this simulation, the vehicle insurance organization has the following staffing and queuing discipline:

**Staffing:**
1. Filling and Completing the Case center: Three workers
2. Expert center: Two experts
3. Photography center: Two photographers
4. Complaint Submission center: One staff member

**Queuing Discipline:**
The majority of queues in this simulation follow a FIFO (First In, First Out) discipline. However, in the case of Filling and Completing the Case, the Completing the Case queue receives higher priority over the Filling the Case queue.

## <a name="outputs"></a>📈 Outputs

The simulation generates the following outputs:

1. Efficiency of workers involved in the Photography, Expert, Complaint Submission, Filling, and Completion of the Case services.
2. Average queue length for the Photography queue, Outside queue, Expert queue, and Complaint Submission queue.
3. Maximum queue length for the Photography queue, Outside queue, Expert queue, and Complaint Submission queue.
4. Average time spent in the Photography queue, Outside queue, Expert queue, and Complaint Submission queue.
5. Probabilities that the Waiting Parking and Filling queue are empty.
6. The percentage of customers who arrived alone and submitted a complaint.
7. Mean time of remaining in the system.

## <a name="branches"></a>Branches

This repository contains three branches, each serving a specific purpose:

1. **Main:** The main branch contains the primary simulation code and documentation.

2. **Part2:** The part2 branch is dedicated to comparing two systems with different parameters. It helps us analyze the effects of increasing staff at each part of the insurance process or making other modifications.

3. **Detached:** The detached branch is designed for finding the warm-up time of each system. The warm-up time is the period during which the queues transition from a transient state to a steady state.

## <a name="authors"></a>Authors 👥

This simulation project is authored by Reza Alvandi and MohammadJavad Bahmani.

## <a name="documentation-and-contribution"></a>Documentation and Contribution

For more details and contribution guidelines, please refer to the documentation provided in the repository. Happy Simulating! 🚀


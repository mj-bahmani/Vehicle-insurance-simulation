![Simulation](https://placeholder.image.url1) 

# 🚗 Vehicle Insurance Simulation 📊

This repository contains a simulation project for a vehicle insurance organization. The project involves handling various types of events, each with its own service time distribution. Different scenarios such as the probability of a car arriving alone or a customer making a complaint are also considered.

## 🎯 Event Types

![Event Types](https://placeholder.image.url2)

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

## ⏱️ Service Time Distributions

![Distribution](https://placeholder.image.url3)

Service times for each event follows a certain distribution:

| Event/Distribution   | Parameters            |
|:---------------------|:----------------------|
| Arrival              | Depends on weather and time, Exponential |
| Photography service  | Exponential (lambda = 6) |
| Single car waiting   | Exponential (lambda = 30) |
| Filling the case     | Triangular (min = 5, mode = 6, max = 7) |
| Expert service       | Exponential (lambda = 9) |
| Case completion      | Triangular (min = 6, mode = 8, max = 9) |
| Complaint service    | Exponential (lambda = 15) |

## 🎲 Other Parameters

Here are some additional parameters considered in this simulation:

* Probability that a car arrives alone: 0.3
* Probability that a customer makes a complaint: 0.1

![Parameters](https://placeholder.image.url4)

For more details, please review our [documentation](https://your.documentation.url) or feel free to contribute on [GitHub](https://your.github.url).

Happy Simulating! 🚀
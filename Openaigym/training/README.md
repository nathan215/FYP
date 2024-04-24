# Reinforcement Learning on Drone Navigation Algorithm

## General Information

I am utilizing the `stable_baselines3` library for reinforcement learning algorithms, as it provides a straightforward setup for my current level of understanding in reinforcement learning. I aim to delve deeper into reinforcement learning concepts and develop custom algorithms in the future.

## Current Attempts

Feb 23
1. **Q-Learning, Deep Q-Learning**: These methods are tailored for discrete action spaces. Currently, the results are not satisfactory, but I plan to revisit and refine my approach with these algorithms later.
2. **DDQN (Double Deep Q-Network)**: The outcomes have been underwhelming, with the model consistently navigating towards the furthest point during training.
3. **SAC (Soft Actor-Critic)**: Training with theoretical data has shown promising results, as the algorithm consistently gravitates towards areas of high signal strength in both theoretical and real-world data. However, there are still some issues that need to be addressed.
---
## Current Problems

Feb 23
1. **State Representation Concerns**: The state is currently represented as `[x, y, rssi]`, with the strongest signal always at the coordinates `(0,0)`. The model might be learning to simply move towards `(0,0)` rather than truly understanding signal strength distributions. To counteract this, I am considering shifting the coordinate system or changing the state representation to delta `[x, y]` from the starting point.
2. **Reward Structure for Movement**: I have implemented a negative reward for small steps, intending to encourage the algorithm to move larger than a predefined threshold. However, the model occasionally opts for shorter paths. Need further adjustments to the reward structure.
---


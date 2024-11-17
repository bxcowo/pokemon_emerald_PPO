# Reinforcement Learning Fundamentals

## Introduction

This submodule contains the source code of Reinforcement Learning fundamentals exercises.

### Exercise 1: Q-Learning with Ping Pong
Develop a Q-Learning agent to play Ping Pong with the game's source code (not using Gymnasium or Retro).

#### Objective
Train an AI agent to control a paddle and successfully return the ball in a Ping Pong game using Q-Learning algorithm.

#### Learning Outcomes
- Understand Q-Learning implementation in a continuous state space
- Learn about state discretization techniques
- Implement epsilon-greedy exploration strategy
- Experience reward function design
- Analyze learning performance and convergence

#### Environment Details
- **State Space**: Paddle position, ball position (x, y), ball velocity (dx, dy)
- **Action Space**: Move paddle up, down, or stay still
- **Reward Structure**:
  - +1 for successfully hitting the ball
  - -1 for missing the ball
  - Small negative reward for excessive paddle movement (energy penalty)

#### Implementation Steps
1. Set up the Ping Pong environment
2. Implement state discretization
3. Create Q-table and initialize learning parameters
4. Develop the Q-Learning update rule
5. Train the agent with epsilon-greedy exploration
6. Evaluate and visualize the learning progress


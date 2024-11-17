# Exercise 1: Ping Pong Q-Learning

## Overview
Implement Q-Learning to train an AI agent to play Ping Pong. The environment is already set up - your task is to implement the reinforcement learning components.

## Tasks
1. Implement state discretization for the continuous state space
2. Design an appropriate reward function
3. Create and implement the Q-Learning algorithm
4. Add epsilon-greedy exploration strategy
5. Train and evaluate your agent

## Environment Details
- **State Space**: Continuous values for ball position, velocity, and paddle positions
- **Action Space**: [-1, 0, 1] for [UP, STAY, DOWN]
- **Reward**: To be implemented by you!

## Files
- `game_environment.py`: The main environment (modify rewards here)
- `game_objects.py`: Game object implementations
- `main.py`: Game loop and rendering

## Getting Started
1. Review the environment code
2. Implement your reward function in `game_environment.py`
3. Create your Q-Learning implementation
4. Train your agent! 
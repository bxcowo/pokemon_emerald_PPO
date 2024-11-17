# Exercise 1: Ping Pong Q-Learning

## Overview
Implement Q-Learning to train an AI agent to play Ping Pong through self-play. The environment supports both human play and accelerated training modes.

## Tasks
1. Implement state discretization for the continuous state space
2. Design an appropriate reward function
3. Create and implement the Q-Learning algorithm with self-play
4. Add epsilon-greedy exploration strategy
5. Train and evaluate your agent

## Environment Details
- **State Space**: Continuous values for ball position, velocity, and paddle positions
- **Action Space**: [-1, 0, 1] for [UP, STAY, DOWN]
- **Training Modes**: 
  - Human vs AI (visualization mode)
  - AI vs AI (fast training mode)

## Files
- `game_environment.py`: The main environment (modify rewards here)
- `game_objects.py`: Game object implementations
- `main.py`: Game loop and visualization
- `train.py`: (To be created) Training script for self-play

## Training Strategy
1. Create two Q-tables, one for each paddle
2. Run training episodes in fast-forward mode (no rendering)
3. Periodically save the Q-tables and evaluate performance
4. Use the best model for human vs AI matches

## Getting Started
1. Review the environment code
2. Create `train.py` for accelerated self-play training
3. Implement your reward function in `game_environment.py`
4. Train your agents!

## Tips
- Use pygame.HIDDEN flag during training to avoid rendering
- Save Q-tables periodically to resume training
- Track metrics for both paddles during self-play
- Evaluate against simple rule-based opponent periodically
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

## Implementation Tips

### State Discretization
Consider discretizing these continuous values:
- Ball position (x, y)
- Ball velocity (vx, vy)
- Paddle position
- Relative position between paddle and ball

Example approach:
```python
def discretize_state(state):
    # Example bins for each dimension
    pos_bins = [-1.0, -0.5, 0.0, 0.5, 1.0]
    vel_bins = [-1.0, 0.0, 1.0]
    # Use numpy.digitize for each state component
    discretized_state = (
        np.digitize(state['ball_x'], pos_bins),
        np.digitize(state['ball_y'], pos_bins),
        np.digitize(state['ball_vx'], vel_bins),
        np.digitize(state['ball_vy'], vel_bins),
        np.digitize(state['player_y'], pos_bins)
    )
    return discretized_state
```


### Training Loop Structure
1. Create a separate training script
2. Implement the Q-Learning update rule:
   ```python
   Q[state][action] = Q[state][action] + alpha * (
       reward + gamma * max(Q[next_state]) - Q[state][action]
   )
   ```
3. Use epsilon-greedy for exploration:
   ```python
   if random.random() < epsilon:
       action = random.choice(actions)
   else:
       action = np.argmax(Q[state])
   ```

### Hyperparameters to Tune
- Learning rate (alpha): Try 0.1 to 0.5
- Discount factor (gamma): Usually 0.9 to 0.99
- Exploration rate (epsilon): Start high (0.9) and decay over time
- Number of discretization bins per dimension

## Getting Started
1. Review the environment code
2. Implement your reward function in `game_environment.py`
3. Create a new file for Q-Learning implementation
4. Train your agent!

## Evaluation
Track these metrics during training:
- Average reward per episode
- Success rate (ball hits / misses)
- Learning curve (plot rewards over time)
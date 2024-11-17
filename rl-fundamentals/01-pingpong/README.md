# Exercise 1: Ping Pong Q-Learning

## Step-by-Step Guide

### 1. Environment Understanding
- Review `game_environment.py` to understand:
  - State space representation
  - Available actions
  - Game mechanics
  - Reward placeholder structure

### 2. State Space Design
- Implement discretization in `QAgent.discretize_state()`
- Consider which state variables are most relevant
- Choose appropriate bin sizes for each dimension

### 3. Q-Learning Implementation
- Complete the `QAgent` class in `train.py`:
  ```python
  def discretize_state()  # Convert continuous to discrete state
  def get_action()        # Epsilon-greedy action selection
  def update()           # Q-value update rule
  ```

### 4. Training Loop
- Run training episodes in fast-forward mode
- Monitor and log:
  - Average rewards
  - Win rates
  - Q-value convergence
- Save models periodically

### 5. Evaluation
- Test against rule-based AI
- Analyze performance metrics
- Visualize learned behavior

## Files
- `game_environment.py`: Core game logic and RL interface
- `game_objects.py`: Paddle and Ball implementations
- `main.py`: Human vs AI gameplay
- `train.py`: Self-play training implementation

## Development Tips
- Start with larger state space bins, then refine
- Test reward functions incrementally
- Use `set_training_mode(True)` for faster training
- Save checkpoints to resume training
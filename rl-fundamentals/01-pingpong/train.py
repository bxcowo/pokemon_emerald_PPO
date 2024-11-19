import pygame
import numpy as np
import pickle
import os
import csv
from collections import defaultdict
from typing import Dict, Tuple, List
from game_environment import PongEnvironment, FixedOpponent

# Definición de la clase QAgent
class QAgent:
    def __init__(self, state_bins: Dict[str, np.ndarray], actions: List[int], epsilon: float = 0.8, alpha: float = 0.1, gamma: float = 0.99):
        # Se inicializa q_table con defaultdict para que no inicializase con todos los estados al inicio
        # se llama a una función anónima (lambda) para asegurarnos que lo contengan sea otro diccionario con
        # sus respectivas acciones
        self.q_table = defaultdict(lambda: {action: 0.0 for action in actions})  # Inicializa Q-table de forma perezosa
        self.state_bins = state_bins
        self.actions = actions
        # Hiperparámetros de entrenamiento Q-Learning
        self.epsilon = epsilon  # Tasa de exploración inicial
        self.alpha = alpha  # Tasa de aprendizaje
        self.gamma = gamma  # Factor de descuento

    def _discretize_state(self, state: Dict[str, float]) -> Tuple:
        """Discretiza el estado continuo en bins definidos."""
        pos_bins = self.state_bins['pos']
        vel_bins = self.state_bins['vel']

        ball_x_bin = np.digitize(state['ball_x'], pos_bins)
        ball_y_bin = np.digitize(state['ball_y'], pos_bins)
        ball_vx_bin = np.digitize(state['ball_vx'], vel_bins)
        ball_vy_bin = np.digitize(state['ball_vy'], vel_bins)
        player_y_bin = np.digitize(state['player_y'], pos_bins)
        opponent_y_bin = np.digitize(state['opponent_y'], pos_bins)

        return ball_x_bin, ball_y_bin, ball_vx_bin, ball_vy_bin, player_y_bin, opponent_y_bin

    def get_action(self, state: Dict[str, float]) -> int:
        """Selecciona una acción usando la política epsilon-greedy."""
        discretized_state = self._discretize_state(state)
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)  # Exploración
        else:
            # Explotación: seleccionar la acción con el mayor valor Q
            return max(self.q_table[discretized_state], key=self.q_table[discretized_state].get)

    # Funcion para obtener valores en base a la tabla Q
    def get_action_with_q(self, state: Dict[str, float]) -> int:
        """Selecciona la acción con el mayor valor Q para el estado dado."""
        discretized_state = self._discretize_state(state)
        if discretized_state not in self.q_table:
            # Si el estado no está en la tabla Q, seleccionar una acción aleatoria
            return np.random.choice(self.actions)
        else:
            # Seleccionar la acción con el mayor valor Q
            return max(self.q_table[discretized_state], key=self.q_table[discretized_state].get)

    def update(self, state: Dict[str, float], action: int, reward: float, next_state: Dict[str, float],
               done: bool) -> None:
        """Actualiza la Q-table usando la fórmula de Q-Learning."""
        discretized_state = self._discretize_state(state)
        if done:
            target = reward  # No hay siguiente estado
        else:
            discretized_next_state = self._discretize_state(next_state)
            target = reward + self.gamma * max(self.q_table[discretized_next_state].values())

        # Actualización de la Q-table
        self.q_table[discretized_state][action] += self.alpha * (target - self.q_table[discretized_state][action])

    def decay_epsilon(self, min_epsilon: float = 0.01, decay_rate: float = 0.995) -> None:
        """Aplica decay a epsilon para reducir la exploración con el tiempo."""
        self.epsilon = max(min_epsilon, self.epsilon * decay_rate)


# Función para guardar la Q-table
def save_q_table(agent: QAgent, filename: str) -> None:
    """Guarda la Q-table del agente en un archivo utilizando pickle."""
    try:
        dirctry = 'Pickle-registers'
        os.makedirs(dirctry, exist_ok=True)
        filepath = os.path.join(dirctry, filename)

        with open(filepath, 'wb') as output_file:
            pickle.dump(dict(agent.q_table), output_file)
        print(f"Q-table guardada en {filename}")
    except IOError as e:
        print(f"Error al guardar la Q-table en {filename}: {e}")


# Función principal de entrenamiento
def train(episodes: int = 10000, save_interval: int = 1000, log_filename: str = 'training_metrics.csv') -> None:
    """Entrena el agente usando Q-Learning en el entorno Pong."""

    # Configuración de Pygame para modo headless (sin ventana visible)
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()

    # Configuración del entorno
    CONFIG = {
        'window_width': 800,
        'window_height': 600,
        'paddle_width': 15,
        'paddle_height': 90,
        'ball_size': 15,
        'paddle_speed': 5,
        'ball_speed': 7,
        'colors': {
            'white': (255, 255, 255),
            'black': (0, 0, 0)
        }
    }

    env = PongEnvironment(CONFIG)
    env.set_training_mode(True)  # Habilita el modo de entrenamiento rápido sin renderizar y más rápido

    # Definición de bins para discretización del estado
    state_bins = {
        'pos': np.linspace(-1, 1, 10),
        'vel': np.linspace(-1, 1, 5)
    }
    actions = [-1, 0, 1]  # Acciones: -1 (arriba), 0 (mantenerse), 1 (abajo)

    # Inicialización del agente y el oponente fijo
    agent = QAgent(state_bins, actions)
    opponent = FixedOpponent(env.opponent, env.ball)

    # Inicialización del archivo de log
    with open(log_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['episode', 'total_reward', 'epsilon']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Ciclo de entrenamiento
        for episode in range(1, episodes + 1):
            state = env.reset()
            done = False
            total_reward = 0

            while not done:
                action_agent = agent.get_action(state)
                action_opponent = opponent.get_action()

                next_state, rewards, done, _ = env.step(action_agent, action_opponent)
                agent.update(state, action_agent, rewards, next_state, done)

                state = next_state
                total_reward += rewards

                # Manejar eventos de Pygame para evitar bloqueos (aunque en modo headless no es estrictamente necesario)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

            # Aplicar decay a epsilon después de cada episodio
            agent.decay_epsilon()

            # Guardar métricas en el log
            writer.writerow({'episode': episode, 'total_reward': total_reward, 'epsilon': agent.epsilon})

            # Guardar la Q-table y mostrar progreso cada save_interval episodios
            if episode % save_interval == 0:
                save_q_table(agent, f'register_{episode}.pkl')
                print(f"Episode {episode} completado. Recompensa total: {total_reward}, Epsilon: {agent.epsilon:.4f}")

    pygame.quit()
    print("Entrenamiento completado.")


# Ejecutar la función de entrenamiento
if __name__ == "__main__":
    train(episodes=10000, save_interval=1000, log_filename='Pickle-registers/training_metrics.csv')


import numpy as np
import pickle
import pygame
from typing import Dict, Tuple
from game_environment import PongEnvironment
from train import QAgent, FixedOpponent

def load_q_table(filename: str) -> Dict[Tuple, Dict[int, float]]:
    """Carga la Q-table desde un archivo pickle."""
    try:
        with open(filename, 'rb') as input_file:
            q_table = pickle.load(input_file)
        print(f"Q-table cargada desde {filename}")
        return q_table
    except IOError as e:
        print(f"Error al cargar la Q-table desde {filename}: {e}")
        return {}


def test_agent(q_table_filename: str, episodes: int = 10) -> None:
    """Prueba el agente entrenado cargando la Q-table."""

    # Configuración del entorno (debe coincidir con la configuración del entrenamiento)
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

    # Inicializar Pygame
    pygame.init()
    screen = pygame.display.set_mode((CONFIG['window_width'], CONFIG['window_height']))
    pygame.display.set_caption("Prueba del Agente Entrenado Pong")
    clock = pygame.time.Clock()

    # Inicializar el entorno
    env = PongEnvironment(CONFIG)
    env.set_training_mode(False)  # Desactivar el modo de entrenamiento para ver el juego

    # Inicializar el agente y cargar la Q-table
    state_bins = {
        'pos': np.linspace(-1, 1, 10),
        'vel': np.linspace(-1, 1, 5)
    }
    actions = [-1, 0, 1]

    agent = QAgent(state_bins, actions)
    agent.q_table = load_q_table(q_table_filename)

    # Crear un oponente fijo o cualquier otra lógica que desees
    opponent = FixedOpponent(env.opponent, env.ball)

    for episode in range(1, episodes + 1):
        state = env.reset()
        done = False
        total_reward = 0

        while not done:
            # Manejar eventos de Pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Obtener acción del agente basado en la Q-table
            action_agent = agent.get_action_with_q(state)

            # Obtener acción del oponente fijo
            action_opponent = opponent.get_action()

            # Ejecutar un paso en el entorno
            next_state, rewards, done, _ = env.step(action_agent, action_opponent)

            # Actualizar el estado y la recompensa
            state = next_state
            total_reward += rewards

            # Renderizar el entorno
            env.render(screen)

            # Controlar la velocidad del juego
            clock.tick(60)  # 60 FPS

        print(f"Episode {episode} completado. Recompensa total: {total_reward}")

    pygame.quit()
    print("Prueba completada.")

if __name__ == "__main__":
    # Reemplaza 'register_10000.pkl' con el nombre de tu archivo Q-table
    test_agent(q_table_filename='Pickle-registers/register_10000.pkl', episodes=5)

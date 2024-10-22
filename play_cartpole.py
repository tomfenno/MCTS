from cartpole import CartPoleState
from mcts import mcts

def play_game():
    game = CartPoleState()

    game.env.render()

    while not game.is_terminal():
        action = mcts(game, iteration_limit=100)
        reward, done = game.take_action(action)
        if done:
            break

    game.env.close()

if __name__ == "__main__":
    play_game()
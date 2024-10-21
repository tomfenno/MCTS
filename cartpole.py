import gym

class CartPoleState:
    def __init__(self, name="CartPole-v0"):
        self.env = gym.make(name)
        self.state = self.env.reset()
        self.possible_actions = self.env.action_space.n
        self.observation = self.env.observation_space.shape[0]

    def is_terminal():
        return

    def get_actions():
        return

    def take_action():
        return

    def get_utility():
        return
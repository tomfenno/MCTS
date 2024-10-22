import gym
from copy import deepcopy

class CartPoleState:
    def __init__(self, name="CartPole-v1"):
        self.env = gym.make(name, render_mode="human")
        self.state = self.env.reset()
        self.possible_actions = self.env.action_space.n
        self.observation = self.env.observation_space.shape[0]
        self.reward = 0
        self.terminal = False

    def is_terminal(self):
        _ , _ , done, truncated, _ = self.env.step(0)
        return done or truncated 

    def get_actions(self):
        return range(self.possible_actions)

    def take_action(self, action):
        next_state, reward, done, truncate, info = self.env.step(action)
        self.state = next_state
        return next_state

    def get_utility(self):
        return self.reward
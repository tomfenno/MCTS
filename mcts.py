import numpy as np
import math
import time
import random
from copy import deepcopy

C = math.sqrt(2)

# def random_policy(state):
#     while not state.is_terminal():
#         action = random.choice(state.get_actions())
#         node_state = state.take_action()
#         return node_state.get_utility()

class Node():
    def __init__(self, state, parent,):
        self.state = state
        self.parent = parent
        self.terminal = state.is_terminal()
        self.exhausted = self.terminal
        self.visits = 0
        self.utility = 0
        self.player = state.get_player()
        self.children = {}

def mcts(initial_state, time_limit=None, iteration_limit=None):
    root = Node(initial_state, None)
    if time_limit:
        while time.time() < time_limit:
            playout(root)
    else:
        count = 0
        while count < iteration_limit:
            playout(root)
            count += 1
    

def select(node):
    while not node.terminal:
        if node.exhausted:
            node = select_child(node)
        else:
            return expand(node)
        
def expand(node):
    actions = node.state.get_actions()
    for action in actions:
        if action not in node.children:
            new_node = Node(node.state.take_action(), node)
            node.children[action] = new_node
            return new_node
        
def simulate(state):
    while not state.is_terminal():
        action = random.choice(state.get_actions())
        node_state = state.take_action()
        return node_state.get_utility()
    
def backpropogate(node, utility):
    while node is not None:
        node.visits += 1
        node.utility += node.player * utility
        node = node.parent

def playout(node):
    selected_node = select(node)
    utility = simulate(selected_node)
    backpropogate(selected_node, utility)

def select_child(node):
    highest_UCB1 = float("-inf")
    best_nodes = []
    for child in node.children.values():
        ucb1 = ( child.utility / child.visits ) + C * math.sqrt( math.log(node.visits) / child.visits )
        if ucb1 > highest_UCB1:
            highest_UCB1 = ucb1
            best_nodes[child]
        elif ucb1 == highest_UCB1:
            best_nodes.append(child)
        return random.choice(best_nodes)
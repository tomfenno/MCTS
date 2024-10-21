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
        end_time = time.time() + time_limit
        while time.time() < end_time:
            playout(root)
    else:
        count = 0
        while count < iteration_limit:
            playout(root)
            count += 1

    best_child = most_visited(root)

    for action, child in root.children.items():
        if child == best_child:
            return action


def select(node):
    while not node.terminal:
        if node.exhausted:
            node = select_child(node)
        else:
            return expand(node)
    return node
        
def expand(node):
    actions = node.state.get_actions()

    for action in actions:
        if action not in node.children:
            new_node = Node(node.state.take_action(action), node)
            node.children[action] = new_node
            if len(actions) == len(node.children):
                node.exhausted = True
            return new_node
        
def simulate(node):
    sim_node = deepcopy(node)
    while not sim_node.state.is_terminal():
        action = random.choice(sim_node.state.get_actions())
        sim_node.state = sim_node.state.take_action(action)
    return sim_node.state.get_utility()
    
def backpropogate(node, utility):
    while node is not None:
        node.visits += 1
        node.utility += utility
        node = node.parent

def playout(node):
    selected_node = select(node)
    utility = simulate(selected_node)
    backpropogate(selected_node, utility)

def select_child(node):
    highest_UCB1 = float("-inf")
    best_nodes = []

    for child in node.children.values():
        if child.visits == 0:
            return child
        ucb1 = (child.utility / child.visits) + C * math.sqrt(math.log(node.visits) / child.visits)
        if ucb1 > highest_UCB1:
            highest_UCB1 = ucb1
            best_nodes = [child]
        elif ucb1 == highest_UCB1:
            best_nodes.append(child)
    
    return random.choice(best_nodes)

def most_visited(node):
    most_visits = 0
    best_nodes = []

    for child in node.children.values():
        if child.visits > most_visits:
            most_visits = child.visits
            best_nodes = [child]
        elif child.visits == most_visits:
            best_nodes.append(child)      
        if len(best_nodes) == 1:
            return best_nodes[0]
        else:
            best_nodes.clear()
            best_ratio = float("-inf")
            for node in best_nodes:
                ratio = node.utility / node.visits
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_nodes = [node]
                elif ratio == best_ratio:
                    best_nodes.append(node)
    
    return random.choice(best_nodes)
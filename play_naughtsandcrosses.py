from naughtsandcrosses import NaughtsAndCrossesState, Action
from mcts import mcts  # Import your MCTS implementation

def play_game():
    # Initialize the game state
    current_state = NaughtsAndCrossesState()

    # Print the initial board
    print_board(current_state)

    while not current_state.is_terminal():
        if current_state.get_player() == -1:
            print("Your turn!")
            valid_move = False
            while not valid_move:
                try:
                    col = int(input("Enter the column (1-3): "))
                    row = int(input("Enter the row (1-3): "))
                    action = Action(player=-1, x=row - 1, y=col - 1)
                    if action in current_state.get_actions():
                        valid_move = True
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please enter valid row/column numbers.")

            current_state = current_state.take_action(action)
            print_board(current_state) 
        else:
            print("Monty is thinking...")
            action = mcts(current_state, iteration_limit=10)
            print(f"Monty chose action: {action}")
            current_state = current_state.take_action(action)
            print_board(current_state)
            
    # Game over
    utility = current_state.get_utility()
    if utility == 0:
        print("The game is a draw!")
    elif utility < 0:
        print("Player X wins!")
    else:
        print("Monty wins!")

def print_board(state):
    board = state.board
    symbols = {-1: 'X', 1: 'O', 0: ' '}
    for row in board:
        print(" | ".join([symbols[cell] for cell in row]))
        print()
        # print("-" * 5)

if __name__ == "__main__":
    play_game()

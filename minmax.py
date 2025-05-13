from movement2 import select_safe_move
from gameLogic import isGameOver, makeMove, createGameState
from heuristics import evaluatePoint
import json 
import os
import copy
from time import time

def save_game_state(game_state, current_turn, depth, moves, heuristic_value=None):
    # Ensure the directory exists
    turn = game_state["turn"]
    game_state["heuristic_value"] = heuristic_value
    directory = f"json/{turn}"
    os.makedirs(directory, exist_ok=True)
    moves = "-".join(moves)

    # Save the game state as a JSON file
    file_path = os.path.join(directory, f"{depth}_{moves}_.json")
    with open(file_path, "w") as f:
        json.dump(game_state, f, indent=4)

def miniMax(game_state, depth, curr_snake_id, main_snake_id, previous_snake_id,
            return_move, alpha, beta, current_turn, list_of_moves=[]):
    # If given game_state reached an end or depth has reached zero, return game_state score
    maximizer = False
    for index, snake in enumerate(game_state["snakes"]):
        if (snake["id"] == curr_snake_id):
            if(snake["name"] == "Agent25-G12"):
                maximizer = True
            break
    SAVE_GAME_STATE = False

    if (depth == 0 or isGameOver(game_state, previous_snake_id)):
        #save the game state in a json file 
        heuristic_value = evaluatePoint(game_state, depth, curr_snake_id, main_snake_id, current_turn)
        if SAVE_GAME_STATE:
            save_game_state(game_state, current_turn, depth, list_of_moves, heuristic_value = heuristic_value)
        return heuristic_value
    # get the id of the next snake that we're gonna minimax
    curr_index = 0
    #for index, snake in enumerate(game_state["board"]["snakes"]):
    for index, snake in enumerate(game_state["snakes"]):
        if (snake["id"] == curr_snake_id):
            curr_index = index
            break

    #next_snake_id = game_state["board"]["snakes"][(curr_index + 1) % len(game_state["board"]["snakes"])]["id"]
    next_snake_id = game_state["snakes"][(curr_index + 1) % len(game_state["snakes"])]["id"]

    moves = select_safe_move(game_state, snake_id=curr_snake_id)

    if (maximizer):  #i.e. the maximizer
        highest_value = float("-inf")
        best_move = None
        for move in moves:
            # Makes a copy of the current game state with the current snake taking a possible move
            new_game_state = makeMove(game_state, curr_snake_id, move)
            list_of_moves_ = copy.copy(list_of_moves)
            list_of_moves_.append(move)
            curr_val = miniMax(new_game_state, depth - 1, next_snake_id,
                               main_snake_id, curr_snake_id, False, alpha,
                               beta, current_turn + 1, list_of_moves_)
            # print(f"{curr_snake_id} {move}: {curr_val}")
            if (curr_val > highest_value):
                best_move = move
                highest_value = curr_val

            alpha = max(alpha, curr_val)

            if (alpha >= beta):
                break

        # print(f"highest :   {curr_snake_id} {best_move}: {highest_value}")
        if SAVE_GAME_STATE:
            save_game_state(game_state, current_turn, depth, list_of_moves, heuristic_value = heuristic_value)

        return (highest_value, best_move) if return_move else highest_value

    else:
        min_value = float("inf")
        best_move = None
        for move in moves:
            new_game_state = makeMove(game_state, curr_snake_id, move)
            list_of_moves_ = copy.copy(list_of_moves)
            list_of_moves_.append(move)
            curr_val = miniMax(new_game_state, depth - 1, next_snake_id,
                               main_snake_id, curr_snake_id, False, alpha,
                               beta, current_turn,list_of_moves_)
            # print(f"{curr_snake_id} {move}: {curr_val}")
            if (min_value > curr_val):
                best_move = move
                min_value = curr_val

            beta = min(curr_val, beta)

            if (beta <= alpha):
                break

        if SAVE_GAME_STATE:
            save_game_state(game_state, current_turn, depth, list_of_moves, heuristic_value = heuristic_value)

        return (min_value, best_move) if return_move else min_value


# Main function
def miniMax_value(game_state):

    
    others = {}
    current_game_state = createGameState(game_state, game_state["you"]["id"])
    print( select_safe_move(current_game_state, snake_id=current_game_state["main_snake_id"]))
    current_turn = game_state["turn"]
    for index, snake in enumerate(current_game_state["snakes"]):
        print(snake["name"])

    snakes_num = len(game_state["board"]["snakes"])

    if (snakes_num == 4):
        depth = 10
    elif (snakes_num == 3):
        depth = 10
    elif (snakes_num == 2):
        depth = 10
    else:
        depth = 10
    #depth = 6

    t0 = time()
    result_value, best_move = miniMax(current_game_state, depth,
                                      game_state["you"]["id"],
                                      game_state["you"]["id"], None, True,
                                      float("-inf"), float("inf"),
                                      current_turn)
    if best_move is None:
        best_move = select_safe_move(current_game_state, snake_id=current_game_state["main_snake_id"])[0]
    t1 = time()
    duration = t1 - t0
    others["time"] = duration
    print(f"Time taken: {t1 - t0:.4f} seconds")
    print(f"Minimax value: {result_value}, Best move: {best_move}")

    

    return best_move, others

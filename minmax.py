from movement import select_safe_move
from gameLogic import isGameOver, makeMove, createGameState
from heuristics import evaluatePoint


def miniMax(game_state, depth, curr_snake_id, main_snake_id, previous_snake_id,
            return_move, alpha, beta, current_turn):
    # If given game_state reached an end or depth has reached zero, return game_state score
    if (depth == 0 or isGameOver(game_state, previous_snake_id)):
        return evaluatePoint(game_state, depth, curr_snake_id, current_turn)

    # get the id of the next snake that we're gonna minimax
    curr_index = 0
    for index, snake in enumerate(game_state["board"]["snakes"]):
        if (snake["id"] == curr_snake_id):
            curr_index = index
            break

    next_snake_id = game_state["board"]["snakes"][(curr_index + 1) %
                                         len(game_state["board"]["snakes"])]["id"]

    moves = select_safe_move(game_state, snake_id=next_snake_id)

    if (curr_snake_id == main_snake_id):  #i.e. the maximizer
        highest_value = float("-inf")
        best_move = None
        for move in moves:
            # Makes a copy of the current game state with the current snake taking a possible move
            new_game_state = makeMove(game_state, curr_snake_id, move)
            curr_val = miniMax(new_game_state, depth - 1, next_snake_id,
                               main_snake_id, curr_snake_id, False, alpha,
                               beta, current_turn + 1)
            # print(f"{curr_snake_id} {move}: {curr_val}")
            if (curr_val > highest_value):
                best_move = move
                highest_value = curr_val

            alpha = max(alpha, curr_val)

            if (alpha >= beta):
                break

        # print(f"highest :   {curr_snake_id} {best_move}: {highest_value}")

        return (highest_value, best_move) if return_move else highest_value

    else:
        min_value = float("inf")
        best_move = None
        for move in moves:
            new_game_state = makeMove(game_state, curr_snake_id, move)
            curr_val = miniMax(new_game_state, depth - 1, next_snake_id,
                               main_snake_id, curr_snake_id, False, alpha,
                               beta, current_turn)
            # print(f"{curr_snake_id} {move}: {curr_val}")
            if (min_value > curr_val):
                best_move = move
                min_value = curr_val

            beta = min(curr_val, beta)

            if (beta <= alpha):
                break

        return (min_value, best_move) if return_move else min_value


# Main function
def miniMax_value(game_state, safe_moves):
    current_game_state = createGameState(game_state, game_state["you"]["id"])
    current_turn = game_state["turn"]

    snakes_num = len(game_state["board"]["snakes"])

    if (snakes_num == 4):
        depth = 2
    elif (snakes_num == 3):
        depth = 2
    elif (snakes_num == 2):
        depth = 2
    else:
        depth = 2

    result_value, best_move = miniMax(current_game_state, depth,
                                      game_state["you"]["id"],
                                      game_state["you"]["id"], None, True,
                                      float("-inf"), float("inf"),
                                      current_turn)
    print(f"Minimax value: {result_value}, Best move: {best_move}")

    if (best_move is not None):
        if (best_move in safe_moves):
            safe_moves[best_move] += result_value

    return best_move

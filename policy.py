import random as rd
from movement import select_safe_move
import copy
import random

def choose_move(safe_moves, game_state, args={"policy": "random"}):
    if args["policy"] == "random":
        return rd.choice(safe_moves)
    elif args["policy"] == "minmax":
        depth = args.get("depth", 3)  # Default depth of 3 if not specified
        return minmax(safe_moves, game_state, depth)


def manhattan_distance(p1, p2):
    return abs(p1["x"] - p2["x"]) + abs(p1["y"] - p2["y"])

def evaluate_state(game_state):
    """Simple heuristic: closer to food is better."""
    head = game_state["you"]["body"][0]
    food = game_state["board"]["food"]
    if not food:
        return 0
    distances = [manhattan_distance(head, f) for f in food]
    return -min(distances)  

def get_all_snakes_in_turn_order(game_state):
    return sorted(game_state["board"]["snakes"], key=lambda s: len(s["body"]), reverse=True)

def simulate_move(snake, move):
    head = snake["body"][0].copy()
    if move == "up":
        head["y"] += 1
    elif move == "down":
        head["y"] -= 1
    elif move == "left":
        head["x"] -= 1
    elif move == "right":
        head["x"] += 1
    return head

def apply_move_to_snake(snake, move):
    new_head = simulate_move(snake, move)
    new_body = [new_head] + snake["body"][:-1]  # Simplified, doesn't handle food
    return {"id": snake["id"], "body": new_body}

def minmax(safe_moves, game_state, depth, is_max=True, snake_index=0):
    if depth == 0 or len(game_state["board"]["snakes"]) <= 1:
        return evaluate_state(game_state)

    snakes = get_all_snakes_in_turn_order(game_state)
    current_snake = snakes[snake_index]

  
    is_you = current_snake["id"] == game_state["you"]["id"]
    moves = ["up", "down", "left", "right"]  # Could filter with select_safe_move()
    moves = select_safe_move(game_state, snake_id = current_snake["id"])
    

    best_value = float('-inf') if is_you else float('inf')
    for move in moves:
        new_game_state = copy.deepcopy(game_state)
        new_snakes = new_game_state["board"]["snakes"]

        # Apply move
        for idx, s in enumerate(new_snakes):
            if s["id"] == current_snake["id"]:
                new_snakes[idx] = apply_move_to_snake(s, move)

        # Advance turn
        next_index = (snake_index + 1) % len(snakes)
        next_is_max = (new_snakes[next_index]["id"] == new_game_state["you"]["id"])

        value = minmax(safe_moves, new_game_state, depth - 1, next_is_max, next_index)

        if is_you:
            best_value = max(best_value, value)
        else:
            best_value = min(best_value, value)

    if depth == 3 and is_max:  # Top-level decision
        best_moves = []
        best_score = float('-inf')
        for move in safe_moves:
            new_game_state = copy.deepcopy(game_state)
            new_snakes = new_game_state["board"]["snakes"]
            for idx, s in enumerate(new_snakes):
                if s["id"] == game_state["you"]["id"]:
                    new_snakes[idx] = apply_move_to_snake(s, move)

            value = minmax(safe_moves, new_game_state, depth - 1, False, 1)
            if value > best_score:
                best_score = value
                best_moves = [move]
            elif value == best_score:
                best_moves.append(move)

        return random.choice(best_moves)

    return best_value

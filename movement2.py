def select_safe_move(game_state, snake_id= None):
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    
    # Get current snake
    curr_snake = None
    if snake_id is not None:
        for snake in game_state["snakes"]:
            if snake["id"] == snake_id:
                curr_snake = snake
                break
    else:
        for snake in game_state["snakes"]:
            if snake["id"] == game_state["curr_snake_id"]:
                curr_snake = snake
                break
        
    if curr_snake is None:
        return []  # Fallback in case the snake isn't found
    
    my_head = curr_snake["head"]
    my_body = curr_snake["body"]
    my_neck = my_body[1] if len(my_body) > 1 else my_head

    # Avoid moving back into the neck
    if my_neck[0] < my_head[0]:  # Neck is left
        is_move_safe["left"] = False
    elif my_neck[0] > my_head[0]:  # Neck is right
        is_move_safe["right"] = False
    elif my_neck[1] < my_head[1]:  # Neck is below
        is_move_safe["down"] = False
    elif my_neck[1] > my_head[1]:  # Neck is above
        is_move_safe["up"] = False

    board_width, board_height = game_state["shape"]
    is_move_safe = prevent_out_of_bounds(my_head, board_width, board_height, is_move_safe)
    is_move_safe = prevent_collision_with_self(my_body, is_move_safe)

    opponents = [s for s in game_state["snakes"] if s["id"] != curr_snake["id"]]
    is_move_safe = prevent_collision_with_opponents(opponents, my_head, is_move_safe)

    is_move_safe2 = prevent_potential_collision_with_opponents_head(opponents, my_head, my_body,  is_move_safe)

    #if there is a least one move safe in is_move_safe2
    if any(is_move_safe2.values()):
        is_move_safe = is_move_safe2

    return [move for move, safe in is_move_safe.items() if safe]


def prevent_out_of_bounds(my_head, board_width, board_height, is_move_safe):
    x, y = my_head
    if x == 0:
        is_move_safe["left"] = False
    if x == board_width - 1:
        is_move_safe["right"] = False
    if y == 0:
        is_move_safe["down"] = False
    if y == board_height - 1:
        is_move_safe["up"] = False
    return is_move_safe


def prevent_collision_with_self(my_body, is_move_safe):
    head = my_body[0]
    for body_part in my_body[1:-1]:
        for move in list(is_move_safe.keys()):
            if is_move_safe[move] and not is_a_move_safe(move, head, body_part):
                is_move_safe[move] = False
    return is_move_safe


def prevent_collision_with_opponents(opponents, my_head, is_move_safe):
    for opponent in opponents:
        for body_part in opponent["body"][:-1]:
            for move in list(is_move_safe.keys()):
                if is_move_safe[move] and not is_a_move_safe(move, my_head, body_part):
                    is_move_safe[move] = False
    return is_move_safe


def is_a_move_safe(move, head, body_part):
    x, y = head
    bx, by = body_part
    if move == "up" and (x, y + 1) == (bx, by):
        return False
    if move == "down" and (x, y - 1) == (bx, by):
        return False
    if move == "left" and (x - 1, y) == (bx, by):
        return False
    if move == "right" and (x + 1, y) == (bx, by):
        return False
    return True

def move_to_vector(move):
    if move == "up":
        return (0, 1)
    elif move == "down":
        return (0, -1)
    elif move == "left":
        return (-1, 0)
    elif move == "right":
        return (1, 0)
    else:
        raise ValueError("Invalid move direction")

def prevent_potential_collision_with_opponents_head(opponents, my_head, my_body, is_move_safe):
    new_is_move_safe = {key: value for key, value in is_move_safe.items()}

    for opponent in opponents:
        opponent_head = opponent["head"]
        opponent_length = len(opponent["body"])
        
        for move in is_move_safe:
            if not is_move_safe[move]:
                continue  # Skip already unsafe moves

            # Simulate moving to that position
            dx, dy = move_to_vector(move)
            new_head = (my_head[0] + dx, my_head[1] + dy)

            diff = (abs(new_head[0] - opponent_head[0]), abs(new_head[1] - opponent_head[1]))

            # If the heads could both move into the same square next turn
            if diff == (1, 0) or diff == (0, 1):
                if opponent_length >= len(my_body):
                    new_is_move_safe[move] = False

    return new_is_move_safe

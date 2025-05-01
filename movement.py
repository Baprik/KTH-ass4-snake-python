def select_safe_move(game_state, snake_id = False):
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    if snake_id:
        snake = game_state["board"]["snakes"][0]
        for s in game_state["board"]["snakes"]:
            if s["id"] == snake_id:
                snake = s
                break
        my_head = snake["body"][0]
        my_neck = snake["body"][1]
    else:
        my_head = game_state["you"]["body"][0]  # Coordinates of your head
        my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
    
    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
      is_move_safe["left"] = False
    
    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
      is_move_safe["right"] = False
    
    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
      is_move_safe["down"] = False
    
    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
      is_move_safe["up"] = False
    
    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    
    is_move_safe = prevent_out_of_bounds(my_head, board_width, board_height,
                                       is_move_safe)
    
    
    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
    
    is_move_safe = prevent_collision_with_self(my_body, is_move_safe)
    
    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = [
      snake for snake in game_state['board']['snakes']
      if snake['id'] != game_state['you']['id']
    ]
    is_move_safe = prevent_collision_with_opponents(opponents, my_body,
                                                  is_move_safe)
    
    safe_moves = []
    for move, isSafe in is_move_safe.items():
      if isSafe:
          safe_moves.append(move)
          
    return safe_moves

def prevent_out_of_bounds(my_head, board_width, board_height, is_move_safe):
  if my_head['x'] == 0:
      is_move_safe['left'] = False
  if my_head['x'] == board_width - 1:
      is_move_safe['right'] = False
  if my_head['y'] == 0:
      is_move_safe['down'] = False
  if my_head['y'] == board_height - 1:
      is_move_safe['up'] = False
  return is_move_safe


def prevent_collision_with_self(my_body, is_move_safe):
  my_head = my_body[0]
  for body_part in my_body[1:-1]:
      for move, isSafe in is_move_safe.items():
          if isSafe:
              is_move_safe[move] = is_a_move_safe(move, my_head, body_part)
  return is_move_safe


def is_a_move_safe(move, head, body_part):
  if move == 'up' and body_part['y'] == head['y'] + 1 and body_part[
          'x'] == head['x']:
      return False
  if move == 'down' and body_part['y'] == head['y'] - 1 and body_part[
          'x'] == head['x']:
      return False
  if move == 'left' and body_part['x'] == head['x'] - 1 and body_part[
          'y'] == head['y']:
      return False
  if move == 'right' and body_part['x'] == head['x'] + 1 and body_part[
          'y'] == head['y']:
      return False
  return True


def prevent_collision_with_opponents(opponents, my_body, is_move_safe):
  my_head = my_body[0]
  for opponent in opponents:
      for body_part in opponent['body']:
          for move, isSafe in is_move_safe.items():
              if isSafe:
                  is_move_safe[move] = is_a_move_safe(
                      move, my_head, body_part)
  return is_move_safe
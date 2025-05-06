import copy

def createGameState(game_state, curr_snake_id):
  # dict_keys(['game', 'turn', 'board', 'you'])
  #for init in main function
  game_state_copy = copy.deepcopy(game_state)
  game_state_copy["curr_snake_id"] = curr_snake_id
  return game_state_copy

def createNewGameState(game_state, curr_snake_id):
  new_game_state = copy.deepcopy(game_state)
  new_game_state["curr_snake_id"] = curr_snake_id

  return new_game_state

def isGameOver(game_state, snake_id):
  if (snake_id is None):
      return False

  if (game_state is None):
      return True

  snake_state = game_state["board"]["snakes"]

  for snake in snake_state:
      if (snake["id"] == snake_id):
          return False
  return True


# Creates a new version of game state with the move and the correspondent snake
def makeMove(game_state, curr_snake_id, move):
    board_width = game_state["board"]["width"]
    board_height =  game_state["board"]["height"]

    # new game state to update, change the id to current snake
    new_game_state = createNewGameState(
        game_state, curr_snake_id)

    # Our snake's head coordinates
    head_x, head_y = findHeadCoord(new_game_state, curr_snake_id)

    # Current snake does not exist
    if (head_x is None or head_y is None):
        return None

    # Update head coordinate value to destination after move is applied
    head_x, head_y = updateHeadCoord(head_x, head_y, move)

    # Acquire current snake info
    curr_snake_index = findCurrentSnake(new_game_state, curr_snake_id)
    if curr_snake_index is None:
        print("Snake index is None !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return None

    current_snake = new_game_state["board"]["snakes"][curr_snake_index]



    # Check if snake destination hits border
    if not (0 <= head_x < board_width and 0 <= head_y < board_height):
        removeKilledSnake(new_game_state, curr_snake_index)
        return new_game_state


    # Checks if snake runs into another snake or edge boundary
    collide_with_snake = False
    collide_with_snake_head = False
    collide_with_food = False
    potential_snake_collided = None
    potential_snake_index = 0
  

    for idx, snake in enumerate(new_game_state["board"]["snakes"]):
        if snake["head"]["x"] == head_x and snake["head"]["y"] == head_y:
            collide_with_snake_head = True
            potential_snake_collided = snake
            potential_snake_index = idx
            break
        for body_part in snake["body"]:
            if body_part["x"] == head_x and body_part["y"] == head_y:
                potential_snake_collided = snake
                collide_with_snake = True
                break
    for food in new_game_state["board"]["food"]:
        if food["x"] == head_x and food["y"] == head_y:
            collide_with_food = True
            break

    # if collision is with the head of a snake
    if (collide_with_snake_head):
        destination_snake_length = 0
        destination_snake_index = 0

        # Find the snake the current snake is about to collide with

        destination_snake_length = potential_snake_collided["length"]
        curr_snake_length = current_snake["length"]


        # Our size is bigger and we kill the another snake
        if (destination_snake_length < curr_snake_length):

            # Remove destination snake from game board and snake state
            removeKilledSnake(new_game_state, potential_snake_index)

            # Index might have changed when snake is removed
            curr_snake_index = findCurrentSnake(new_game_state, curr_snake_id)
            if curr_snake_index is None:
                print("Snake index is None !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return None

            # Snake moves forward and updates all coords in new game state
            moveForward(new_game_state, curr_snake_index, head_x, head_y, False)

            curr_health = updateSnakeHealth(current_snake, True, False)

            # check if our snake ran out of health
            if (curr_health <= 0):
                removeKilledSnake(new_game_state, curr_snake_index)

        # Our snake is smaller or same size
        else:
            removeKilledSnake(new_game_state, curr_snake_index)

            # Index might have changed when snake is removed
            destination_snake_index = findCurrentSnake(new_game_state, destination_snake_index)
            if destination_snake_index is None:
                print("Snake index is None !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return None

            # Same size case
            if (destination_snake_length == curr_snake_length):
                removeKilledSnake(new_game_state, destination_snake_index)

        return new_game_state

    elif collide_with_snake:
        # TODO handle tail collision ?? 
        removeKilledSnake(new_game_state, curr_snake_index)
        return new_game_state

    # Snake move to a cell with food
    elif collide_with_food:
        # Snake moves forward and updates all coords in new game state
        moveForward(new_game_state, curr_snake_index, head_x, head_y, True)
  
        updateSnakeHealth(current_snake, True, True)
  
        return new_game_state

    # Snake's regular movement to empty spaces
    else:

        # Snake moves forward and updates all coords in new game state
        moveForward(new_game_state, curr_snake_index, head_x, head_y, False)

        curr_health = updateSnakeHealth(current_snake, True, False)
  
        # check if our snake ran out of health
        if (curr_health <= 0):
            removeKilledSnake(new_game_state, curr_snake_index)

        return new_game_state


def findHeadCoord(new_gamestate, curr_snake_id):
  snakes = new_gamestate["board"]["snakes"]
  for snake in snakes:
    if snake["id"] == curr_snake_id:
      return snake["head"]["x"], snake["head"]["y"]  
  return None, None

def updateHeadCoord(head_x, head_y, move):
  if move == "up":
    head_y += 1
  elif move == "down":
    head_y -= 1
  elif move == "left":
    head_x -= 1
  elif move == "right":
    head_x += 1
  return head_x, head_y

def findCurrentSnake(new_game_state, curr_snake_id):
  curr_snake_index = 0
  new_snake_state = new_game_state["board"]["snakes"]
  for snake in new_snake_state:
    if snake["id"] == curr_snake_id:
      return curr_snake_index
    curr_snake_index += 1
  return None

def removeKilledSnake(gamestate, snake_index):
  if snake_index == None:
      print("Snake index is None !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      return
  if(gamestate["board"]["snakes"] == []):
      print("No snakes left !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      return
  gamestate["board"]["snakes"].pop(snake_index)



def moveForward(game_state,  curr_snake_index, head_x, head_y, eat_food):
  
    snake = game_state["board"]["snakes"][curr_snake_index]
    snake["head"]["x"] = head_x
    snake["head"]["y"] = head_y

    snake["body"].insert(0, {"x": head_x, "y": head_y})

    if not eat_food:
        snake["body"].pop(-1)
        print("simulate not eating")


# Update snake's health, -1 health for every turn or 0 if snake dies
def updateSnakeHealth(snake, isAlive, hasAte):
    if (hasAte):
        snake["health"] = 100
    elif (isAlive):
        snake["health"] -= 1
    else:
        snake["health"] = 0
    return snake["health"]


      


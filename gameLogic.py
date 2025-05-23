import copy
from utils import border_kill, flood_fill_area
def createGameState(original_game_state, curr_snake_id):
  # dict_keys(['game', 'turn', 'board', 'you'])
  #for init in main function
  #game_state_copy = copy.deepcopy(game_state)
  #game_state_copy["curr_snake_id"] = curr_snake_id

  snakes = []
  for snake in original_game_state["board"]["snakes"]:

    snake_body = [(body_part["x"],body_part["y"]) for body_part in snake["body"]]
    snake_id = snake["id"]
    snake_health = snake["health"]
    snake_name = snake["name"]
    snake_head = (snake["head"]["x"], snake["head"]["y"])

    snake_dict = {
        "id": snake_id,
        "body": snake_body,
        "health": snake_health,
        "head": snake_head,
        "name": snake_name,
        "first_move": None
    }
    snakes.append(snake_dict)

  new_game_state = {
     "shape" : (original_game_state["board"]["width"], original_game_state["board"]["height"]),
      "food" : [( food_pos["x"], food_pos["y"]) for food_pos in original_game_state["board"]["food"]],
      "snakes" : snakes,
      "main_snake_id" : original_game_state["you"]["id"], # -> [max_id1, max_id2 ] 
      "curr_snake_id" : curr_snake_id,
  }
  return new_game_state

def createNewGameState(game_state, curr_snake_id):
  #new_game_state = copy.deepcopy(game_state)
  #new_game_state["curr_snake_id"] = curr_snake_id

  new_game_state = {
    "shape" : game_state["shape"],
    "food" : [(x, y) for x,y in game_state["food"]],
    "snakes" : copy.deepcopy(game_state["snakes"]),
    "main_snake_id" : game_state["main_snake_id"],
    "curr_snake_id" : curr_snake_id,
  }

  return new_game_state

def isGameOver(game_state, snake_id):
  if (snake_id is None):
      return False

  if (game_state is None):
      return True

  #snake_state = game_state["board"]["snakes"]
  snake_state = game_state["snakes"]

  for snake in snake_state:
      if snake["id"] == snake_id  :
          if (snake["health"] <= 0):
              return True
          return False
          if border_kill(game_state, snake): #it is in a position where it is going to die (if the ennemi plays well)
              return True
          if flood_fill_area(game_state, snake["head"]) <= len(snake["body"]):
              return True
          
          
  return True


# Creates a new version of game state with the move and the correspondent snake
def makeMove(game_state, curr_snake_id, move):
    
    #board_width = game_state["board"]["width"]
    #board_height =  game_state["board"]["height"]
    board_width, board_height = game_state["shape"]

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
        return None

    #current_snake = new_game_state["board"]["snakes"][curr_snake_index]
    current_snake = new_game_state["snakes"][curr_snake_index]
    if current_snake["first_move"] == None:
       current_snake["first_move"] = (head_x, head_y)



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
  

    #for idx, snake in enumerate(new_game_state["board"]["snakes"]):
    for idx, snake in enumerate(new_game_state["snakes"]):
        #if snake["head"]["x"] == head_x and snake["head"]["y"] == head_y:
        if snake["head"] == (head_x, head_y):
            collide_with_snake_head = True
            potential_snake_collided = snake
            potential_snake_index = idx
            break
        for body_part in snake["body"]:
            #if body_part["x"] == head_x and body_part["y"] == head_y:
            if body_part == (head_x, head_y):
                potential_snake_collided = snake
                collide_with_snake = True
                break
    #for food in new_game_state["board"]["food"]:
    for food in new_game_state["food"]:
        #if food["x"] == head_x and food["y"] == head_y:
        if food == (head_x, head_y):
            collide_with_food = True
            new_game_state["food"].remove(food)
            break

    # if collision is with the head of a snake
    if (collide_with_snake_head):
        destination_snake_length = 0
        destination_snake_index = 0

        # Find the snake the current snake is about to collide with

        #destination_snake_length = potential_snake_collided["length"]
        destination_snake_lenghth = len(potential_snake_collided["body"])
        #curr_snake_length = current_snake["length"]
        curr_snake_length = len(current_snake["body"])


        # Our size is bigger and we kill the another snake
        if (destination_snake_length < curr_snake_length):

            # Remove destination snake from game board and snake state
            removeKilledSnake(new_game_state, potential_snake_index)

            # Index might have changed when snake is removed
            curr_snake_index = findCurrentSnake(new_game_state, curr_snake_id)
            if curr_snake_index is None:
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
  #snakes = new_gamestate["board"]["snakes"]
  snakes = new_gamestate["snakes"]
  for snake in snakes:
    if snake["id"] == curr_snake_id:
      #return snake["head"]["x"], snake["head"]["y"]
      return snake["head"] 
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
  #new_snake_state = new_game_state["board"]["snakes"]
  new_snake_state = new_game_state["snakes"]

  for snake in new_snake_state:
    if snake["id"] == curr_snake_id:
      return curr_snake_index
    curr_snake_index += 1
  return None

def removeKilledSnake(gamestate, snake_index):
  if snake_index == None:
      return
  #if(gamestate["board"]["snakes"] == []):
  if (gamestate["snakes"] == []):
      return
  
  #gamestate["board"]["snakes"].pop(snake_index)
  gamestate["snakes"].pop(snake_index)




def moveForward(game_state,  curr_snake_index, head_x, head_y, eat_food):
  
    #snake = game_state["board"]["snakes"][curr_snake_index]
    snake = game_state["snakes"][curr_snake_index]
    snake["head"] = (head_x, head_y)
    #snake["head"]["x"] = head_x
    #snake["head"]["y"] = head_y

    #snake["body"].insert(0, {"x": head_x, "y": head_y})
    snake["body"].insert(0, (head_x, head_y))

    if not eat_food:
        snake["body"].pop(-1)


# Update snake's health, -1 health for every turn or 0 if snake dies
def updateSnakeHealth(snake, isAlive, hasAte):
    if (hasAte):
        snake["health"] = 100
    elif (isAlive):
        snake["health"] -= 1
    else:
        snake["health"] = 0
    return snake["health"]


      


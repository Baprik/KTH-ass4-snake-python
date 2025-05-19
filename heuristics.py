from utils import flood_fill_area, border_kill
import math
def distance_to_closest_body_part(ourSnake, otherSnake):
  headx, heady = ourSnake["body"][0]
  minDist = 100
  for bodyx, bodyy in otherSnake["body"][0]:
    newDist = math.sqrt((headx-bodyx)**2+(heady-bodyy)**2)
    if newDist < minDist:
      minDist = newDist
  if minDist == 100:
    return 0
  return minDist

def distance_to_border(snake, max_y):
    (x, y) = snake["first_move"]
    max_x = max_y

    #Distances to each border
    distances = [
        x,               
        y,               
        max_x - x,       
        max_y - y        
    ]

    return min(distances)

def evaluatePoint(game_state, depth, curr_snake_id, main_snake_id, current_turn):
  try:
    if game_state == None :
      #print(f"Game state is None, game state: {game_state}")
      return 0
    #if not "snakes" in game_state["board"] :
    if not "snakes" in game_state :

      #print(f"Game state doesn't have 'snakes' field, game state: {game_state}")
      return 0
    #if game_state["board"]["snakes"] == []:
    if game_state["snakes"] == []:
      #print(f"Game state 'snakes' is empty")
      return 0
    
    

    #for i in game_state["board"]["snakes"]:


    main_snake = None
    for snake in game_state["snakes"]:
      if snake["id"] == main_snake_id:
        main_snake = snake
        break
      
    if main_snake == None or border_kill(game_state, main_snake): #So he is dead or it will die
      return float("-inf")
    
    teamMembers = 0
    for snake in game_state["snakes"]:
      if snake["name"] == "MAS2025-12":
        teamMembers += 1

    #snake_length = 0
    #    snake_length += len(snake["body"])  #we don't want to eat though

    otherSnakes = len(game_state["snakes"]) - teamMembers
    head_pos = main_snake["head"]

    area = flood_fill_area(game_state, head_pos)

    for snake in game_state["snakes"]:
      if snake["name"] == "MAS2025-12":
        continue
      #it is going to kill a snake 
      if border_kill(game_state, snake):
        otherSnakes -= 1

    if main_snake["health"] >= 40: #nice idea
      health = 0
    elif main_snake["health"] >= 20:
      health = -100
    else:
      health = -300

    if head_pos[0] <= 1 or head_pos[0] >= game_state["shape"][0] - 2 or head_pos[1] <= 0 or head_pos[1] >= game_state["shape"][1] - 2:
      misposed = -100
    else:
      misposed = 0

    distanceFromBorder = 0
    
    #for snake in game_state["snakes"]:
    if main_snake["first_move"] != None:
      distanceFromBorder += distance_to_border(main_snake, game_state["shape"][1] - 1)
        
    # distanceToLongerSnakesAndTeammate = 0
    # for snake in game_state["snakes"]:
    #   if snake == main_snake:
    #     continue
    #   if snake["name"] == "MAS2025-12" or len(snake["body"]) > len(main_snake["body"]): #want to increase distance to teammate and longer snakes
    #     distanceToLongerSnakesAndTeammate += distance_to_closest_body_part(snake, main_snake)

    return teamMembers * 400  - otherSnakes * 200 + health*2 + distanceFromBorder * 10 + area * 32  + misposed #+ distanceToLongerSnakesAndTeammate     #maybe add distance from eachother


  except KeyError as e:
    print(f"KeyError: {game_state} is empty")
    print(f"KeyError: {e}")
    return float("-inf")
  except Exception as e:
    print(f"KeyError: {game_state} is empty")
    print(f"An error occurred: {e}")
    return float("-inf")
  
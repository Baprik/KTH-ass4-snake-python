from utils import flood_fill_area, border_kill

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
    else:
      health = -100

    if head_pos[0] <= 1 or head_pos[0] >= game_state["shape"][0] - 2 or head_pos[1] <= 0 or head_pos[1] >= game_state["shape"][1] - 2:
      misposed = -100
    else:
      misposed = 0

    return area * 10  + teamMembers * 300  - otherSnakes * 10 + health + misposed #maybe add distance from eachother






  except KeyError as e:
    print(f"KeyError: {game_state} is empty")
    print(f"KeyError: {e}")
    return float("-inf")
  except Exception as e:
    print(f"KeyError: {game_state} is empty")
    print(f"An error occurred: {e}")
    return float("-inf")
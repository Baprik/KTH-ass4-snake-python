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
    for index, snake in enumerate(game_state["snakes"]):
      if snake["id"] == main_snake_id:
        main_snake = snake
        break
      
    if main_snake == None or border_kill(game_state, main_snake): #So he is dead or it will die
      return float("-inf")
    
    snake_length = len(main_snake["body"])

    snakes_alived = len(game_state["snakes"])

    area = flood_fill_area(game_state, main_snake["head"])

    for snake in game_state["snakes"]:
      if snake["id"] == main_snake_id:
        continue
      #it is going to kill a snake 
      if border_kill(game_state, snake):
        snakes_alived -= 1

    return area + snake_length - snakes_alived * 10






  except KeyError as e:
    print(f"KeyError: {game_state} is empty")
    print(f"KeyError: {e}")
    return float("-inf")
  except Exception as e:
    print(f"KeyError: {game_state} is empty")
    print(f"An error occurred: {e}")
    return float("-inf")
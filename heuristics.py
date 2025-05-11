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
    for i in game_state["snakes"]:
      if i["id"] == main_snake_id:
        return len(i["body"])
      
    #So he is dead 
    return float("-inf")
  






  except KeyError as e:
    print(f"KeyError: {game_state} is empty")
    print(f"KeyError: {e}")
    return float("-inf")
  except Exception as e:
    print(f"KeyError: {game_state} is empty")
    print(f"An error occurred: {e}")
    return float("-inf")
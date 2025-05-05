def evaluatePoint(game_state, depth, curr_snake_id, current_turn):
  print("depth:" + str(depth))
  try:
    if game_state["board"]["snakes"] == []:
      print("No snakes left !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      return 0
    for i in game_state["board"]["snakes"]:
      if i["id"] == curr_snake_id:
        return len(i["body"])
    return 0
  except KeyError as e:
    print(f"KeyError: {game_state} is empty")
    print(f"KeyError: {e}")
    return float("-inf")
  except Exception as e:
    print(f"KeyError: {game_state} is empty")
    print(f"An error occurred: {e}")
    return float("-inf")
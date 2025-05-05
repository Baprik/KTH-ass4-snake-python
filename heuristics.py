def evaluatePoint(game_state, depth, curr_snake_id, current_turn):
  print("depth:" + str(depth))
  for i in game_state["board"]["snakes"]:
    if i["id"] == curr_snake_id:
      return len(i["body"])
  return 0
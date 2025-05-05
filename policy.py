import random as rd
from movement import select_safe_move
import copy
import random
from minmax import miniMax_value


def choose_move(safe_moves, game_state, args={"policy": "random"}):
    if args["policy"] == "random":
        return rd.choice(safe_moves)
    elif args["policy"] == "minmax":
        depth = args.get("depth", 3)  # Default depth of 3 if not specified
        return miniMax_value(game_state, safe_moves)

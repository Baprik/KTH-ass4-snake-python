# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import typing
from movement import select_safe_move
from policy import choose_move

#test push

total_time_minimax = 0
step = 0


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Group12",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


def start(game_state: typing.Dict):
    print(game_state)
    print(game_state.keys())
    global total_time_minimax 
    global step
    step = 0
    total_time_minimax = 0
    print("GAME START")


def end(game_state: typing.Dict):
    print("GAME OVER\n")


def move(game_state: typing.Dict) -> typing.Dict:

    safe_moves = select_safe_move(game_state)

    # Are there any safe moves left?

    if len(safe_moves) == 0:
        print(
            f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    #Our policy algorithm
    # next_move = random.choice(safe_moves)

    

    snake_index = 0
    for idx, snake in enumerate(game_state["board"]["snakes"]):
        if snake["id"] == game_state["you"]["id"]:
            snake_index = idx
            #print(snake)
            break

    if snake_index == 0:
        policy = "random"
        print(f"{game_state['you']['id']} : {policy}")
    else:
        policy = "minmax"
        print(f"{game_state['you']['id']} : {policy}")
    args = {"policy": "minmax"}
    

    next_move, others = choose_move(safe_moves, game_state, args)

    #if others["time"] exists
    if "time" in others:
        time = others["time"]
        global total_time_minimax
        global step
        step += 1
        total_time_minimax += time
        print(f"Average Time taken for minimax: {total_time_minimax/step} seconds")


    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    print("Starting Battlesnake Server...")
 
    run_server({"info": info, "start": start, "move": move, "end": end})

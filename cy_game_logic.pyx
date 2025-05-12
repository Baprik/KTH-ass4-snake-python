from libc.stdlib cimport malloc, free
from cython cimport cast
from copy import deepcopy

# Typedef for snake dict
ctypedef dict SnakeDict
ctypedef dict GameStateDict


def createGameState(dict original_game_state, str curr_snake_id):
    cdef list snakes = []
    cdef dict snake_dict
    cdef tuple snake_body

    for snake in original_game_state["board"]["snakes"]:
        snake_body = [(body_part["x"], body_part["y"]) for body_part in snake["body"]]
        snake_dict = {
            "id": snake["id"],
            "body": snake_body,
            "health": snake["health"],
            "head": (snake["head"]["x"], snake["head"]["y"])
        }
        snakes.append(snake_dict)

    return {
        "shape": (original_game_state["board"]["width"], original_game_state["board"]["height"]),
        "food": [(f["x"], f["y"]) for f in original_game_state["board"]["food"]],
        "snakes": snakes,
        "main_snake_id": original_game_state["you"]["id"],
        "curr_snake_id": curr_snake_id
    }


def createNewGameState(dict game_state, str curr_snake_id):
    return {
        "shape": game_state["shape"],
        "food": [(x, y) for x, y in game_state["food"]],
        "snakes": deepcopy(game_state["snakes"]),
        "main_snake_id": game_state["main_snake_id"],
        "curr_snake_id": curr_snake_id
    }


def isGameOver(dict game_state, str snake_id):
    if snake_id is None:
        return False
    if game_state is None:
        return True

    for snake in game_state["snakes"]:
        if snake["id"] == snake_id:
            return False
    return True


def makeMove(dict game_state, str curr_snake_id, str move):
    cdef int board_width, board_height
    board_width, board_height = game_state["shape"]
    cdef dict new_game_state = createNewGameState(game_state, curr_snake_id)
    cdef int head_x, head_y
    head_x, head_y = findHeadCoord(new_game_state, curr_snake_id)

    if head_x is None or head_y is None:
        return None

    head_x, head_y = updateHeadCoord(head_x, head_y, move)
    cdef int curr_snake_index = findCurrentSnake(new_game_state, curr_snake_id)

    if curr_snake_index is None:
        return None

    cdef dict current_snake = new_game_state["snakes"][curr_snake_index]

    if not (0 <= head_x < board_width and 0 <= head_y < board_height):
        removeKilledSnake(new_game_state, curr_snake_index)
        return new_game_state

    cdef bint collide_with_snake = False
    cdef bint collide_with_snake_head = False
    cdef bint collide_with_food = False
    cdef dict potential_snake_collided = None
    cdef int potential_snake_index = 0

    for idx, snake in enumerate(new_game_state["snakes"]):
        if snake["head"] == (head_x, head_y):
            collide_with_snake_head = True
            potential_snake_collided = snake
            potential_snake_index = idx
            break
        for part in snake["body"]:
            if part == (head_x, head_y):
                potential_snake_collided = snake
                collide_with_snake = True
                break

    for food in new_game_state["food"]:
        if food == (head_x, head_y):
            collide_with_food = True
            break

    if collide_with_snake_head:
        dest_len = len(potential_snake_collided["body"])
        curr_len = len(current_snake["body"])
        if dest_len < curr_len:
            removeKilledSnake(new_game_state, potential_snake_index)
            curr_snake_index = findCurrentSnake(new_game_state, curr_snake_id)
            if curr_snake_index is None:
                return None
            moveForward(new_game_state, curr_snake_index, head_x, head_y, False)
            if updateSnakeHealth(current_snake, True, False) <= 0:
                removeKilledSnake(new_game_state, curr_snake_index)
        else:
            removeKilledSnake(new_game_state, curr_snake_index)
            if dest_len == curr_len:
                idx = findCurrentSnake(new_game_state, potential_snake_collided["id"])
                if idx is not None:
                    removeKilledSnake(new_game_state, idx)
        return new_game_state

    elif collide_with_snake:
        removeKilledSnake(new_game_state, curr_snake_index)
        return new_game_state

    elif collide_with_food:
        moveForward(new_game_state, curr_snake_index, head_x, head_y, True)
        updateSnakeHealth(current_snake, True, True)
        return new_game_state

    else:
        moveForward(new_game_state, curr_snake_index, head_x, head_y, False)
        if updateSnakeHealth(current_snake, True, False) <= 0:
            removeKilledSnake(new_game_state, curr_snake_index)
        return new_game_state


def findHeadCoord(dict game_state, str snake_id):
    for snake in game_state["snakes"]:
        if snake["id"] == snake_id:
            return snake["head"]
    return None, None


def updateHeadCoord(int head_x, int head_y, str move):
    if move == "up":
        head_y += 1
    elif move == "down":
        head_y -= 1
    elif move == "left":
        head_x -= 1
    elif move == "right":
        head_x += 1
    return head_x, head_y


def findCurrentSnake(dict game_state, str snake_id):
    cdef int idx = 0
    for snake in game_state["snakes"]:
        if snake["id"] == snake_id:
            return idx
        idx += 1
    return None


def removeKilledSnake(dict game_state, int idx):
    if idx is not None and len(game_state["snakes"]) > 0:
        game_state["snakes"].pop(idx)


def moveForward(dict game_state, int idx, int head_x, int head_y, bint ate_food):
    cdef dict snake = game_state["snakes"][idx]
    snake["head"] = (head_x, head_y)
    snake["body"].insert(0, (head_x, head_y))
    if not ate_food:
        snake["body"].pop(-1)


def updateSnakeHealth(dict snake, bint isAlive, bint hasAte):
    if hasAte:
        snake["health"] = 100
    elif isAlive:
        snake["health"] -= 1
    else:
        snake["health"] = 0
    return snake["health"]
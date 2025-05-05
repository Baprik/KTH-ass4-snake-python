import heapq

def get_occupied_coords(game_state):
    occupied = set()
    for snake in game_state["board"]["snakes"]:
        for segment in snake["body"]:
            occupied.add((segment["x"], segment["y"]))
    return occupied

def get_food_coords(game_state):
    return [(f["x"], f["y"]) for f in game_state["board"]["food"]]

def in_bounds(x, y, width, height):
    return 0 <= x < width and 0 <= y < height

def neighbors(x, y, width, height):
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    return [(x+dx, y+dy) for dx, dy in directions if in_bounds(x+dx, y+dy, width, height)]

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, game_state, occupied):
    width = game_state["board"]["width"]
    height = game_state["board"]["height"]
    
    open_set = []
    heapq.heappush(open_set, (0 + manhattan(start, goal), 0, start, []))
    visited = set()

    while open_set:
        est_total_cost, cost_so_far, current, path = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path + [current]  # path includes goal

        for nx, ny in neighbors(current[0], current[1], width, height):
            if (nx, ny) not in occupied and (nx, ny) not in visited:
                heapq.heappush(open_set, (
                    cost_so_far + 1 + manhattan((nx, ny), goal),
                    cost_so_far + 1,
                    (nx, ny),
                    path + [current]
                ))
    return None  # No path found

# MAIN PROCESS
def find_path_to_closest_food(game_state, curr_snake_id):
    # Find my snake
    my_snake = None
    for s in game_state["board"]["snakes"]:
        if s["id"] == curr_snake_id:
            my_snake = s
            break

    if not my_snake:
        raise ValueError("Current snake not found")

    start = (my_snake["head"]["x"], my_snake["head"]["y"])
    occupied = get_occupied_coords(game_state)
    food_list = get_food_coords(game_state)

    if not food_list:
        return None

    # Find closest food
    food_list.sort(key=lambda f: manhattan(start, f))
    for food in food_list:
        path = a_star(start, food, game_state, occupied)
        if path:
            return path  # Return first found path to nearest food

    return None  # No path found to any food

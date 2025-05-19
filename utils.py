from collections import deque


def flood_fill_area(game_state, start_pos, max_steps = 7):
    width, height = game_state["shape"]
    snakes = game_state["snakes"]

    # Build set of all occupied cells (by any snake)
    occupied = set()
    for snake in snakes:
        occupied.update(snake["body"])

    visited = set()
    queue = deque([(start_pos, 0)])  # Include step count
    visited.add(start_pos)

    while queue:
        (x, y), steps = queue.popleft()

        # Stop exploring paths that exceed the step threshold
        if steps >= max_steps:
            continue

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)

            if not (0 <= nx < width and 0 <= ny < height):
                continue

            if neighbor in visited or neighbor in occupied:
                continue

            visited.add(neighbor)
            queue.append((neighbor, steps + 1))

    return len(visited)



def is_on_the_border(game_state, pos):
    width, height = game_state["shape"]
    x, y = pos
    return x == 0 or x == width - 1 or y == 0 or y == height - 1

def border_kill(game_state, snake):
    snake_head = snake["head"]
    snake_dir = (
        snake["body"][0][0] - snake["body"][1][0],
        snake["body"][0][1] - snake["body"][1][1]
    )
    width, height = game_state["shape"]

    if not is_on_the_border(game_state, snake_head):
        return False

    for s in game_state["snakes"]:
        if s["id"] == snake["id"]:
            continue

        enemy_head = s["head"]
        dx = abs(enemy_head[0] - snake_head[0])
        dy = abs(enemy_head[1] - snake_head[1])

        # Check if enemy head is adjacent 
        if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
            enemy_dir = (
                s["body"][0][0] - s["body"][1][0],
                s["body"][0][1] - s["body"][1][1]
            )

            # Same direction
            if enemy_dir == snake_dir:
                # Check which snake is ahead
                delta = (snake_head[0] - enemy_head[0], snake_head[1] - enemy_head[1])
                advance_scalar = snake_dir[0] * delta[0] + snake_dir[1] * delta[1]

                # If the enemy is chasing from behind
                if advance_scalar > 0:
                    # If they are same direction and enemy is longer -> border kill
                    if len(s["body"]) > len(snake["body"]):
                        return True
                else:
                    return True 

    return False

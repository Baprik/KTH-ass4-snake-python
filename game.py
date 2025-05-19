from gameLogic import makeMove
import random
import time
from agents import BotAgent
class Game2V2:
    def __init__(self, bot_disabled=False):
        self.bot_disabled = bot_disabled
        self.reset()

    def reset(self):
        # Initialize positions, health, etc.
        start_positions = [(1, 5), (5, 1), (5, 9), (9, 5)]
        random.shuffle(start_positions)
        self.agent_team = ["1", "2"]
        self.old_health = {"1": 100, "2": 100}
        if self.bot_disabled:
            self.bot_team = []
        else:
            self.bot_team = ["3", "4"]
        self.shape = (11, 11)
        if self.bot_disabled:
            snakes  = [
                {"id": "1", "health": 100, "head": start_positions[0], "name": "agent1", "body": [start_positions[0],start_positions[0],start_positions[0]]},
                {"id": "2", "health": 100, "head": start_positions[1], "name": "agent2", "body": [start_positions[1],start_positions[1],start_positions[1]]}
            ]
        else:
            snakes = [
                {"id": "1", "health": 100, "head": start_positions[0], "name": "agent1", "body": [start_positions[0],start_positions[0],start_positions[0]]},
                {"id": "2", "health": 100, "head": start_positions[1], "name": "agent2", "body": [start_positions[1],start_positions[1],start_positions[1]]},
                {"id": "3", "health": 100, "head": start_positions[2], "name": "bot1", "body": [start_positions[2],start_positions[2],start_positions[2]]},
                {"id": "4", "health": 100, "head": start_positions[3], "name": "bot2", "body": [start_positions[3],start_positions[3],start_positions[3]]}
            ]
        self.game_state = {
            "shape": (11, 11),
            "food": [],
            "main_snake_id": self.agent_team,
            "curr_snake_id": self.agent_team[0],
            "snakes": snakes, 

        }
        self.done = False

        ## For reward ##
        self.turn = 0
        self.agent_just_died = False
        self.ennemy_just_died = False

        ## Game init ##

        self.place_food_randomly(5 )

        return self.get_observation()
    def convert_action_to_move(self,action):
        # Convert action to move
        if action == 0:
            return "up"
        elif action == 1:
            return "down"
        elif action == 2:
            return "left"
        elif action == 3:
            return "right"
        else:
            raise ValueError("Invalid action")
        
    def is_alive(self, agent_id):
        # Check if the agent is alive
        for agent in self.game_state["snakes"]:
            if agent["id"] == agent_id:
                return agent["health"] > 0
        return False
        
    def step(self, agent_actions, bot_actions):
        self.old_health = {
            agent_id: self.get_snake(agent_id)["health"] if self.get_snake(agent_id) is not None else 0
            for agent_id in self.agent_team
        }
        # Apply actions to the environment
        for i, action in enumerate(agent_actions):
            agent_id = self.agent_team[i]
            if self.is_alive(agent_id):
                move = self.convert_action_to_move(action)
                self.game_state = makeMove(self.game_state, agent_id, move)
        for i, action in enumerate(bot_actions):
            bot_id = self.bot_team[i]
            if self.is_alive(bot_id):
                move = self.convert_action_to_move(action)
                self.game_state = makeMove(self.game_state, bot_id, move)
        

        self.simulate_food()
        self.turn += 1
        
        # Check game over condition
        self.done = self.check_done()
        reward = self.compute_reward()
        obs = self.get_observation()
        return obs, reward, self.done


    def get_observation(self):
        # Return a representation of the state for the agent
        return self.game_state
    
    def get_snake(self, snake_id):
        # Get the snake object by ID
        for snake in self.game_state["snakes"]:
            if snake["id"] == snake_id:
                return snake
        return None
    
    def get_snake_length(self, snake_id):
        # Get the length of the snake
        snake = self.get_snake(snake_id)
        if snake:
            return len(snake["body"])
        return 0

    def compute_reward(self):
        turn = self.turn
        reward  = 0
        agent_alive  = sum(1 for agent_id in self.agent_team if self.is_alive(agent_id))
        ennemy_alive = sum(1 for bot_id in self.bot_team if self.is_alive(bot_id))
        if agent_alive == 0 and not self.agent_just_died:
            #both died at the same time
            reward +=  -75
        if agent_alive == 0 and self.agent_just_died:
            #last agent died
            reward += -50
        if not self.agent_just_died and agent_alive == 1:
            #one agent died
            self.agent_just_died = True
            reward += -25
        
        if ennemy_alive == 0:
            # ennemy team is dead
            if not self.ennemy_just_died:
                reward += 75
            else:
                reward += 50
        if ennemy_alive == 1 and not self.ennemy_just_died:
            self.ennemy_just_died = True 
            # ennemy team is dead
            reward += 25

        for agent_id in self.agent_team:
            if self.is_alive(agent_id):
                snake = self.get_snake(agent_id)
                if self.old_health[agent_id] < 20:
                    if snake["health"] > 20:
                        # Snake is in critical condition
                        reward += 5
                    else:
                        # Snake is in critical condition and lost health
                        #reward -= 2
                        min_dist = min(min(manhattan(snake["head"], food) for food in self.game_state["food"]),10)
                        reward -= 0.4 * min_dist
                elif self.old_health[agent_id] < 50:
                    if snake["health"] > 50:
                        # Snake is in critical condition
                        reward += 2
                    else:
                        # Snake is in critical condition and lost health
                        #reward -= 1
                        min_dist = min(min(manhattan(snake["head"], food) for food in self.game_state["food"]),10)
                        reward -= 0.2 * min_dist
        #reward += agent_alive 
        reward += (2+ agent_alive - ennemy_alive) * (1 + self.turn / 100)

        return reward
    
    def check_done(self):
        # Check if any team is fully defeated
        agent_dead = all(not self.is_alive(agent_id) for agent_id in self.agent_team)
        bot_dead = all(not self.is_alive(bot_id) for bot_id in self.bot_team)
        return agent_dead or (bot_dead and not self.bot_disabled) # or self.turn >= 50

    def is_valid_position(self, x, y):
            for snake in self.game_state["snakes"]:
                for body_part in snake["body"]:
                    if body_part == (x, y):
                        return False
            return 0 <= x < self.shape[0] and 0 <= y < self.shape[1] and (x, y) not in self.game_state["food"] 
    


    def check_food_needing_placement(self, settings, state):
        min_food = 1
        food_spawn_chance = 15
        num_current_food = len(state['food'])

        if num_current_food < min_food:
            return min_food - num_current_food
        if food_spawn_chance > 0 and (100 - random.randint(0, 99)) < food_spawn_chance:
            return 1

        return 0

    def place_food_randomly(self, n):
        for _ in range(n):
            pos = (random.randint(0, self.shape[0] - 1), random.randint(0, self.shape[1] - 1))
            while not self.is_valid_position(pos[0], pos[1]):
                pos = (random.randint(0, self.shape[0] - 1), random.randint(0, self.shape[1] - 1))
            self.add_food(pos)


    def simulate_food(self):
        settings = {'minimumFood': 1, 'foodSpawnChance': 15}
        n = self.check_food_needing_placement(settings, self.game_state)
        self.place_food_randomly( n)

    def add_food(self, position):
        self.game_state["food"].append(position)


    def display(self):
        # Display the board with x-axis to the right and y-axis upwards
        board = [[" . " for _ in range(self.shape[1])] for _ in range(self.shape[0])]
        
        # Place snakes
        for snake in self.game_state["snakes"]:
            for x, y in snake["body"]:
                board[y][x] = " x " if snake["id"] in self.agent_team else " o "
            head_x, head_y = snake["head"]
            board[head_y][head_x] = f" {snake['id']} "
        
        # Place food
        for x, y in self.game_state["food"]:
            board[y][x] = " F "
        
        # Print from top (high y) to bottom (low y)
        for y in reversed(range(self.shape[1])):
            row = "".join(board[y])
            print(f"{y:2}|{row}")
        
        # Print x-axis labels
        x_labels = "   " + "".join([f"{x:3}" for x in range(self.shape[0])])
        print(x_labels)
        print("\n")

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

if __name__ == "__main__":
    game = Game2V2(True)
    game.reset()
    print("Initial Game State:")
    game.display()
    bots = BotAgent(True,  game.bot_team)
    agents = BotAgent( False, game.agent_team)

    while not game.done:
        a = random.randint(0, 3)
        b = random.randint(0, 3)
        #b = int(input("Enter action for agent 1 (0: up, 1: down, 2: left, 3: right): "))
        agent_actions = [a,b]
        agent_actions = agents.act(game.game_state)
        bot_actions = bots.act(game.game_state)
        obs, reward, done = game.step(agent_actions, bot_actions)
        
        print(f"Agent Actions: {agent_actions}, Bot Actions: {bot_actions}")
        game.display()
        print(game.game_state)
        
        print(f"Reward: {reward}, Done: {done}")
        time.sleep(0.05)
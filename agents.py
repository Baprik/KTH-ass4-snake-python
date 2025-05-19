from movement2 import select_safe_move
import numpy as np

class BotAgent():
    def __init__(self,bot_disabled = False, ids = ["3", "4"]):
        self.bot_disabled = bot_disabled
        self.bot_id = ids 
        pass

    def act(self, state):
        # Implement your bot's action logic here
        # For now, return a random action
        if self.bot_disabled:
            return []
        bots_actions = []
        for id in self.bot_id:

            moves = select_safe_move(state, id)
            if len(moves) == 0:
                bots_actions.append(0)  # No safe moves, default action
            else:
                move = np.random.choice(moves)
                bots_actions.append(self.move_to_action(move))
        
        return bots_actions  # Example: 0=up, 1=down, 2=left, 3=right
    
    def move_to_action(self, move):
        if move == "up":
            return 0
        elif move == "down":
            return 1
        elif move == "left":
            return 2
        elif move == "right":
            return 3
        else:
            raise ValueError("Invalid move")
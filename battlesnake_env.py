import gym
from gym import spaces
import numpy as np
from game import Game2V2
from agents import BotAgent

class TwoVTwoEnv(gym.Env):
    def __init__(self, bot_disabled=False):
        super(TwoVTwoEnv, self).__init__()
        self.bot_disabled = bot_disabled
        self.game = Game2V2(bot_disabled)
        self.bot = BotAgent(bot_disabled)
        
        #self.action_space = spaces.MultiDiscrete([4, 4])
        self.action_space = spaces.Discrete(16)  # 4*4 joint actions
        
        # Example observation space: flat vector of HP and positions
        self.observation_space = spaces.Box(low=0, high=1, shape=(5, 11, 11), dtype=np.float32)


    def reset(self):
        obs = self.game.reset()
        return self._format_obs(obs)

    def step(self, action):
        a1 = action // 4
        a2 = action % 4
        bot_actions = self.bot.act(self.game.game_state)
        actions = [a1, a2]
        obs, reward, done = self.game.step(actions, bot_actions)
        return self._format_obs(obs), reward, done, {}

    def _format_obs(self, obs):
        # Flatten state into a vector (adjust as needed)
        state = np.zeros((11, 11, 5), dtype=np.float32)
        for snake in obs["snakes"]:
            x, y = snake["head"]
            z = int(snake["id"])
            if snake["health"] < 20:
                state[x, y, z] = 0.66
            elif snake["health"] < 50:
                state[x, y, z] = 0.82
            else:
                state[x, y, z] = 1.0
            for part in snake["body"]:
                if part == snake["head"]:
                    continue
                x, y = part
                state[x, y, z] = 0.5
        for food in obs["food"]:
            x, y = food
            state[x, y, 0] = 1
        return np.transpose(state, (2, 0, 1))


from stable_baselines3.common.callbacks import BaseCallback

class DisplayCallback(BaseCallback):
    def __init__(self, env, display_interval=10000, verbose=1):
        super(DisplayCallback, self).__init__(verbose)
        self.env = env
        self.display_interval = display_interval

    def _on_step(self) -> bool:
        if self.num_timesteps % self.display_interval == 0:
            print(f"Step {self.num_timesteps}: Displaying a full game episode")
            obs = self.env.reset()
            done = False
            turn = 0
            while not done:
                action, _ = self.model.predict(obs, deterministic=True)
                obs, reward, done, info = self.env.step(action)
                self.env.game.display()  # Show each step/frame
                turn += 1
                print(f"Turn {turn}: Action {action}, Reward {reward}")
            print(f"Episode finished. Total turns: {turn}")
        return True

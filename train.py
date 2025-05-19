from stable_baselines3 import DQN
from battlesnake_env import TwoVTwoEnv, DisplayCallback
from CNN import SmallGridCNN  # Your CNN

# Training for agent 1
env = TwoVTwoEnv(bot_disabled=False)


display_callback = DisplayCallback(env, display_interval=10_000)

policy_kwargs = dict(
    features_extractor_class=SmallGridCNN,
    features_extractor_kwargs=dict(features_dim=128),
)
# if dqn model already exists, load it
#check if the model exists 
import os
if os.path.exists("dqn.zip"):
    print("Model exists, loading...")
    model = DQN.load("dqn", env=env, policy_kwargs=policy_kwargs)
    model.verbose = 0
    model.tensorboard_log = "./logsDQNbots/"
    model.device = "cpu"
    print("Model loaded successfully.")
else:
    print("Model does not exist, creating a new one...")
    model = DQN(
        "CnnPolicy",
        env,
        policy_kwargs=policy_kwargs,
        verbose=0,
        tensorboard_log="./logsDQNbots/",
        device="cpu"
    )
    print("Model created successfully.")

try:
    model.learn(total_timesteps=500_000, callback=display_callback)
except KeyboardInterrupt:
    print("Training interrupted, saving model.")
    model.save("dqn")

model.save("dqn")

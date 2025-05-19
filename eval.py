from stable_baselines3 import DQN
from battlesnake_env import TwoVTwoEnv
from CNN import SmallGridCNN  # your custom CNN

# --- Setup Environment (same as training, no display callback needed) ---
env = TwoVTwoEnv(bot_disabled=False)  # use same init args as during training


# --- Load Trained Model ---
model = DQN.load("dqn_learn_solo", env=env, policy_kwargs=dict(
    features_extractor_class=SmallGridCNN,
    features_extractor_kwargs=dict(features_dim=128),
))
success_rate = 0.0
simulation_count = 1
# --- Reset Env and Start Simulation ---
for _ in range(simulation_count):
    obs = env.reset()
    done = False
    total_reward = 0
    step_count = 0

    while not done:
        action, _states = model.predict(obs, deterministic=True)  # No exploration
        obs, reward, done, info = env.step(action)
        
        total_reward += reward
        step_count += 1
        env.game.display()  # Display the game state (optional, for debugging)
        
        

        # Print useful info (optional)
        print(f"Step {step_count}: Reward {reward}, Done {done}")
        print(f"Old Health: {env.game.old_health}")
        if done:
            if step_count > 49:
                success_rate += 1/simulation_count


# --- Done ---
print(f"\n🎮 Simulation Finished in {step_count} steps. Total reward: {total_reward}")
print(f"Success Rate: {success_rate * 100:.2f}%")

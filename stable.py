import gymnasium as gym
import dcss_examples
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import os
import time
import sys
sys.path.append("logs/")
import process
# Parallel environments
iterations = 30
replace_frame = 5
vec_env = make_vec_env("dcss_examples/Inventory-v0", n_envs=1, env_kwargs={"render_mode": "None", "verbose_output": "False", "max_iterations":iterations, "replace_frame":replace_frame})
if os.path.isfile('logs/terminated_logs.txt'):
    os.remove('logs/terminated_logs.txt')
if os.path.isfile('logs/inventory_check.txt'):
    os.remove('logs/inventory_check.txt')
model = PPO("MultiInputPolicy", vec_env, verbose=1, device="cpu")
model.load("dcss_inventory_bot")
model.learn(total_timesteps=2048)


obs = vec_env.reset()
vec_env.env_method("toggle_verbose_output")
print("Starting records:")

"""
TODO:
Visualize rewards over the multiple sessions
"""
for i in range(iterations*10+1): #Get ten example results
    action, _states = model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)

model.save("dcss_inventory_bot")

processor = process.Processor("logs/")
processor.set_up_lists()
processor.plot_all()

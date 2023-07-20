import gymnasium as gym
import dcss_examples
from stable_baselines3 import PPO
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
import os
import time
import sys
sys.path.append("logs/")
import process

if len(sys.argv) > 1:
    iterations = int(sys.argv[1])
else:
    iterations = 30

if len(sys.argv) > 2:
    replace_frame = int(sys.argv[2])
else:
    replace_frame = 5

if len(sys.argv) > 3:
    sessions = int(sys.argv[3])
else:
    sessions = 10

if len(sys.argv) > 4:
    num_envs = int(sys.argv[4])
else:
    num_envs = 1

#Make the environment and pass in the iterations and replace_frame
vec_env = make_vec_env("dcss_examples/Inventory-v0", n_envs=num_envs, env_kwargs={"render_mode": "None", "verbose_output": "False", "max_iterations":iterations, "replace_frame":replace_frame})
#Remove logs from previous session.
"""
TODO:
    Expand this to include the pngs created by logs/process.py
"""
if os.path.isfile('logs/terminated_logs.txt'):
    os.remove('logs/terminated_logs.txt')
if os.path.isfile('logs/inventory_check.txt'):
    os.remove('logs/inventory_check.txt')
    
#Cpu is faster for me for some reason - cuda is very slow
#model = PPO("MultiInputPolicy", vec_env, verbose=0, device="cpu")
model = DQN("MultiInputPolicy", vec_env, verbose = 0, device="cpu")
#If we have a model already, load it
if os.path.isfile('dcss_inventory_bot_PPO.zip'):
    print("Loading Model")
    model.load("dcss_inventory_bot_PPO")
elif os.path.isfile('dcss_inventory_bot_DQN.zip'):
    print("Loading Model")
    model.load("dcss_inventory_bot_DQN")

#After every session, save the model
for i in range(sessions):
    model.learn(total_timesteps=2048 * num_envs)
    #model.save("dcss_inventory_bot_PPO")
    model.save("dcss_inventory_bot_DQN")
    print("Session ", i+1, " done.\n Saved.\n")
obs = vec_env.reset()
vec_env.env_method("toggle_verbose_output")
print("Done with all sessions.\nStarting records:")



mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)

print("Mean_reward: ", mean_reward)
print("std_reward: ", std_reward)
for i in range(iterations*10+1): #Get ten example results
    action, _states = model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)

#Instantiate and process the logs we just created
processor = process.Processor("logs/")
processor.plot_all()

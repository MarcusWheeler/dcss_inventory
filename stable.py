import gymnasium as gym
import dcss_examples
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import time
# Parallel environments
vec_env = make_vec_env("dcss_examples/Inventory-v0", n_envs=4, env_kwargs={"render_mode": "None", "verbose_output": "False"})

model = PPO("MultiInputPolicy", vec_env, verbose=1, device="cpu")
model.learn(total_timesteps=10000)
#model.save("ppo_cartpole")

#del model # remove to demonstrate saving and loading

#model = PPO.load("ppo_cartpole")

obs = vec_env.reset()
vec_env.env_method("toggle_verbose_output")
print("Should be toggled")

for i in range(1001):#10000 iterations
    action, _states = model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)
    
    print(i)
    #vec_env.env_method("print_current_stats")
    #if rewards > 20:
    
    #time.sleep(1)
    #vec_env.render(None)

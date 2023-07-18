from gymnasium.envs.registration import register
register(
     id="dcss_examples/Inventory-v0",
     entry_point="dcss_examples.envs:InventoryEnv",
     max_episode_steps=1100,
)

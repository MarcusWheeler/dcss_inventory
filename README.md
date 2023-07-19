# dcss_inventory
usage
python3 stable.py [iterations per session] [frame to replace items on] [# sessions]

Structure:
dcss-examples
    |stable.py
    |setup.py
    logs
        |process.py
    dcss_examples
        |__init__.py
        envs
            |__init__.py
            |inventory.py
            |item.py

inventory.py contains the custom environment for gymnasium

item.py is a helper class that represents the items used in the env

both __init__.py files and the setup.py file is for gymnasium and registering the
custom environment

stable.py is the driver - it utilizes stable baselines3 for the algorithms
and gymnasium for the environment.

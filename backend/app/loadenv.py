import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()

    env_vars = os.environ

    return dict(env_vars)
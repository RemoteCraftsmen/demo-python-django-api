"""
Settings for env file
"""
import os

import environ

from .base_dir import BASE_DIR
env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

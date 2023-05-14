import os

from .error_checking import check

_API_KEY = None

def _init_api_key():
    env_var_name = 'NUTRINAUT_API_KEY'

    if env_var_name in os.environ:
        global _API_KEY
        _API_KEY = os.environ[env_var_name]

def set_api_key(api_key):
    check(isinstance(api_key, str), TypeError,
        f"expected 'api_key' of type str, but got {type(api_key)}")
    global _API_KEY
    _API_KEY = api_key

def get_api_key():
    return _API_KEY


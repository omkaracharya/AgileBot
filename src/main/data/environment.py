# Interacts with the environment variables.

import os

def set_env():
    filepath = (os.path.dirname(os.path.abspath(__file__ + "../../../../"))
                + '/environment_variables.txt')
    variables = dict(line.strip().split('=') for line in open(filepath))
    for k, v in variables.items():
        set_var(k, v)


def set_var(key, value):
    os.environ.setdefault(key, value)


def get_env(variable):
    return os.environ.get(variable)

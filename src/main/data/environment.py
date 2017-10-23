import os

def set_env(filepath='../../../environment_variables.txt'):
    variables = dict(line.strip().split('=') for line in open(filepath))
    for k, v in variables.items():
        os.environ.setdefault(k, v)


def get_env(variable):
    return os.environ.get(variable)

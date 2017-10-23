import os

def set_env():
    variables = dict(line.strip().split('=') for line in open('../../../environment_variables.txt'))
    for k, v in variables.items():
        os.environ.setdefault(k, v)


def get_env(variable):
    return os.environ.get(variable)

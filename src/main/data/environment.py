import os

variables = dict(line.strip().split('=') for line in open('../../../environment_variables.txt'))


def set_env():
    for k, v in variables.items():
        os.environ.setdefault(k, v)


def get_env(variable):
    return os.environ.get(variable)

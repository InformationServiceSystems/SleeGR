from functools import wraps


def check_json(f):
    def d(*args, **kwargs):
        f(*args)
    return d



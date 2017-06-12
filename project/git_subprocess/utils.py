import os


def silence(method, *args, **kwargs):
    # with open(os.devnull, 'w') as f:
    #     kwargs['stdout'] = f
        print args, kwargs
        return method(*args, **kwargs)
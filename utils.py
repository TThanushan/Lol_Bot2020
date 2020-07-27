"""Utilities functions"""
import time
import random

def sleep(nb_secs=random.uniform(0.005, 0.1)):
    """Pause the program for a duration"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            time.sleep(nb_secs)
            func(*args, **kwargs)
        return wrapper
    return decorator

def check_exec_time():
    """Return the execution time of a function"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            time_before = time.time()
            ret = func(*args, **kwargs)
            time_after = time.time()
            exec_time = time_after - time_before
            print("Function {0} tooks {1} to execute.".format(func, exec_time))
            return ret
        return wrapper
    return decorator
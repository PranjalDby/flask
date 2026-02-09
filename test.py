import functools
def decorate_me(func):
    @functools.wraps(func)
    def inner_wrapper(*args,**kwds):
        print('Applied decorator function on = ',func.__name__)
        res = func(*args,**kwds)
        print(f'________- res - _____________\n')
        return res
        
    return inner_wrapper


@decorate_me
def add(num1,num2):
    return num1 + num2


plus_two = add
print(plus_two(20,30))
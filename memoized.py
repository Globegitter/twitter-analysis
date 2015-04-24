import collections
import functools


'''
Decorator. Caches a function's return value each time it is called.
If called later with the same arguments, the cached value is returned
(not reevaluated).
'''


class memoized(object):

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    '''Return the function's docstring.'''
    def __repr__(self):
        return self.func.__doc__

    '''Support instance methods.'''
    def __get__(self, obj, objtype):
        return functools.partial(self.__call__, obj)
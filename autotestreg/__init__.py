"""
Automatically test your functions to see if you have changed their behavior by mistake!
"""

# from sys import modules
# from types import ModuleType
from autotestreg.autotest import autotest_func, autotest_module, set_interactive

__all__ = ["autotest_func", "autotest_module", "set_interactive"]


# class CallableModule(ModuleType):
#     """Inspired from https://stackoverflow.com/a/74604283"""
#     def __init__(self):
#         ModuleType.__init__(self, __name__)
#         self.__dict__.update(modules[__name__].__dict__)
#
#     def __call__(self, *args, **kwargs):
#         searchin(*args, **kwargs)
#
#     mod_call= __call__
#     __all__= list(set(vars().keys()) - {'__qualname__'})
#
# modules[__name__]= CallableModule()

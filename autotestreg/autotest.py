from dataclasses import dataclass
import inspect
import os
import pickle
from typing import Callable, List, Any
from types import ModuleType
import difflib
import sys


@dataclass
class Hash:
    hash: int

    def __repr__(self):
        return str(self.hash)


def hash_if_possible(obj: Any) -> Any:
    """
    Try to hash an object if it is hashable.
    If it's not, return the object as is.
    """
    try:
        return Hash(hash(obj))
    except TypeError:
        return obj


def is_equal(obj1: Any, obj2: Any) -> bool:
    """
    Check if two objects are equal.
    """
    if isinstance(obj1, Hash) and isinstance(obj2, Hash):
        return obj1.hash == obj2.hash
    return obj1 == obj2


def index_in_list(list_: List, item: Any) -> int:
    """
    Return the index of an item in a list.
    :param list_: the list to search
    :param item: the item to search for
    :return: the index of the item
    """
    for i, x in enumerate(list_):
        if is_equal(x, item):
            return i
    return -1


def autotest_func(func: Callable, autotest_path: str = "autotestreg_data/") -> Callable:
    """
    Replace the function with a wrapper than runs the function but
    records the output and compares it to previously computed output.
    :param func: the function to wrap
    :param autotest_path: the path to store the output
    :return: the wrapped function
    """
    if hasattr(func, "__autotest__"):
        return func

    # noinspection PyUnresolvedReferences
    def wrapper(*args, **kwargs):
        """
        The wrapper function.
        :param args: the arguments to the function
        :param kwargs: the keyword arguments to the function
        :return: the result of the function
        """
        inputs = (args, kwargs)
        outputs = func(*args, **kwargs)

        # This saves ressources but makes the errors messages less readable
        # inputs = hash_if_possible(inputs)
        # outputs = hash_if_possible(outputs)

        file_path = os.path.join(autotest_path, *func.__module__.split("."), func.__name__ + ".pkl")

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                all_inputs, all_outputs = pickle.load(f)
                index = index_in_list(all_inputs, inputs)
                if index >= 0:
                    old_output = all_outputs[index]
                    if is_equal(old_output, outputs):
                        return outputs
                    else:
                        diff_results = difflib.unified_diff(
                            str(old_output).splitlines(keepends=True), str(outputs).splitlines(keepends=True)
                        )
                        sys.stderr.write("".join(diff_results))
                        # fail the test
                        raise AssertionError("Output changed in " + func.__module__ + "/" + func.__name__)
        else:
            all_inputs = []
            all_outputs = []
        # in any other case, save the new output
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        all_inputs.append(inputs)
        all_outputs.append(outputs)
        with open(file_path, "wb") as f:
            pickle.dump((all_inputs, all_outputs), f)

        return outputs

    # add a custom attribute to the wrapper so that it can be identified as an autotest function
    wrapper.__autotest__ = True
    return wrapper


def autotest_module(module: ModuleType):
    """
    Replace all functions in a module with autotest versions.
    :param module: the module to wrap
    :return: the wrapped module
    """
    for name, obj in module.__dict__.items():
        if inspect.isfunction(obj) and not hasattr(obj, "__autotest__") and obj.__module__ == module.__name__:
            setattr(module, name, autotest_func(obj))
        elif isinstance(obj, ModuleType):
            autotest_module(obj)
        elif inspect.isclass(obj) and obj.__module__ == module.__name__:
            for method_name, m_obj in obj.__dict__.items():
                if (
                    inspect.isfunction(m_obj)
                    and not hasattr(m_obj, "__autotest__")
                    and m_obj.__module__ == module.__name__
                ):
                    setattr(obj, method_name, autotest_func(m_obj))

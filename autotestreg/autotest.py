import argparse
import ast
import difflib
import hashlib
import inspect
import os
import pickle
import shutil
import sys
from types import ModuleType
from typing import Any, Callable, List, Optional

# Prefer dill for robust serialization of arbitrary objects
try:
    import dill as _serializer

    _SERIALIZER_NAME = "dill"
except Exception:
    _serializer = pickle
    _SERIALIZER_NAME = "pickle"


def _serializer_load(f):
    """Load using chosen serializer, falling back to pickle if necessary."""
    try:
        return _serializer.load(f)
    except Exception:
        # fallback to stdlib pickle
        f.seek(0)
        return pickle.load(f)


def _serializer_dump(obj, f):
    """Dump using chosen serializer, raise on failure to allow fallback handling."""
    try:
        return _serializer.dump(obj, f)
    except Exception:
        # re-raise for caller to handle
        raise


INTERACTIVE = True

# Global dictionary to track user decisions about code changes per function
# Key: (module_name, function_name, old_code_hash, new_code_hash)
# Value: bool (True if user accepted the change, False if rejected)
_CODE_CHANGE_DECISIONS = {}


def _deterministic_hash(text: str) -> int:
    """
    Create a deterministic hash that is stable across Python sessions.
    Uses SHA-256 to create a consistent hash value.
    :param text: the text to hash
    :return: a deterministic integer hash
    """
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16) % (2**63)


def _normalize_code_for_hashing(source_code: str) -> str:
    """
    Normalize source code by removing comments and docstrings for hash comparison.
    This allows ignoring docstring/comment-only changes.
    :param source_code: the original source code
    :return: normalized source code without comments and docstrings
    """
    try:
        # Parse the source code into an AST
        tree = ast.parse(source_code)

        # Remove docstrings (first string literal in functions, classes, modules)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                # Remove docstring if present (first statement is a string)
                if (
                    node.body
                    and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)
                ):
                    node.body = node.body[1:]
            elif isinstance(node, ast.Module):
                # Remove module-level docstring
                if (
                    node.body
                    and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)
                ):
                    node.body = node.body[1:]

        # Convert back to source code using ast.unparse (Python 3.9+)
        try:
            # Python 3.9+
            normalized = ast.unparse(tree)
            return normalized
        except AttributeError:
            # Fallback for older Python versions
            return _normalize_code_simple_fallback(source_code)

    except Exception:
        # If AST parsing fails, fall back to simple comment removal
        return _normalize_code_simple_fallback(source_code)


def _normalize_code_simple_fallback(source_code: str) -> str:
    """
    Simple string-based normalization as fallback.
    """
    lines = source_code.split("\n")
    normalized_lines = []
    in_triple_quote = False
    quote_type = None

    for line in lines:
        stripped = line.strip()

        # Skip empty lines and obvious comments
        if not stripped or stripped.startswith("#"):
            continue

        # Basic handling of triple-quoted strings (docstrings)
        if '"""' in line or "'''" in line:
            if not in_triple_quote:
                # Check if this starts a docstring
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    quote_type = '"""' if '"""' in line else "'''"
                    if line.count(quote_type) == 1:  # Opening triple quote
                        in_triple_quote = True
                        continue
                    # else: single-line triple quote, skip it
                    continue
            else:
                # We're in a triple quote, check if it closes
                if quote_type and quote_type in line:
                    in_triple_quote = False
                    quote_type = None
                continue

        if in_triple_quote:
            continue

        # Remove inline comments (basic approach)
        if "#" in line:
            # Simple heuristic: remove # and everything after if not in quotes
            quote_count = line.count('"') + line.count("'")
            if quote_count % 2 == 0:  # Even number of quotes, likely not inside string
                comment_pos = line.find("#")
                if comment_pos >= 0:
                    line = line[:comment_pos].rstrip()

        if line.strip():
            normalized_lines.append(line)

    return "\n".join(normalized_lines)


def set_interactive(interactive: bool = True) -> None:
    """
    Set the interactive mode.
    :param interactive: whether to run in interactive mode
    """
    global INTERACTIVE
    INTERACTIVE = interactive


class Hash:
    def __init__(self, hash: int) -> None:
        self.hash = hash

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


class FunctionAutoTest:
    def __init__(
        self, all_inputs: List[Any], all_outputs: List[Any], code_hash: int
    ) -> None:
        self.all_inputs = all_inputs
        self.all_outputs = all_outputs
        self.code_hash = code_hash


def _ask_user_about_code_change(func_module: str, func_name: str) -> bool:
    """
    Ask the user if they want to accept a code change.
    :param func_module: the module name
    :param func_name: the function name
    :return: True if user accepts the change (logic changed), False otherwise
    """
    if not INTERACTIVE:
        return False

    answer = ""
    while answer not in {"y", "n"}:
        answer = input(
            "Function code changed in "
            + func_module
            + "/"
            + func_name
            + ". Has function logic changed? [y/n] "
        ).lower()
    return answer == "y"


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

    # Precompute code source and hash once when wrapping the function.
    # These do not depend on runtime args/kwargs, so computing them once
    # avoids repeated work and lets us ask the user at wrap-time.
    code_source = inspect.getsource(func)
    # Normalize code to ignore comment/docstring-only changes
    normalized_code = _normalize_code_for_hashing(code_source)
    code_hash = _deterministic_hash(normalized_code)

    file_path = os.path.join(
        autotest_path, *func.__module__.split("."), func.__name__ + ".pkl"
    )

    # stored_code_hash will be the code hash persisted with the data. If the user
    # accepts a code change we will store the new hash here (so serialization
    # at the end of wrapper uses the right value).
    stored_code_hash = code_hash
    # Default: don't ignore code changes unless user decided otherwise
    ignore_code_change = False

    # Determine initial decision now (at wrapping time). We only check and
    # possibly ask the user once per unique (old_hash,new_hash) tuple.
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as f:
                try:
                    fn_autotest_data = _serializer_load(f)
                except Exception:
                    f.seek(0)
                    fn_autotest_data = pickle.load(f)
                old_code_hash = fn_autotest_data.code_hash
                if code_hash != old_code_hash:
                    decision_key = (
                        func.__module__,
                        func.__name__,
                        old_code_hash,
                        code_hash,
                    )
                    if decision_key in _CODE_CHANGE_DECISIONS:
                        ignore_code_change = _CODE_CHANGE_DECISIONS[decision_key]
                    else:
                        ignore_code_change = _ask_user_about_code_change(
                            func.__module__, func.__name__
                        )
                        _CODE_CHANGE_DECISIONS[decision_key] = ignore_code_change

                    # Always update the stored hash when user makes a decision
                    # This prevents re-asking the same question
                    stored_code_hash = code_hash

                    # If user says logic didn't change, we need to immediately update
                    # the persisted data with the new hash to avoid asking again
                    if not ignore_code_change:
                        # Update the existing data with new hash
                        updated_data = FunctionAutoTest(
                            fn_autotest_data.all_inputs,
                            fn_autotest_data.all_outputs,
                            code_hash,
                        )
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        with open(file_path, "wb") as f:
                            try:
                                _serializer_dump(updated_data, f)
                            except Exception:
                                try:
                                    pickle.dump(updated_data, f)
                                except Exception:
                                    # If serialization fails, we'll handle it later
                                    pass
                else:
                    # hashes equal -> nothing to do
                    pass
        except Exception:
            # If loading fails, behave as if no prior data exists.
            stored_code_hash = code_hash
            old_code_hash = None
            ignore_code_change = False
    else:
        # No file yet: nothing to compare
        old_code_hash = None
        ignore_code_change = False

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

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                # try the more capable serializer first, fallback to stdlib pickle
                try:
                    fn_autotest_data = _serializer_load(f)
                except Exception:
                    f.seek(0)
                    fn_autotest_data = pickle.load(f)
                all_inputs = fn_autotest_data.all_inputs
                all_outputs = fn_autotest_data.all_outputs
                old_code_hash = fn_autotest_data.code_hash

                index = index_in_list(all_inputs, inputs)
                if index >= 0:
                    # If function code has changed, use the precomputed decision
                    if code_hash != old_code_hash:
                        ignore = ignore_code_change
                    else:
                        ignore = False

                    if ignore:  # We accept the change, hence we delete the old data
                        all_inputs.pop(index)
                        all_outputs.pop(index)
                    else:
                        old_output = all_outputs[index]
                        if is_equal(old_output, outputs):
                            return outputs
                        else:
                            diff_results = difflib.unified_diff(
                                str(old_output).splitlines(keepends=True),
                                str(outputs).splitlines(keepends=True),
                            )
                            sys.stderr.write("".join(diff_results))
                            # fail the test
                            raise AssertionError(
                                "Output changed in "
                                + func.__module__
                                + "/"
                                + func.__name__
                            )
        else:
            all_inputs = []
            all_outputs = []

        # in any other case, save the new output
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        all_inputs.append(inputs)
        all_outputs.append(outputs)

        # Try to pickle normally, but be defensive: some outputs (exceptions,
        # third-party objects) are not picklable. Fall back to safer
        # representations when pickle fails.
        def _safe_for_pickle(obj):
            try:
                pickle.dumps(obj)
                return obj
            except Exception:
                # Try to return a stable hash if possible, otherwise a repr
                try:
                    return Hash(hash(obj))
                except Exception:
                    return repr(obj)

        safe_all_inputs = []
        for inp_args, inp_kwargs in all_inputs:
            safe_args = tuple(_safe_for_pickle(a) for a in inp_args)
            safe_kwargs = {k: _safe_for_pickle(v) for k, v in inp_kwargs.items()}
            safe_all_inputs.append((safe_args, safe_kwargs))

        safe_all_outputs = []
        for out in all_outputs:
            safe_all_outputs.append(_safe_for_pickle(out))

        with open(file_path, "wb") as f:
            # Persist using the stored_code_hash which may have been updated
            # above if the user accepted a code change.
            try:
                _serializer_dump(
                    FunctionAutoTest(all_inputs, all_outputs, stored_code_hash), f
                )
            except Exception:
                try:
                    pickle.dump(
                        FunctionAutoTest(all_inputs, all_outputs, stored_code_hash), f
                    )
                except Exception:
                    # Last resort: dump sanitized versions so we don't crash the
                    # test collection step.
                    pickle.dump(
                        FunctionAutoTest(
                            safe_all_inputs, safe_all_outputs, stored_code_hash
                        ),
                        f,
                    )

        return outputs

    # add a custom attribute to the wrapper so that it can be identified as an autotest function
    setattr(wrapper, "__autotest__", True)
    return wrapper


def autotest_module(
    module: ModuleType, _visited: Optional[set] = None, _root_name: Optional[str] = None
):
    """
    Replace all functions in a module with autotest versions.
    Defensive: track visited modules to avoid infinite recursion and only
    recurse into submodules that belong to the same package root. This
    prevents descending into third-party packages (pytest, google, etc.)
    which can cause recursion and expose unpicklable objects.
    :param module: the module to wrap
    :param _visited: internal set of visited module ids
    :param _root_name: the root module name to constrain recursion
    :return: the wrapped module
    """
    if _visited is None:
        _visited = set()
    if _root_name is None:
        _root_name = getattr(module, "__name__", "")

    mid = id(module)
    if mid in _visited:
        return
    _visited.add(mid)

    for name, obj in list(module.__dict__.items()):
        # Only wrap functions defined in this module
        if (
            inspect.isfunction(obj)
            and not hasattr(obj, "__autotest__")
            and obj.__module__ == module.__name__
        ):
            setattr(module, name, autotest_func(obj))
        # Recurse into module attributes only if they are submodules of the same root
        elif isinstance(obj, ModuleType):
            mod_name = getattr(obj, "__name__", "")
            if (
                mod_name
                and _root_name
                and (mod_name == _root_name or mod_name.startswith(_root_name + "."))
            ):
                autotest_module(obj, _visited=_visited, _root_name=_root_name)
        # Wrap methods of classes declared in this module
        elif inspect.isclass(obj) and obj.__module__ == module.__name__:
            for method_name, m_obj in list(obj.__dict__.items()):
                if (
                    inspect.isfunction(m_obj)
                    and not hasattr(m_obj, "__autotest__")
                    and m_obj.__module__ == module.__name__
                ):
                    setattr(obj, method_name, autotest_func(m_obj))


def cmd():
    parser = argparse.ArgumentParser(description="AutoTest Command Line Tool")
    parser.add_argument("command", choices=["delete"], help="Command to execute")
    parser.add_argument("target", choices=["cache"], help="Target to apply command to")
    parser.add_argument(
        "--cache", "-C", help="Specify cache folder", default="autotestreg_data"
    )
    args = parser.parse_args()

    if args.command == "delete" and args.target == "cache":
        shutil.rmtree(args.cache, ignore_errors=True)
        print("Cache deleted successfully (" + args.cache + ")")

from sys import getrefcount
import re
from datetime import date, datetime, time
import inspect
import functools
from types import LambdaType

debug_info = True

primitives = set(
    [
        int,
        float,
        bool,
        str,
        datetime,
        date,
        time,
        complex
    ])

# Utils
def is_primitive(obj: object) -> bool:
    return type(obj) in primitives

def is_none(obj: object) -> bool:
    return obj is None

def is_magicmarked(s: str) -> bool:
    return re.match("^__(?:\w+)__$", s) != None

def is_collection(obj: object) -> bool:
    return getattr(obj, "__iter__", None) != None and getattr(obj, "__getitem__", None) != None

def is_kvbased(obj: object) -> bool:
    """Check if collection is based on <key> : <value> relations

        Returns:
            False - if an exception was occured during accessing value by __iter__() based key

            True - otherwise

    """
    for el in obj:
        try:
            val = obj[el]
        except Exception:
            return False
    return True

def pack_iterable(obj: object) -> dict:
    """Parse object as collection

        Supported objects:
            1)Object containing
    """
    if is_collection(obj):
        if is_kvbased(obj):
            subset = {}
            for key in obj:
                subset.update({key: obj[key]})
        else:
            subset = []
            for el in obj:
                subset.append(el)
        return subset
    else:
        raise ValueError(f"{obj} is not Iterable")

def pack_objstate(obj: object) -> dict:
    """Return object state as:
        
        1)Object state -> all fields and attributes except '__<attr>__' (magic) attributes
        
        2)As a primitive

        3)As a object collection if obj is iterable

    """
    result = {}
    state = [el for el in inspect.getmembers(obj, lambda el: not callable(el)) if not is_magicmarked(el[0])]
    for el in state:
        result[el[0]] = el[1]
    return result

def pack_callable(obj: object) -> dict:
    result = {}
    return inspect.findsource(obj)


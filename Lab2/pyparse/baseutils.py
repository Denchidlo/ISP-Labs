import builtins
import os
import re
from datetime import date, datetime, time
import inspect
import functools
import dis
from sys import builtin_module_names, modules

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

def is_basetype(obj: object) -> bool:
    for el in primitives:
        if el.__name__ == obj.__name__:
            return True
    if el in [dict, list, tuple, set]:
        if el.__name__ == obj.__name__:
            return True
    return False

def is_none(obj: object) -> bool:
    return obj is None

def has_source(obj: object) -> bool:
    return callable(obj) or inspect.isclass(obj)

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
                subset.update({key: pack(obj[key])})
        else:
            subset = []
            for el in obj:
                subset.append(pack(el))
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
    try:
        result.update({".type":pack(type(obj)), ".state": {}})
    except Exception:
        result.update({".type":pack(type(obj)), ".state": {}})
    state = [el for el in inspect.getmembers(obj, lambda el: not callable(el)) if not is_magicmarked(el[0])]
    for el in state:
        result[".state"][el[0]] = pack(el[1])
    return result

def pack(obj: object):
    if is_primitive(obj):
        return obj
    if inspect.ismodule(obj):
        try:
            return {".code": inspect.getsource(obj), ".bigmodule" : f"{obj.__name__}"}
        except Exception:
            return {".bigmodule": f"{obj.__name__}"}
    if getattr(obj, "__name__", None):
        if obj.__name__ in dir(builtins) and not is_basetype(obj):
            return {".builtin": obj.__name__}
        if  getattr(obj, "__module__", None):
            if has_source(obj):
                try:
                    return {".code": inspect.getsource(obj), ".module" : f"{obj.__module__}", ".name": obj.__name__}
                except Exception:
                    return {".name": obj.__name__, ".module": f"{obj.__module__}"}
    elif is_collection(obj):
        return pack_iterable(obj)
    else:
        return pack_objstate(obj)

def unpack(src: object, objtype=None):
    if isinstance(src, dict):
        if ".builtin" in src.keys():
            result = eval("{}".format(src[".builtin"]))
            return result
        elif ".bigmodule" in src.keys():
            try:
                exec("import {module}".format(src[".bigmodule"]))
                result = eval(src[".bigmodule"])
                return result
            except Exception:
                if ".code" in src.keys():
                    with open("{}/baseutil_temp.py".format("/".join(modules["__main__"].__file__.split('/')[:-1])), "w") as writer:
                        writer.write(src[".code"])
                    exec("import baseutil_temp as temp")
                    result = eval("temp")
                    os.unlink("{}/baseutil_temp.py".format("/".join(modules["__main__"].__file__.split('/')[:-1])))
                    return result
                else:
                    raise ValueError("Unknown type")
        elif ".name" in src.keys():
            if src[".module"] in modules.keys():
                try:
                    exec("from {module} import {name}".format(src[".module"], src[".name"]))
                    result = eval(src[".name"])
                    print(result)
                    return result
                except Exception:
                    if ".code" in src.keys():
                        
                        with open("{}/baseutil_temp.py".format("/".join(modules["__main__"].__file__.split('/')[:-1])), "w") as writer:
                            writer.write(src[".code"])
                        exec("from baseutil_temp import {}".format(src[".name"]))
                        result = eval(src[".name"])
                        os.unlink("{}/baseutil_temp.py".format("/".join(modules["__main__"].__file__.split('/')[:-1])))
                        return result
                    else:
                        raise ValueError("Unknown type")
            else:
                try:
                    with open("{}/baseutil_temp.py".format("/".join(modules["__main__"].__file__.split('/')[:-1])), "w") as writer:
                        writer.write(src[".code"])
                    exec("from baseutil_temp import {}".format(src[".name"]))
                    result = eval(src[".name"])
                    print(dir(result))
                    os.unlink("{}/baseutil_temp.py".format("/".join(modules["__main__"].__file__.split('/')[:-1])))
                    return result
                except Exception:
                    raise ValueError("Unknown type")
        elif ".type" in src.keys():
            obj_type = unpack(src[".type"])
            obj = object.__new__(obj_type)
            obj_state = unpack(src[".state"])
            for el in obj_state:
                setattr(obj, el, unpack(obj_state[el]))
            return obj
        else:
            if is_kvbased(src):
                return_dict = {}
                for el in src:
                    return_dict[el] = unpack(src[el])
                return return_dict
            elif is_collection(src):
                return_list = []
                for el in src:
                    return_list.append(unpack(el))
                return return_list



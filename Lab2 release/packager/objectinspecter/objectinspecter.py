import builtins
import inspect

primitives = set(
    [
        int,
        float,
        bool,
        str
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

def is_instance(obj):
    if not hasattr(obj, '__dict__'):
        return False
    if inspect.isroutine(obj): 
        return False
    if inspect.isclass(obj):
        return False
    else:
        return True

def is_none(obj: object) -> bool:
    return obj is None

def fetch_typereferences(cls):
    if inspect.isclass(cls):
        mro = inspect.getmro(cls)
        metamro = inspect.getmro(type(cls))
        metamro = tuple(cls for cls in metamro if cls not in (type, object))
        class_bases = mro
        if not type in mro and len(metamro) != 0:
            return class_bases[1:-1], metamro[0]
        else:
            return class_bases[1:-1], None
            
def fetch_funcreferences(func: object):
    if inspect.ismethod(func):
        func = func.__func__

    if not inspect.isfunction(func):
        raise TypeError("{!r} is not a Python function".format(func))

    code = func.__code__
    if func.__closure__ is None:
        nonlocal_vars = {}
    else:
        nonlocal_vars = {
            var : cell.cell_contents
            for var, cell in zip(code.co_freevars, func.__closure__)
       }

    global_ns = func.__globals__
    builtin_ns = global_ns.get("__builtins__", builtins.__dict__)
    if inspect.ismodule(builtin_ns):
        builtin_ns = builtin_ns.__dict__
    global_vars = {}
    builtin_vars = {}
    unbound_names = set()
    for name in code.co_names:
        if name in ("None", "True", "False"):
            continue
        try:
            global_vars[name] = global_ns[name]
        except KeyError:
            try:
                builtin_vars[name] = builtin_ns[name]
            except KeyError:
                unbound_names.add(name)

    return (nonlocal_vars, global_vars,
                       builtin_vars, unbound_names)
            
def deconstruct_class(cls):
    attributes = inspect.classify_class_attrs(cls)
    deconstructed = []
    for attr in attributes:
        if attr.defining_class == object or attr.defining_class == type:
            continue
        else:
            deconstructed.append((
                attr.name,
                attr.object,
                attr.kind
            ))
    return deconstructed

def deconstruct_func(func):
    references = fetch_funcreferences(func)
    func_code = inspect.getsource(func)
    return {
        ".name": func.__name__,
        ".code": func_code,
        ".references": references
    }

def getfields(obj):
    """Try to get as much attributes as possible"""
    members = inspect.getmembers(obj)
    
    cls = type(obj)
    type_attrnames = [el.name for el in inspect.classify_class_attrs(cls)]
    
    result = {}
    
    for member in members:
        if not member[0] in type_attrnames:
            result[member[0]] = member[1]
            
    return result

def deconstruct_instance(obj):
    type_ = type(obj)
    fields = getfields(obj)
    return (type_, fields)
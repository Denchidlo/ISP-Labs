import builtins
import os
import re
from datetime import date, datetime, time
import inspect
from sys import builtin_module_names, modules

def fetch_references(obj: object) -> dict:
    """Function fetch_reference used to get object references to another classes, variables, functions and so on

        Two cases are possible:

        1)If we come across with the callable we search the following references:

            - global

            - builtins

            - unbound 

            - nonlocals

        2)If we come across with the type we search:

            - metaclass

            - baseclasses 

    """
    # First case (callable)
    # Code was copied from inspect.getclosurevars()
    # check inspect for details 
    if inspect.ismethod(obj):
        func = obj.__func_
        if not inspect.isfunction(func):
            raise TypeError("{!r} is not a Python function".format(func))

        code = func.__code__
        # Nonlocal references are named in co_freevars and resolved
        # by looking them up in __closure__ by positional index
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
                # Because these used to be builtins instead of keywords, they
                # may still show up as name references. We ignore them.
                continue
            try:
                global_vars[name] = global_ns[name]
            except KeyError:
                try:
                    builtin_vars[name] = builtin_ns[name]
                except KeyError:
                    unbound_names.add(name)

        return {
            "global": global_vars,
            "builtins": builtin_vars, 
            "unbound": unbound_names,
            "nonlocals": nonlocal_vars
        }
    
    # Second case (class baseclasses and metaclass)
    elif inspect.isclass(obj):
        pass

def deconstruct_type(cls: object) -> dict:
    deconstructed = {
        "name": cls,
    }

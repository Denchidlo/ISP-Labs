from .objectinspecter import *
from .creator import *
from datetime import datetime
from sys import builtin_module_names, modules

class _Packer:
    def __init__(self):
        self.metainfo = {}

    def pack(self, obj: object):
        dump = self.dump(obj)
        if len(self.metainfo) == 0:
            return dump
        else:
            return {".META":self.metainfo, ".OBJ":dump}
        
    def dump(self, obj: object):
        obj_id = id(obj)       
        
        if is_none(obj):
            return None
        
        if is_primitive(obj):
            return obj
        
        if type(obj) in [list, set, tuple]:
            if isinstance(obj, dict):
                result = {key:self.dump(obj[key]) for key in obj}
            else:
                result = [self.dump(el) for el in obj]
            return result
        
        if isinstance(obj, datetime):
            return {".time":str(obj.isoformat())}
        
        if inspect.ismodule(obj):
            try:
                if self.metainfo.get(str(obj_id)) == None:
                    if obj.__name__ in builtin_module_names:
                        self.metainfo.update({str(obj_id):{".metatype" : "module", ".name": obj.__name__}})
                    else:
                        self.metainfo.update({str(obj_id):{"_code": inspect.getsource(obj), ".metatype" : "module", ".name": obj.__name__}})
            except Exception:
                self.metainfo.update({str(obj_id):{".metatype" : "module", ".name": obj.__name__}})
            return {".metaid": str(obj_id), "name": obj.__name__}
        
        if getattr(obj, "__name__", None) and not is_basetype(obj):
            if obj.__name__ in dir(builtins):
                return {".builtin": obj.__name__}
            
            if inspect.ismethod(obj) or inspect.isfunction(obj):
                function_module = obj.__module__
            
                if function_module in builtin_module_names:
                    self.metainfo.update({str(obj_id):{".metatype" : "builtin func", ".name": obj.__name__, ".module": function_module}})
                else:
                    deconstructed = deconstruct_func(obj)
                    codedump = deconstructed[".code"]
                    refs = deconstructed[".references"]
            
                    nonlocals_ = refs[0]
                    globals_ = refs[1]
                    builtins_ = refs[2]
                    unbounds_ = refs[3]
                    
                    deconstructed_refs = {
                        "nonlocals": {},
                        "globals": {},
                        "builtins": {},
                        "unbound": {}
                    }
                    
                    for key in nonlocals_:
                        new_id = id(nonlocals_[key])
                        el = self.dump(nonlocals_[key])
                        if self.metainfo.get(str(new_id)) == None:
                            self.metainfo.update({str(new_id): el})
                        deconstructed_refs["nonlocals"][key] = str(new_id)
                            
                    for key in globals_:
                        new_id = id(globals_[key])
                        el = self.dump(globals_[key])
                        if self.metainfo.get(str(new_id)) == None:
                            self.metainfo.update({str(new_id): el})
                        deconstructed_refs["globals"][key] = str(new_id)
                            
                    for key in builtins_:
                        new_id = id(builtins_[key])
                        el = self.dump(builtins_[key])
                        if self.metainfo.get(str(new_id)) == None:
                            self.metainfo.update({str(new_id): el})
                        deconstructed_refs["builtins"][key] = str(new_id)
                            
                    for key in unbounds_:
                        if key in dir(obj.__module__):
                            try:
                                exec(f"from {obj.__module__} import dump__{key}")
                                new_id = id(builtins_[key])
                                el = eval(f"dump__{key}")
                                print(el)
                                if self.metainfo.get(str(new_id)) == None:
                                    self.metainfo.update({str(new_id): self.dump(el)})
                                deconstructed_refs["unbounds"][key] = str(new_id)
                                print(f"{key} imported")
                            except Exception:
                                continue
                            
                    if self.metainfo.get(str(obj_id)) == None:
                        self.metainfo.update({str(obj_id):{".code": inspect.getsource(obj), ".metatype" : "func", ".name": obj.__name__, ".module": getattr(obj, "__module__", None), ".refs":deconstructed_refs}})
                    else:
                        self.metainfo[str(obj_id)].update({".code": inspect.getsource(obj), ".metatype" : "func", ".name": obj.__name__, ".module": getattr(obj, "__module__", None), ".refs":deconstructed_refs})
                        
                    return {".metaid": str(obj_id), ".name": obj.__name__}
            
            if is_instance(obj):
                type_, fields = deconstruct_instance(obj)
                type_id = id(type_)
                self.dump(type_)
                    
                data = {key: self.dump(fields[key]) for key in fields}
                return { ".metaid": str(type_id), ".fields": data}
            
            if inspect.isclass(obj):
                    
                mro = fetch_typereferences(obj)
                attrs = deconstruct_class(obj)
                
                mro = [self.dump(el) for el in mro]
                attrs = [{el[0]:self.dump(el[1])} for el in attrs]
                    
                if self.metainfo.get(str(obj_id)) == None:
                    self.metainfo.update({str(obj_id): {".metatype": "class", ".name": obj.__name__, ".module": getattr(obj, "__module__", None), ".class": {"mro":mro, "attrs":attrs}}})
                        
                return { ".metaid": str(obj_id), ".name": obj.__name__}

class _Unpacker:
    def __init__(self):
        self.metainfo = []
        self.data = None
        
    def get_dataitem(self, obj: object):
        pass
    
    def get_metaitem(self, obj: object):
        pass
    
    def unpack(self, obj: object):
        pass
import inspect

class AbstractMetaclass():
    _id = 0
    @staticmethod
    def create(mro):
        bases = ",".join([base.__name__ for base in mro[0][1:-1]])
        meta = "metaclass="+mro[1].__name__
        exec(f"class AbstractMetaTemplate_{AbstractMetaclass._id}({bases + meta}):\n\tpass")
        metaclass = eval(f"AbstractMetaTemplate_{AbstractMetaclass._id}")
        AbstractMetaclass._id += 1
        return metaclass

class AbstractClass():
    _id = 0
    @staticmethod
    def create(mro):
        bases = ",".join([base.__name__ for base in mro[0][1:-1]])
        print(mro[1])
        meta = "metaclass="+mro[1].__name__
        str_ = bases + ", "+ meta
        exec(f"class AbstractClassTemplate_{AbstractClass._id}({str_}):\n\tpass")
        _class = eval(f"AbstractClassTemplate_{AbstractClass._id}")
        AbstractClass._id += 1
        return _class

def create_class(name, mro=None, attributes=None):
    template = AbstractClass.create(mro)
    template.__class__.__name__ = name
    for key, attribute, kind in attributes:
        if key == "__dict__":
            continue
        elif kind == "static method":
            setattr(template, key, staticmethod(attribute))
        elif kind == "class method":
            setattr(template, key, classmethod(attribute))
        else:
            setattr(template, key, attribute)
    return template

def fetch_typereferences(cls):
    if inspect.isclass(cls):
        mro = inspect.getmro(cls)
        metamro = inspect.getmro(type(cls)) # for attributes stored in the metaclass
        metamro = tuple(cls for cls in metamro if cls not in (type, object))
        class_bases = mro
        return class_bases, metamro[0]
    else:
        raise TypeError("Type or class expected")

dict.__itemsize__
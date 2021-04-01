class AbstractMetaclass():
    _id = 0
    @staticmethod
    def create(mro):
        print(mro)
        bases = ",".join([base.__name__ for base in mro[0][1:-1]])
        print(bases)
        exec(f"class AbstractMetaTemplate_{AbstractMetaclass._id}({bases}):\n\tpass")
        metaclass = eval(f"AbstractMetaTemplate_{AbstractMetaclass._id}")
        AbstractMetaclass._id += 1
        return metaclass

class AbstractClass():
    _id = 0
    @staticmethod
    def create(mro):
        bases = ",".join([base.__name__ for base in mro[0][1:-1]])
        meta = "metaclass="+mro[1].__name__
        if bases != "":
            str_ = bases + ", "+ meta
        else:
            str_ = meta
        exec(f"class AbstractClassTemplate_{AbstractClass._id}({str_}):\n\tpass")
        _class = eval(f"AbstractClassTemplate_{AbstractClass._id}")
        AbstractClass._id += 1
        return _class

def create_class(name, mro=None, attributes=None):
    if mro[1]:
        template = AbstractClass.create(mro)
    else: 
        template = AbstractMetaclass.create(mro)
    template.__name__ = name
    for key, attribute, kind in attributes:
        try:
            if kind == "static method":
                setattr(template, key, attribute)
            elif kind == "class method":
                setattr(template, key, classmethod(attribute))
            else:
                setattr(template, key, attribute)
        except AttributeError:
            continue
    return template

def create_function(name, code, references):
    func = eval(code)
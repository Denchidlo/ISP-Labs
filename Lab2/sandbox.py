from lib import Serializer as ser
import json

serializer = ser.Serializer()


globala = "HI"

class MetaS(type):
    def __new__(cls, *args):
        obj = super(cls, cls).__new__(cls, *args)
        return obj

class Parent:
    def _getAttreasdasd(self):
        print(globala +  "Asdas")
    
class ClassA(Parent,metaclass=MetaS):
    a = range
    def __init__(self):
        self.dict = {"asd": 1}

def wrapper_(func):
    def wrap():
        print("boo!!!!")
        return func() 
    return wrap

def foo():
    print("ABC")

serializer.data = wrapper_(foo)

serializer.dump("sample.json")


serializer.data = lambda x: print(x)

serializer.dump("lambda.json")

serializer.data = ClassA

serializer.dump("class_a.json")
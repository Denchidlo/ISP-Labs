"""objects.py is used to storage all test object samples
"""

from sys import modules
from datetime import datetime

# Here shown all objects we test

# basic class
class BasicClass:
    pass

# basic func
def basic_func():
    pass

def func_arg(name):
    return name

# class with fields
class ClassWithFields:
    def __init__(self, string, num):
        self.string = string
        self.int = num

# class with attribute
class SomeClassWithAttribute:
    attr = "Some attribute"

# class with method
class SomeClassWithMethod:
    def do(self):
        return "Result"

files = {
    "json": "{}/resources/sample.json".format("/".join(modules["__main__"].__file__.split('/')[:-1])),
    "pickle": "{}/resources/sample.pickle".format("/".join(modules["__main__"].__file__.split('/')[:-1])),
    "toml": "{}/resources/sample.toml".format("/".join(modules["__main__"].__file__.split('/')[:-1])),
    "yaml": "{}/resources/sample.yaml".format("/".join(modules["__main__"].__file__.split('/')[:-1]))
}

samples = {
    "primitive check":{
        "int": 234,
        "float": 2.718281828,
        "str": "Some sample string",
        "boolean": True,
        "datetime": datetime(2005, 7, 14, 12, 30)
    },
    "base collections": {
        "dict": {
            "One": 1,
            "Two": 2,
            "Three": 3
        },
        "list": [1, 2, 3, 4, 5, 6, 7]
    },
    "advanced collections": {
        "aCollection": [
            1, "String", 3.141592653589793,
            {
                "key": "value",
                "list": [
                    1, 2, 3, 4
                ]
            }
        ]
    },
    "basic class": BasicClass(),
    "basic method": basic_func,
    "func with argument": func_arg,
    "object with fields": ClassWithFields("String asmple", 228),
    "class with attribute": SomeClassWithAttribute,
    "class with method": SomeClassWithMethod,

}


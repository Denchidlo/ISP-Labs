import json

class Car:
    def __init__(self, is_broken):
        self.engine = "WOW"
        self.weight = 10
        self.is_broken = is_broken

    def beep(self):
        return print("Beeep beeep mafacka!")

    some_attr = "IMovable"

i_zhiga = Car(True)

def obj_dump(obj):
    for name in dir(obj):
        if name.startswith("__"):
            continue
        if callable(obj.):
            print("Method : " + name.__str__)
        else:
            if obj.__getattribute__(name) is not None:
                print("Car attribute: " + name + " " + str(obj.__dict__[name]))
            else:
                print("Field" + str(obj.__dict__[name]))
        return None

obj_dump(i_zhiga)
            
import pickle

import tasks.Task12 as task

globalaa = "adsa"

def func():
    print("None" + globalaa)

with open("dump.pickle", "w") as writer:
    pickle.dump(task.ModelCreator._wrapped_init(func), writer)


import dis
import inspect

from pyparse.JSONEncoder import JsonEncoder 
from pyparse.baseutils import pack_objstate
import tasks.Task12 as task

_list = [123, 23.8944, "asdasd", {"qwe":13, 12:'q'}, True]
_dict = {
    123:12
}

o = task.Student(name="Vitya", average=12.0, inner_list=_list, inner_dict=_dict)

# Gets source code
# print(inspect.getsource(o.__init__))

# inspect.getfullargspec(o.__init__)

encoder = JsonEncoder()
state = pack_objstate(o)
print(state)
encoder._getlines(state, 0)

print("".join(encoder.json_strings))


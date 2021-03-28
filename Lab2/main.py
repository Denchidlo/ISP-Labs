import dis
import inspect

from pyparse.JSONEncoder import JsonEncoder 
from pyparse.baseutils import pack_objstate
import tasks.Task12 as task

o = task.Person(name="Vitya")

# Gets source code
# print(inspect.getsource(o.__init__))

# inspect.getfullargspec(o.__init__)

encoder = JsonEncoder()
encoder._getlines(pack_objstate(o), 0)

print(encoder.json_strings)


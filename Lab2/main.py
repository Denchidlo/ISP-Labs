import pyparse.baseserializer as util
import tasks.Task12 as task
import dis
import inspect

o = task.Person(name="Vitya")

print(inspect.getsource(o.__init__))

code = dis._get_code_object(o.__init__)

dis.disassemble(code)

print(inspect.getsourcelines(o.__init__)[0][1:])

func = compile(''.join(inspect.getsourcelines(o.__init__)[0][1:]), inspect.getsourcefile(o.__init__), mode="exec")


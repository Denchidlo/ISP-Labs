
from pyparse.json_extended import Json


with open("test.json", "r") as reader:
    ob = Json.load(reader)

ob.set_text("asdfsadfsdfsadfsaf")

print(dir(ob))

ob.analyse()

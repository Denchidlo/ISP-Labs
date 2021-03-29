from io import FileIO
from typing import Any, IO
from json import dumps, loads
from pyparse.baseutils import pack, unpack

class Json:
    base_dumps = dumps
    base_loads = loads

    def dump(obj: object, file: object=None) -> None:
        packed_obj = pack(obj)
        print(type(file))
        if file:
            file.write(Json.base_dumps(packed_obj))
        else:
            raise ValueError("File transfer aborted")

    def dumps(obj: object) -> None:
        packed_obj = pack(obj)
        return Json.base_dumps(packed_obj)

    def load(file: object) -> Any:
        if file:
            raw_obj = Json.base_loads(file.read())
            unpacked_obj = unpack(raw_obj)
            return unpacked_obj
        else:
            raise ValueError("File transfer aborted")

    def loads(toml: str) -> Any:
        raw_obj = Json.base_loads(toml)
        unpacked_obj = unpack(raw_obj)
        return unpacked_obj
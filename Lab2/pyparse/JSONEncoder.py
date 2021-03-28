from typing import Any
from datetime import datetime, time
from pyparse.baseutils import is_primitive, is_collection, is_kvbased, is_none
from pyparse.poolinstancer import PoolInstancer

class JsonEncoder(metaclass=PoolInstancer):
    item_separator = ","
    dict_start = "{\n"
    dict_end = "}"
    list_start = "[\n"
    list_end = "]"

    def __init__(self) -> None:
        self.json_strings = [""]

    @PoolInstancer.instancelock
    def __call__(self, obj: Any, objtype=None):
        self.json_strings = []
        self._getlines(obj, 0)
        return "".join(self.json_strings)

    def _getlines(self, obj: Any, tab: int, objtype=None):
        print(self.json_strings[-1])
        if is_none(obj):
            self.json_strings[-1] += 'null'
            return
        if is_primitive(obj):
            if isinstance(obj, str) or isinstance(obj, datetime) or isinstance(obj, time) or isinstance(obj, time):
                self.json_strings[-1] += f'"{str(obj)}"'
                return
            else:
                self.json_strings[-1] += f'{str(obj)}'
                return
        if is_collection(obj):
            idx = 0
            if is_kvbased(obj):
                self.json_strings[-1] += JsonEncoder.dict_start
                for key in obj:
                    new_string = JsonEncoder.tabulate(tab + 1) 
                    JsonEncoder._getlines(self, key, tab + 1)
                    self.json_strings[-1] += ": "
                    self.json_strings.append(new_string)
                    JsonEncoder._getlines(self, obj[key], tab + 1)
                    if idx != len(obj) - 1:
                        self.json_strings[-1] += JsonEncoder.item_separator
                    idx += 1
                    self.json_strings[-1] += '\n'
                new_string = JsonEncoder.tabulate(tab) + JsonEncoder.dict_end
                self.json_strings.append(new_string)
            else:
                self.json_strings[-1] += JsonEncoder.list_start
                for el in obj:
                    new_string = JsonEncoder.tabulate(tab + 1)
                    JsonEncoder._getlines(self, el, tab + 1)
                    self.json_strings.append(new_string)
                    if idx != len(obj) - 1:
                        self.json_strings[-1] += JsonEncoder.item_separator
                    idx += 1
                    self.json_strings[-1] += '\n'
                new_string = JsonEncoder.tabulate(tab) + JsonEncoder.list_end
                self.json_strings.append(new_string)

    @staticmethod
    def tabulate(num: int) -> str:
        return "".join(['\t' for _ in range(num)])
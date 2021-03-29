from typing import Any
from datetime import datetime, time
import re
from pyparse.baseutils import is_primitive, is_collection, is_kvbased, is_none
import pyparse.poolinstancer as pool

class JsonEncoder(metaclass=pool.PoolInstancer):
    """JsonEncoder is a descriptor used to create JSON string 

    """
    item_separator = ","
    dict_start = "{\n"
    dict_end = "}"
    list_start = "[\n"
    list_end = "]"
    @pool.thread_local
    def __init__(self) -> None:
        self.json_strings = [""]

    @pool.thread_local
    def _getlines(self, obj: Any, tab: int, objtype=None) -> None:
        if is_none(obj):
            self.json_strings[-1] += 'null'
            return
        if is_primitive(obj):
            if isinstance(obj, str) or isinstance(obj, datetime) or isinstance(obj, time) or isinstance(obj, time):
                self.json_strings[-1] += f'"{str(obj)}"'
            else:
                self.json_strings[-1] += f'{str(obj)}'
            return
        if is_collection(obj):
            idx = 0
            if is_kvbased(obj):
                self.json_strings[-1] += JsonEncoder.dict_start
                for key in obj:
                    new_string = JsonEncoder.tabulate(tab + 1) 
                    self.json_strings.append(new_string)
                    JsonEncoder._getlines(self, key, tab + 1)
                    self.json_strings[-1] += ": "
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
                    self.json_strings.append(new_string)
                    JsonEncoder._getlines(self, el, tab + 1)
                    if idx != len(obj) - 1:
                        self.json_strings[-1] += JsonEncoder.item_separator
                    idx += 1
                    self.json_strings[-1] += '\n'
                new_string = JsonEncoder.tabulate(tab) + JsonEncoder.list_end
                self.json_strings.append(new_string)

    @pool.instancelock
    def encode(self, obj: Any, objtype=None) -> str:
        self._getlines(obj, 0)
        return ''.join(self.json_strings)
        
    @staticmethod
    def tabulate(num: int) -> str:
        return "".join(['\t' for _ in range(num)])

class JsonDecoder(metaclass=pool.PoolInstancer):
    def __init__(self):
        self.responce = None

    @pool.instancelock
    def decode(self):
        pass

    @pool.thread_local
    def _getobject(s: str):
        # Float point case
        if re.fullmatch(r"^[\s\n]*(?:(?:[+-]?(?:\d+(?:\.\d*)|\.\d+)(?:[eE][+-]?\d+)?)|NaN|-?Infinity)[\s\n]*$", s) != None:
            return float(JsonDecoder._format(s, " \t\n\r"))
        if re.fullmatch(r"^[\s\n]*(?:[+-]?(?:\d+))[\s\n]*$", s) != None:
            return int(JsonDecoder._format(s, " \t\n\r"))
        if re.fullmatch(r"^[\s\n]*(?:null)[\s\n]*$", s) != None:
            return None
        if re.fullmatch(r"^[\s\n]*(?:\"(?:.|\n)*\")[\s\n]*$", s) != None:
            # TO DO: string truncation
            pass
        res = re.match(r"^[\s\n]*\{(?P<comma_pairs>(?:[\s\n]*(?:\"(?:.|\n)*\")[\s\n]*\:[\s\n]*(?:.|\n)*[\s\n]*\,[\s\n]*)*)(?P<last>(?:[\s\n]*(?:\"(?:.|\n)*\")[\s\n]*\:[\s\n]*(?:.|\n)*[\s\n]*))[\s\n]*\}[\s\n]*$", s)
        if res:
            return_dict = {}
            try:
                enum_kv = res["comma_values"]
                dict_items = enum_kv.split(',')
                for item in dict_items:
                    kv_regex = re.match(r"^[\s\n]*\"(?P<key>(?:.|\n))\"[\s\n]*\:[\s\n]*(?P<value>(?:.|\n))[\s\n]*")
            except Exception:
                dict_items = []
            

    @staticmethod
    def _format(s: str, sym_ignored: str) -> str:
        result = s
        for sym in sym_ignored:
            result = result.replace(sym, "")
        return result
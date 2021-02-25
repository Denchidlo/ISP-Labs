class Employee:
    def __init__(self, js=None):
        if js is None:
            raise ValueError("None is not valid")
        if isinstance(js, list):
            if len(js) != 0:
                jsonDict = js.pop()
            else:
                self.fio = ""
                self.degree = ""
                return
        else:
            raise TypeError("js in Employee.__init__(self, js) expexted 'list', but got" + js.__name__)
        if not isinstance(jsonDict, dict):
            raise TypeError("Wrong JSON occured") 
        if (set(['degree', 'fio']).issubset(set(jsonDict.keys()))):
            self.fio = jsonDict['fio']
            self.degree = jsonDict['degree']
        else:
            raise KeyError("Key mapping fault")
        return
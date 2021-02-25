class Employee:
    def __init__(self, js=None):
        if js is None:
            return
        if isinstance(js, list):
            if len(js) != 0:
                jsonDict = js.pop()
            else:
                self.fio = ""
                self.degree = ""
                return
        self.fio = jsonDict['fio']
        self.degree = jsonDict['degree']
        return
import MySchedule.Employee as emp

class ScheduleModel:
    def __init__(self, js=None):
        if js is None:
            raise ValueError("None is not valid")
        if isinstance(js,str):
            jsonDict = json.loads(js)
        if isinstance(js, list):
            if len(js) != 0:
                jsonDict = js.pop()
            else:
                return  None          
        if isinstance(js, dict):
            jsonDict = js
        if (set(['subject', 'auditory', 'lessonTime', 'lessonType', 'employee']).issubset(set(jsonDict.keys()))):
            if len(jsonDict['auditory']) == 0:
                self.auditory = "  -  "
            else:            
                self.auditory = jsonDict['auditory'].pop()
            self.subject = jsonDict['subject']
            self.lessonTime = jsonDict['lessonTime']
            self.lessonType = jsonDict['lessonType']
            self.employee = emp.Employee(jsonDict['employee'])
        else:
            raise KeyError("Key mapping fault")
        return
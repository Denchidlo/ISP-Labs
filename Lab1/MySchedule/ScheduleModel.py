import MySchedule.Employee as emp

class ScheduleModel:
    """Model of day schedule"""
    def __init__(self, js = None):
        if js is None:
            return
        if isinstance(js,str):
            jsonDict = json.loads(js)
        else:
            jsonDict = js
        if isinstance(js, list):
            if len(js) != 0:
                jsonDict = js.pop()
            else:
                return            
        if len(jsonDict['auditory']) == 0:
            self.auditory = "  -  "
        else:            
            self.auditory = jsonDict['auditory'].pop()
        self.subject = jsonDict['subject']
        self.lessonTime = jsonDict['lessonTime']
        self.lessonType = jsonDict['lessonType']
        self.employee = emp.Employee(jsonDict['employee'])
        return
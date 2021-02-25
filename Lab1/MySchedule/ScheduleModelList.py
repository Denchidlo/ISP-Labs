import MySchedule.ScheduleModel as model

class ScheduleModelList:
    def __init__(self, js = None):
        self.lessonList = []
        if js is None:
            return
        if js is str:
            jsonDict = json.loads(js)
        else:
            jsonDict = js
        if isinstance(jsonDict, list):
            for lesson in jsonDict:
                self.lessonList.append(model.ScheduleModel(lesson))
        return
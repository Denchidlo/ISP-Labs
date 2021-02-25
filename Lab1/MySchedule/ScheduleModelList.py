import MySchedule.ScheduleModel as model

class ScheduleModelList:
    def __init__(self, js=None):
        self.lessonList = []
        if js is None:
            return
        if js is str:
            jsonList = json.loads(js)
        else:
            jsonList = js
        if isinstance(jsonList, list):
            for lesson in jsonList:
                self.lessonList.append(model.ScheduleModel(lesson))
        else:
            raise TypeError("Invalid JSON format")
        return
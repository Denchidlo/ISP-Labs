import json
import requests as req
from requests.exceptions import HTTPError
import MySchedule.ScheduleModelList as scheduleList

class GroupSchedule:
    def __init__(self, js=None, group="953506"):
        if js is None:
            scheduleResponse = req.get(self.requestString + group)
            if scheduleResponse.status_code == 200:
                self.deserialize(scheduleResponse.json())
            else:
                raise HTTPError("Request failed in 'GroupSchedule.__init__'")
        else:
            self.deserialize(js)
        self.initialized = True
        return

    def deserialize(self, js=None):
        if js is None:
            raise ValueError("Empty json")
        else:
            if not isinstance(js, dict):
                raise TypeError("js in method 'GroupSchedule.deserialize(self, js)' need to be a dict, but got" + scheduleList.__name__)
            if (set(['todaySchedules', 'tomorrowSchedules', 'todayDate']).issubset(set(js.keys()))):
                self.todaySchedules = scheduleList.ScheduleModelList(js['todaySchedules'])
                self.tomorrowShedules = scheduleList.ScheduleModelList(js['tomorrowSchedules'])
                self.todayDate = js['todayDate']
            else:
                raise KeyError("Key mapping fault")
        return
    
    def lessons_amount(self):
        if self.initialized == True:
            return len(self.todaySchedules.lessonList)

    def print_schedule(self):
        if self.initialized == True:
            print('************************************')
            print("*Рассписание на сегодня: {date}*".format(date=self.todayDate))
            print('************************************')
            counter = 1
            for lesson in self.todaySchedules.lessonList:
                print("{counter}|{auditory:<5}|{subject:^10}|{time:11}|{type}|{fio:^10}".format(counter=str(counter), auditory=lesson.auditory, 
                                                                                             subject=lesson.subject, time=lesson.lessonTime,
                                                                                             type=lesson.lessonType, fio=lesson.employee.fio))
                counter += 1
        else:
            print("Invalid behaviour")

    requestString = "https://journal.bsuir.by/api/v1/studentGroup/schedule?studentGroup="
import json
import requests as req
import MySchedule.ScheduleModelList as scheduleList

class GroupSchedule:
    def __init__(self, js = None, group = "953506"):
        if js is None:
            schedule = req.get(self.requestString + group)
            self.deserialize(schedule.json())
        else:
            self.deserialize(js)
        self.initialized = True
        return

    def deserialize(self, js = None):
        if js is None:
            raise ValueError("Empty json")
        else:
            self.todaySchedules = scheduleList.ScheduleModelList(js['todaySchedules'])
            self.tomorrowShedules = scheduleList.ScheduleModelList(js['tomorrowSchedules'])
            self.todayDate = js['todayDate']
        return
    
    def lessons_amount(self):
        if self.initialized == True:
            return len(self.todaySchedules.lessonList)

    def print_schedule(self):
        if self.initialized == True:
            print('************************************')
            print("*Рассписание на сегодня: {date}*".format(date = self.todayDate))
            print('************************************')
            counter = 1
            for lesson in self.todaySchedules.lessonList:
                print("{counter}|{auditory}|{subject:^10}|{time:11}|{type}|{fio:^10}".format(counter = str(counter), auditory = lesson.auditory, 
                                                                                                    subject = lesson.subject, time = lesson.lessonTime,
                                                                                                    type = lesson.lessonType, fio = lesson.employee.fio))
                counter += 1

    requestString = "https://journal.bsuir.by/api/v1/studentGroup/schedule?studentGroup="
import requests as req
import json
import MySchedule.GroupSchedule as groups

obj = groups.GroupSchedule(group="953506")
obj.print_schedule()
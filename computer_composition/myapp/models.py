import json

from django.db.models import *


class StudentTable(Model):
    stu_id = CharField(max_length=100, null=True)
    stu_name = CharField(max_length=100, null=True)
    stu_room_num = IntegerField(null=True, default=0)
    stu_seat_num = IntegerField(null=True, default=0)

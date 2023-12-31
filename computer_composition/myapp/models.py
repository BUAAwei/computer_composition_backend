import json

from django.db.models import *


class StaticData(Model):
    static_id = IntegerField(null=True, default=0)
    static_password = CharField(max_length=100, null=True)
    static_cookie = CharField(max_length=200, null=True)
    static_lvt = CharField(max_length=200, null=True)
    static_lpvt = CharField(max_length=200, null=True)


class StudentTable(Model):
    stu_id = CharField(max_length=100, null=True)
    stu_name = CharField(max_length=100, null=True)
    stu_room_num = IntegerField(null=True, default=0)
    stu_seat_num = IntegerField(null=True, default=0)
    is_register = BooleanField(default=False)
    is_submit = BooleanField(default=False)


class Student(Model):
    stu_id = CharField(max_length=100, null=True)
    stu_name = CharField(max_length=100, null=True)
    class_id = IntegerField(null=True, default=0)


class StudentClass(Model):
    class_id = AutoField(primary_key=True)
    class_name = CharField(max_length=100, null=True)
    class_teacher = CharField(max_length=100, null=True)
    class_year = CharField(max_length=100, null=True)
    class_season = CharField(max_length=100, null=True)
    student_list = ManyToManyField('Student')


class ExamRoom(Model):
    er_id = AutoField(primary_key=True)
    er_name = CharField(max_length=100, null=True)
    er_student_list = ManyToManyField('StudentTable')
    er_case_id = IntegerField(null=True, default=0)


class Exam(Model):
    exam_id = AutoField(primary_key=True)
    exam_name = CharField(max_length=100, null=True)
    exam_time = CharField(max_length=100, null=True)
    exam_room_list = ManyToManyField('ExamRoom')
    join_class_list = ManyToManyField('StudentClass')


class ExamRoomSeatCase(Model):
    ersc_id = AutoField(primary_key=True)
    ersc_seat_num = IntegerField(null=True, default=0)
    ersc_x = IntegerField(null=True, default=0)
    ersc_y = IntegerField(null=True, default=0)


class ExamRoomCase(Model):
    erc_id = AutoField(primary_key=True)
    erc_name = CharField(max_length=100, null=True)
    erc_x_length = IntegerField(null=True, default=0)
    erc_y_length = IntegerField(null=True, default=0)
    erc_seats = ManyToManyField('ExamRoomSeatCase')




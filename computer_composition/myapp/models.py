import json

from django.db.models import *


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


class Exam(Model):
    exam_id = AutoField(primary_key=True)
    exam_name = CharField(max_length=100, null=True)
    exam_time = CharField(max_length=100, null=True)
    exam_room_list = ManyToManyField('ExamRoom')
    join_class_list = ManyToManyField('StudentClass')

from django.urls import path
from .views import *

urlpatterns = [
    path('update_password', update_password, name='update_password'),
    path('get_password', get_password, name='get_password'),
    path('update_cookie', update_cookie, name='update_cookie'),
    path('get_cookie', get_cookie, name='get_cookie'),
    path('create_class', create_class, name='create_class'),
    path('delete_class', delete_class, name='delete_class'),
    path('update_class', update_class, name='update_class'),
    path('get_classes', get_classes, name='get_classes'),
    path('get_all_classes', get_all_classes, name='get_all_classes'),
    path('get_class_student', get_class_student, name='get_class_student'),
    path('add_student_to_class', add_student_to_class, name='add_student_to_class'),
    path('add_students_list_to_class', add_students_list_to_class, name='add_students_list_to_class'),
    path('export_students_list_in_class', export_students_list_in_class, name='export_students_list_in_class'),
    path('delete_student', delete_student, name='delete_student'),
    path('create_exam', create_exam, name='create_exam'),
    path('get_all_exams', get_all_exams, name='get_all_exams'),
    path('get_room_in_exam', get_room_in_exam, name='get_room_in_exam'),
    path('get_class_in_exam', get_class_in_exam, name='get_class_in_exam'),
    path('delete_exam', delete_exam, name='delete_exam'),
    path('set_case_to_exam', set_case_to_exam, name='set_case_to_exam'),
    path('create_class_case', create_class_case, name='create_class_case'),
    path('get_all_class_case', get_all_class_case, name='get_all_class_case'),
    path('get_seats_in_case', get_seats_in_case, name='get_seats_in_case'),
    path('delete_case', delete_case, name='delete_case'),
    path('upload_excel', upload_excel, name='upload_excel'),
    path('clear_database', clear_database, name='clear_database'),
    path('get_information', get_information, name='get_information')
]

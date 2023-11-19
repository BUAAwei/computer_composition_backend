import json

import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from openpyxl import load_workbook
import random
import openpyxl

from .models import *


@csrf_exempt
@require_http_methods(['POST'])
def update_password(request):
    data = json.loads(request.body)
    new_password = data.get('password')
    static_data = StaticData.objects.get(static_id=1)
    static_data.static_password = new_password
    static_data.save()
    return JsonResponse({'msg': '密码修改成功'})


@csrf_exempt
@require_http_methods(['POST'])
def get_password(request):
    static_data = StaticData.objects.get(static_id=1)
    return JsonResponse({'password': static_data.static_password})


@csrf_exempt
@require_http_methods(['POST'])
def update_cookie(request):
    data = json.loads(request.body)
    new_cookie = data.get('cookie')
    static_data = StaticData.objects.get(static_id=1)
    static_data.static_cookie = new_cookie
    static_data.save()
    return JsonResponse({'msg': 'cookie修改成功'})


@csrf_exempt
@require_http_methods(['POST'])
def get_cookie(request):
    static_data = StaticData.objects.get(static_id=1)
    return JsonResponse({'cookie': static_data.static_cookie})


@csrf_exempt
@require_http_methods(['POST'])
def create_class(request):
    data = json.loads(request.body)
    class_name = data.get('name')
    class_teacher = data.get('teacher')
    class_year = data.get('year')
    class_season = data.get('season')
    new_class = StudentClass.objects.create(class_name=class_name, class_teacher=class_teacher, class_year=class_year, class_season=class_season)
    new_class.save()
    return JsonResponse({'class_id': new_class.class_id, 'msg': "创建班级成功"})


@csrf_exempt
@require_http_methods(['POST'])
def delete_class(request):
    data = json.loads(request.body)
    class_id = data.get('id')
    try:
        student_class = StudentClass.objects.get(class_id=class_id)
        student_class.delete()
        return JsonResponse({'msg': '班级删除成功'})
    except StudentClass.DoesNotExist:
        return JsonResponse({'msg': '班级不存在'})


@csrf_exempt
@require_http_methods(['POST'])
def update_class(request):
    data = json.loads(request.body)
    class_id = data.get('id')
    student_class = StudentClass.objects.get(class_id=class_id)
    class_name = data.get('name')
    class_teacher = data.get('teacher')
    class_year = data.get('year')
    class_season = data.get('season')
    student_class.class_name = class_name
    student_class.class_teacher = class_teacher
    student_class.class_year = class_year
    student_class.class_season = class_season
    student_class.save()
    return JsonResponse({'msg': '班级信息修改成功'})


@csrf_exempt
@require_http_methods(['POST'])
def get_classes(request):
    data = json.loads(request.body)
    class_year = data.get('year')
    class_season = data.get('season')
    student_classes = StudentClass.objects.filter(class_year=class_year, class_season=class_season)
    class_list = []
    for student_class in student_classes:
        class_list.append({
            'class_id': student_class.class_id,
            'name': student_class.class_name,
            'teacher': student_class.class_teacher,
            'year': student_class.class_year,
            'season': student_class.class_season,
            'students': len(student_class.student_list.all())
        })
    return JsonResponse({'classes': class_list})


@csrf_exempt
@require_http_methods(['POST'])
def get_all_classes(request):
    student_classes = StudentClass.objects.all()
    class_list = []
    for student_class in student_classes:
        class_list.append({
            'class_id': student_class.class_id,
            'name': student_class.class_name,
            'teacher': student_class.class_teacher,
            'year': student_class.class_year,
            'season': student_class.class_season,
            'students': len(student_class.student_list.all())
        })
    return JsonResponse({'classes': class_list})


@csrf_exempt
@require_http_methods(['POST'])
def get_class_student(request):
    data = json.loads(request.body)
    class_id = data.get('id')
    student_class = StudentClass.objects.get(class_id=class_id)
    student_list = student_class.student_list.all()
    students = []
    for student in student_list:
        students.append({
            'stu_id': student.stu_id,
            'stu_name': student.stu_name
        })
    return JsonResponse({'students': students})


@csrf_exempt
@require_http_methods(['POST'])
def add_student_to_class(request):
    data = json.loads(request.body)
    student_id = data.get('student_id')
    student_name = data.get('student_name')
    class_id = data.get('class_id')

    try:
        student_class = StudentClass.objects.get(class_id=class_id)
    except StudentClass.DoesNotExist:
        return JsonResponse({'msg': '班级不存在'})

    student, created = Student.objects.get_or_create(stu_id=student_id)
    student.stu_name = student_name
    student.save()

    student_class.student_list.add(student)

    return JsonResponse({'msg': '学生已成功加入班级'})


@csrf_exempt
@require_http_methods(['POST'])
def add_students_list_to_class(request):
    class_id = request.POST.get('class_id')
    file = request.FILES.get('file')

    try:
        student_class = StudentClass.objects.get(class_id=class_id)
    except StudentClass.DoesNotExist:
        return JsonResponse({'msg': '班级不存在'})

    students_added = 0
    try:
        workbook = load_workbook(file)
        sheet = workbook.active
        for row in sheet.iter_rows(values_only=True):
            student_id, student_name = row[:2]
            student, created = Student.objects.get_or_create(stu_id=student_id)
            student.stu_name = student_name
            student.save()
            student_class.student_list.add(student)
            students_added += 1

        return JsonResponse({'msg': f'成功添加 {students_added} 个学生到班级'})
    except Exception as e:
        return JsonResponse({'msg': f'添加学生失败：{str(e)}'})


@csrf_exempt
@require_http_methods(['POST'])
def export_students_list_in_class(request):
    data = json.loads(request.body)
    class_id = data.get('class_id')
    student_class = StudentClass.objects.get(class_id=class_id)

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    students = student_class.student_list.all()
    row = 1
    for student in students:
        sheet.cell(row=row, column=1, value=student.stu_id)
        sheet.cell(row=row, column=2, value=student.stu_name)
        row += 1

    # 创建响应对象
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=student_list_class_{class_id}.xlsx'

    # 保存文件到响应对象
    workbook.save(response)

    return response


@csrf_exempt
@require_http_methods(['POST'])
def delete_student(request):
    data = json.loads(request.body)
    stu_id = data.get('student_id')
    stu_name = data.get('student_name')
    try:
        student = Student.objects.get(stu_id=stu_id, stu_name=stu_name)
        student.delete()
        return JsonResponse({'msg': '学生删除成功'})
    except StudentClass.DoesNotExist:
        return JsonResponse({'msg': '学生不存在'})


@csrf_exempt
@require_http_methods(['POST'])
def create_exam(request):
    data = json.loads(request.body)
    join_class = data.get('join_class')
    exam_name = data.get('name')
    exam_time = data.get('time')
    num = data.get('num')
    exam = Exam.objects.create(exam_name=exam_name, exam_time=exam_time)
    students = []
    for class_id in join_class:
        try:
            student_class = StudentClass.objects.get(class_id=class_id)
            students.extend(student_class.student_list.all())
            exam.join_class_list.add(student_class)
        except StudentClass.DoesNotExist:
            return JsonResponse({'msg': '班级不存在'})

    random.shuffle(students)

    total_students = len(students)
    students_per_room = total_students // num + 1
    for i in range(num):
        room_name = f'Room {i + 1}'
        room = ExamRoom.objects.create(er_name=room_name)
        for j in range(students_per_room):
            if i * students_per_room + j >= len(students):
                break
            student = students[i * students_per_room + j]
            student_table = StudentTable.objects.create(stu_id=student.stu_id, stu_name=student.stu_name)
            student_table.stu_room_num = i + 1
            student_table.stu_seat_num = j + 1
            student_table.save()
            room.er_student_list.add(student_table)
        room.save()
        exam.exam_room_list.add(room)
    exam.save()
    return JsonResponse({'msg': '考试和考场创建成功'})


@csrf_exempt
@require_http_methods(['POST'])
def upload_excel(request):
    excel_file = request.FILES['file']
    # 使用pandas读取Excel文件
    df = pd.read_excel(excel_file)

    # 遍历DataFrame的每一行，将数据存入数据库
    for index, row in df.iterrows():
        student = StudentTable(
            stu_id=row['stu_id'],
            stu_name=row['stu_name'],
            stu_room_num=row['stu_room_num'],
            stu_seat_num=row['stu_seat_num']
        )
        student.save()

    return HttpResponse('上传成功！')


@csrf_exempt
@require_http_methods(['POST'])
def clear_database(request):
    # 清空StudentTable表中的所有数据
    StudentTable.objects.all().delete()
    return HttpResponse('数据库已清空！')


@csrf_exempt
@require_http_methods(['POST'])
def get_information(request):
    # 初始化Chrome浏览器
    driver = webdriver.Chrome()

    # 打开网站
    driver.get("https://judge.buaa.edu.cn/admin/courseAdmin/examAdmin/examResult.jsp?examID=647&courseFlag=1654")
    # driver.get("https://judge.buaa.edu.cn/admin/login.jsp")
    # adminname_input = driver.find_element(By.ID,'adminname')
    # password_input = driver.find_element(By.ID,'password')
    # # username_input = driver.find_element_by_name("adminname")
    # # password_input = driver.find_element_by_name("password")
    # adminname_input.send_keys("21371195")
    # password_input.send_keys("21371195@buaa.edu.cn")
    # password_input.send_keys(Keys.RETURN)
    # 在页面上查找元素
    # driver.add_cookie()
    cookie_data = {
        "JSESSIONID": "5DC762D32BDB0097C35A6A38DB748421",
        "Hm_lvt_9eca16a516f8b449709378fbcbb6b200": "1698063708,1698064649,1698067832",
        "Hm_lpvt_9eca16a516f8b449709378fbcbb6b200": "1698067835"
    }
    for name, value in cookie_data.items():
        cookie = {
            'name': name,
            'value': value
        }
        driver.add_cookie(cookie)
    driver.refresh()
    # element = driver.find_element(By.CLASS_NAME,"even")
    elements1 = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "odd")))
    elements2 = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "even")))
    elements = elements1 + elements2
    message_list = []
    # 获取元素的文本内容
    for element in elements:
        text = element.text
        parts = text.split()
        if parts[-1] != '未提交答案':
            print(parts[1], parts[2], '已提交答案')
        else:
            print(parts[1], parts[2], parts[-1])
        if parts[-1] != '未提交答案':
            message_info = {
                "stu_id": parts[1],
                "stu_name": parts[2],
                "is_submit": '已提交答案'
            }
        else:
            message_info = {
                "stu_id": parts[1],
                "stu_name": parts[2],
                "is_submit": parts[-1]
            }
        message_list.append(message_info)
    # 关闭浏览器
    driver.quit()
    return JsonResponse({"submit_message": message_list})

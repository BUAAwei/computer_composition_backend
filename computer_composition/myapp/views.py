import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


from .models import StudentTable


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

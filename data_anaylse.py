# -*- coding: UTF-8 -*-
'''
@Project ：ch_cup 
@File    ：data_anaylse.py
@IDE     ：PyCharm 
@Author  ：温情止于晚风
@Date    ：2023/11/22 18:38 
'''
#统计薪资层面

import pymongo
from pymongo import MongoClient
import re
import matplotlib.pyplot as plt
client = MongoClient("127.0.0.1",27017)
db = client["boss"]
collection = db["python"]
data_list = []
year_salary = []
pattern = r"\d+"



#设置字体的默认参数避免乱码
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

def salary_model(data):
    data = str(data)
    data = data.strip("[]'")
    if "薪" in data:
        matches = re.findall(pattern, data)
        salary_min = int(matches[0])
        salary_max = int(matches[1])
        salary_structure = int(matches[2])
        annual_salary = (salary_min + salary_max) / 2 * salary_structure
        year_salary.append(annual_salary)
    elif "天" in data:
        matches = re.findall(pattern, data)
        salary_min = int(matches[0])
        salary_max = int(matches[1])
        annual_salary = (salary_min + salary_max) / 2 * 365 // 1000
        year_salary.append(annual_salary)
    elif "周" in data :
        matches = re.findall(pattern, data)
        salary_min = int(matches[0])
        salary_max = int(matches[1])
        annual_salary = (salary_min + salary_max) / 2 * 52 // 1000   #一年按52周
        year_salary.append(annual_salary)
    elif "月" in data :
        matches = re.findall(pattern, data)
        salary_min = int(matches[0]) // 1000
        salary_max = int(matches[1]) // 1000
        annual_salary = (salary_min + salary_max) * 12
        year_salary.append(annual_salary)
    elif "时" in data :
        matches = re.findall(pattern, data)
        salary_min = int(matches[0])
        salary_max = int(matches[1])
        annual_salary = (salary_min + salary_max) / 2 * 10 * 365 // 1000   #一天按工作10h
        year_salary.append(annual_salary)
    else:
        matches = re.findall(pattern, data)
        salary_min = int(matches[0])
        salary_max = int(matches[1])
        annual_salary = (salary_min + salary_max) / 2 * 12
        year_salary.append(annual_salary)

def main() :
    city = str(input("请输入你想要了解薪资情况的城市,目前只支持有关python岗位\n"))
    documents = collection.find({'salary': {'$exists': True}})
    for document in documents :
        if city in str(document["address"]) :
            data = document["salary"]
            data_list.append(data)
            salary_model(data)

    for index,data in enumerate(year_salary) :
        print(index,data)


    max_salary = max(year_salary)
    min_salary = min(year_salary)
    mean_salary = sum(year_salary) // len(year_salary)
    print( f"{city}平均年新为{mean_salary}K")
    print(f"{city}平均最高年薪为{max_salary}K")
    print(f"{city}平均最低年薪为{min_salary}K")
    labels = ["平均年新","平均最高年薪","平均最低年薪"]
    values = [mean_salary,max_salary,min_salary]
    colors = ["red","green","blue"]
    plt.bar(labels,values,color=colors)
    plt.xlabel("薪资情况")
    plt.ylabel("年薪(K)")
    plt.title("年薪统计情况")
    # 在每个柱形图上显示数值
    for i in range(len(labels)):
        plt.text(i, values[i], str(values[i]), ha='center', va='bottom')

    # 添加标签和标题
    # plt.legend(loc='upper left')
    plt.show()

if __name__ == '__main__':
    main()
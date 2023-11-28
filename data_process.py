# -*- coding: UTF-8 -*-
'''
@Project ：ch_cup 
@File    ：data_process.py
@IDE     ：PyCharm 
@Author  ：温情止于晚风
@Date    ：2023/11/1 15:33 
'''

import jieba
import spacy
from collections import Counter
import logging
from pymongo import MongoClient
import re
import matplotlib.pyplot as plt
#统计技术层面
#总体思路 : 对于demand字段直接进行映射后统计词频，对于指纹描述经过jieba分词后再进行映射并统计词频

#设置字体的默认参数避免乱码
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

logging.getLogger("jieba").setLevel(logging.ERROR)      #更改日志等级，使控制台不会输出jieba的非错误红色信息
# nlp = spacy.load("en_core_web_sm") #导入英文分词模型
jieba.initialize()
jieba.load_userdict("txt_file/custom_dict.txt")   #这个文件是自定义的词汇文件，里面出现的词汇jieba不会给他分开
jieba.add_word("c++",883635)

name = str(input("请输入你想要了解哪个方向的技术需求\n"))
client = MongoClient("localhost",27017)
db = client["boss"]
collection = db[name]
search_key = "skill_demand"

mapping_file = "txt_file/mapping.txt"            #指定映射文件



useless_list =[",","/","等","经验",'"',"'",',',' ','，',"+","[","]","技术","计算机相关专业"]


# 自定义词义相近的词映射
def get_mapping() :
    mapping_dict = {}
    with open(mapping_file, mode='r',encoding="utf-8") as file:
        for line in file:  # 映射文件的编写规则是每一行对应一个映射关系
            word, mapping = line.strip().split(':')
            mapping_dict[word.strip()] = mapping.strip()
        return mapping_dict


def read_data(key) :
    skill_list = []
    # text = collection.distinct(key=key)[:100]
    data_list = collection.find({key: {'$exists': True}})
    for data in data_list :
        skill = data[key]
        skill_list.append(skill)
    # print(skill_list)
    print("\n")
    # new_text = ",".join(text)
    # last_text = new_text.replace(","," ")
    return skill_list

def ch_text_handle(text) :
    data = jieba.cut(text)
    tokens = [token for token in data if token.strip()] #去除空字符串
    return str(tokens)

def get_frequency(tokens,mapping_dict) :
    word_counts = Counter()
    for token in tokens:
        # 将词义相近的词映射为同一个词
        mapped_token = mapping_dict.get(token, token)
        word_counts[mapped_token] += 1
    result = word_counts.most_common(10)
    return result     #返回词频最高的三个词

def filter_word(text) :
    tokens = re.findall(r'\w+|[^\w\s]', text.lower())  # 处理标点符号带来的影响
    filtered_text = [token for token in tokens if token not in useless_list]
    # filtered_text = str(filtered_text)
    # filtered_text = re.sub(r"c\+\+", "cpp", filtered_text)
    # filtered_text = re.sub(r'objective-c', 'objc', filtered_text)
    # filtered_text = re.sub(r'c#', 'csharp', filtered_text)
    #filtered_text = filtered_text.replace("'","")
    return filtered_text

def run_output(text) :
    res =ch_text_handle(str(text).lower())
    filter_res = filter_word(res)
    total = len(filter_res)
    mapping_dict = get_mapping()
    frequency = get_frequency(filter_res,mapping_dict)
    print("混合分词结果", filter_res)
    print("混合词频结果", frequency)
    print("\n")
    labels = [item[0] for item in frequency]
    values = [item[1] for item in frequency]
    plt.barh(labels,values)
    percentages = [value / total * 100 for value in values]
    for i, value in enumerate(values):
        percentage = percentages[i]
        plt.text(values[i], i, f'{percentage:.2f}%', ha='center', va='bottom')
    plt.ylabel("技术需求")
    plt.xlabel("技术占比")
    plt.title("Top 10 技术占比")
    plt.tight_layout()
    # 反转y轴显示顺序
    plt.gca().invert_yaxis()
    plt.show()


def main() :
    text = read_data(search_key)
    run_output(text)
if __name__ == '__main__':
    main()



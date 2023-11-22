# -*- coding: UTF-8 -*-
'''
@Project ：ch_cup 
@File    ：apply_data.py
@IDE     ：PyCharm 
@Author  ：温情止于晚风
@Date    ：2023/10/31 16:04 
'''

# import numpy as np
# import pandas as pd
# from collections import Counter
# import unicodedata
# from pymongo import MongoClient
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.tree import DecisionTreeClassifier
#
# client = MongoClient('127.0.0.1',27017)
# db = client['boss']
# collection = db["deep_learning"]
#
# #读取数据库内容
# def read_data(key) :
#     need_key = key
#     data = collection.distinct(key=need_key)[:500]
#     # for demand in data :
#     #     print(demand)
#     print(data)
#     new_data = [item.lower() if isinstance(item,str) else item for item in data]
#     counter = Counter(new_data)
#     most_num = counter.most_common(3)
#     for item in most_num :
#         value = item[0]
#         count = item[1]
#         print(value,count)
# if __name__ == '__main__':
#     read_data("demand")
#

#
# text =["python cnn java c++",
#        "ml dl pytorch tensorflow sql",
#        "c cnn python spark pca",
#        "flume boosting nlp net",
#        "kafka numpy java c++ svm"]
# new_text = ["python"]
# label = [1,0,1,0,0]
#
# vector = CountVectorizer()
# x_bow = vector.fit_transform(text)
# dtc = DecisionTreeClassifier()
# dtc.fit(x_bow,label)
#
# y_bow = vector.transform(new_text)
# predict = dtc.predict(y_bow)
# print(predict)


from collections import Counter
import re

text = "I have cats and dogs. My cat likes to play, but the dogs prefer to sleep."

# 自定义词义相近的词映射
mapping_file = "txt_file/mapping.txt"
mapping_dict = {}
with open(mapping_file, 'r') as file:
    for line in file:                       #映射文件的编写规则是每一行对应一个映射关系
        word, mapping = line.strip().split(':')
        mapping_dict[word.strip()] = mapping.strip()

# 分词
tokens = re.findall(r'\w+|[^\w\s]', text.lower())   #处理标点符号带来的影响

# 统计词频
word_counts = Counter()
for token in tokens:
    # 将词义相近的词映射为同一个词
    mapped_token = mapping_dict.get(token,token)
    word_counts[mapped_token] += 1

# 输出词频
for word, count in word_counts.items():
    print(f"{word}: {count}")
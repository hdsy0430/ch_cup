# -*- coding: UTF-8 -*-
'''
@Project ：ch_cup 
@File    ：data_rules.py
@IDE     ：PyCharm 
@Author  ：温情止于晚风
@Date    ：2023/9/24 14:35 
'''

#关联规则挖掘算法 aprioi 与 fpgrowth

'''import mlxtend
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori,association_rules,fpgrowth
import pandas as pd
# dataset = [["努力","听课","成绩优秀"],
#            ["努力","不听课","成绩优秀"],
#            ["不努力","不听课","成绩不好"],
#            ["努力","听课","成绩不好"],
#            ["努力","成绩优秀"]]
dataset = [["大数据开发","SQL Hadoop Spark Kettle Informatica SPSS Kafka Java"],
           ["大数据讲师","Java Python Scala Spark Flink SQL"],
           ["大数据etl工程师",",MySQL/Oracle/DB2 Kettle/Informatica Python"],
           ["大数据讲师","Java Python Scala Spark Flink SQL"],
           ["大数据开发","Hive Python SQL tableau"],
           ["大数据工程师","数据仓库 ETL 数据挖掘 数据分析 SQL Java Python Scala"],
           ["大数据工程师","Python Java C++ Shell SQL"],
           ["大数据开发","SQL Spark Flink 计算机相关专业 大数据开发经验 数仓建设经验"]]
te = TransactionEncoder()
py_te = te.fit_transform(dataset)
df = pd.DataFrame(py_te,columns=te.columns_)

frequent_sets = apriori(df=df,min_support=0.2,use_colnames=True)    #确定最小支持度
rules = association_rules(frequent_sets,metric="confidence",min_threshold=0.1)  #确定最小置信度
print(" 频繁项集 :")
print(frequent_sets)
print("\n关联规则")
print(rules)
print(rules["confidence"])'''

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori,fpgrowth,association_rules

# dataset = [["bread","milk","apple"],
#             ["bread","milk","banana"],
#             ["milk","water","pear"],
#             ["bread","milk","meat"],
#             ["bread","meat"]]
#
dataset = [
  {
    "demand": ["机器学习", "算法", "深度学习"],
    "job_name": ["深度学习"]
  },
  {
    "demand": ["搜索/推荐", "智能驾驶", "翻译", "Java", "Python", "C/C++", "机器学习算法/工程化经验", "深度学习经验"],
    "job_name": ["深度学习"]
  },
  {
    "demand": ["C++", "Python", "深度学习算法", "视觉图像算法", "PyTorch", "Caffe", "CNN"],
    "job_name": ["深度学习"]
  },
  {
    "demand": ["搜索算法", "搜索/推荐", "广告算法", "自然语言处理", "深度学习算法", "推荐算法"],
    "job_name": ["深度学习"]
  },
  {
    "demand": ["深度学习算法", "TensorFlow", "Caffe", "PyTorch"],
    "job_name": ["深度学习"]
  },
  {
    "demand": ["C/C++", "TensorFlow/PyTorch", "深度学习经验"],
    "job_name": ["深度学习研究专员"]
  },
  {
    "demand": ["深度学习算法", "TensorFlow", "PyTorch", "视觉图像算法", "机器学习算法", "C++", "Python"],
    "job_name": ["深度学习"]
  },
  {
    "demand": ["深度学习算法", "视觉图像算法", "人脸识别", "Python", "TensorFlow", "Caffe", "PyTorch", "C语言"],
    "job_name": ["深度学习"]
  },
  {
    "demand": ["算法", "人工智能", "深度学习"],
    "job_name": ["深度学习"]
  }
]

features = [ d["job_name"] + d["demand"] for d in dataset ]
te = TransactionEncoder()
data = te.fit_transform(features)
# print(data)
df = pd.DataFrame(data,columns=te.columns_)

frequent_sets = apriori(df,min_support=0.4,use_colnames=True)
rules = association_rules(frequent_sets,metric="confidence",min_threshold=0.6)
print("频繁项集 :")
print(frequent_sets)
print("\n关联规则")
print(rules)
print(rules["confidence"])
rules_list = list(rules)
for index,rule in rules.iterrows():
  confidence = rule["confidence"]
  if confidence >= 0.8 :
    print("you can learn the below knowledge")
    antecedents = str(rule["antecedents"]).replace("frozenset({'","").replace("'})","").replace("', '","").strip()
    consequents = str(rule["consequents"]).replace("frozenset({'","").replace("'})","").replace("', '","").strip()
    print(antecedents,consequents)
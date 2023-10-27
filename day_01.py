# -*- coding: UTF-8 -*-
'''
@Project ：ch_cup 
@File    ：day_01.py
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

dataset = [["bread","milk","apple"],
            ["bread","milk","banana"],
            ["milk","water","pear"],
            ["bread","milk","meat"],
            ["bread","meat"]]

te = TransactionEncoder()
data = te.fit_transform(dataset)
df = pd.DataFrame(data,columns=te.columns_)

frequent_sets = apriori(df,min_support=0.4,use_colnames=True)
rules = association_rules(frequent_sets,metric="confidence",min_threshold=0.6)
print("频繁项集 :")
print(frequent_sets)
print("\n关联规则")
print(rules)
print(rules["confidence"])
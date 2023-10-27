# -*- coding: UTF-8 -*-
'''
@Project ：ch_cup 
@File    ：day_02.py
@IDE     ：PyCharm 
@Author  ：温情止于晚风
@Date    ：2023/9/24 20:34 
'''
#决策树
# import sklearn
# from sklearn import tree
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction import DictVectorizer
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
#
# filename = "train.csv"
# data = pd.read_csv(filename)
# #print(data.columns)    #获取所有特征名
# features = data[["Pclass","Age","Sex"]]
# feature_copy = features.copy()       #获取副本避免不必要的麻烦
# #年龄有缺失值要处理
# feature_copy["Age"].fillna(feature_copy["Age"].mean(),inplace=True)  #缺失值用平均值代替
#
# data_target = data["Survived"]       #目标特征
#
# #特征抽取
# dvc = DictVectorizer()
# feature_copy = feature_copy.to_dict(orient="records")  #将每一行数据转换为一个字典，然后将所有字典组成一个列表。这样的数据结构更适合用于特征向量化或者模型的输入。
# data_features = dvc.fit_transform(feature_copy)
#
# x_train,x_test,y_train,y_test = train_test_split(data_features,data_target,test_size=0.2)#第一个数组是特征矩阵，第二个数组是目标变量
#
# dtc = DecisionTreeClassifier(criterion="entropy")
# dtc.fit(x_train,y_train)       #fit只能接受数值类型
# plt.figure(figsize=(20,12))
# tree.plot_tree(dtc)
# accuracy = dtc.score(x_test,y_test)
# print(accuracy)
# plt.show()

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction import DictVectorizer
import xgboost
from xgboost.sklearn import XGBClassifier
import pandas as pd

filename = "train.csv"
data = pd.read_csv(filename)
features = data[["Pclass","Age","Sex"]]
copy = features.copy()
copy["Age"].fillna(copy["Age"].mean(),inplace=True)
target = data["Survived"]

dvt = DictVectorizer()
copy = copy.to_dict(orient="records")
data_features = dvt.fit_transform(copy)

x_train,x_test,y_train,y_test = train_test_split(data_features,target,test_size=0.2)
xgb = XGBClassifier(max_depth=7,
    learning_rate=0.1,
    n_estimators=100,
    objective='binary:logistic',
    random_state=42)

xgb.fit(x_train,y_train)
y_pred = xgb.predict(x_test)
accuracy = accuracy_score(y_test,y_pred)
print(accuracy)


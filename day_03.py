# -*- coding: UTF-8 -*-
'''
@Project ：ch_cup 
@File    ：day_03.py
@IDE     ：PyCharm 
@Author  ：温情止于晚风
@Date    ：2023/9/25 16:02 
'''

#决策树与随机森林       想做数据预处理的时候卡住了
'''import pandas as pd
import sklearn
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split ,cross_val_score
from sklearn.feature_extraction import DictVectorizer
import matplotlib.pyplot as plt

filename = "train.csv"
data = pd.read_csv(filename)
#print(data.columns)
features = data[["Pclass","Age","Sex"]]
features_copy = features.copy()
features_copy.head()
features_copy["Age"].fillna(features_copy["Age"].mean(),inplace=True)
data_target = data["Survived"]

dcv = DictVectorizer()
features_copy = features_copy.to_dict(orient="records")
data_features = dcv.fit_transform(features_copy)

x_train,x_test,y_train,y_test = train_test_split(data_features,data_target,test_size=0.2)
dtc = DecisionTreeClassifier(criterion="entropy")
rfc = RandomForestClassifier(n_estimators=25)   #指定森林中树的数量为25
rfc_s = cross_val_score(rfc,data_features,data_target,cv=10)    #返回一个评分值
dtc_s = cross_val_score(dtc,data_features,data_target,cv=10)
dtc.fit(x_train,y_train)
rfc.fit(x_train,y_train)
plt.plot(range(1,11),rfc_s,label="Random forest",color="red")
plt.plot(range(1,11),dtc_s,label="Decision tree",color="green")
plt.title("decide process")
plt.legend(loc='upper left')
plt.show()
print(dtc.score(x_test,y_test))
print(rfc.score(x_test,y_test))'''

import sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


filename = "train.csv"
data = pd.read_csv(filename)
#print(data.columns)
features = data[["Pclass","Age","Sex"]]
features_copy = features.copy()
features_copy.head()
features_copy["Age"].fillna(features_copy["Age"].mean(),inplace=True)
data_target = data["Survived"]

test_data = pd.read_csv("test.csv")
#print(test_data.columns)
test_features = test_data[["Pclass","Age","Sex"]]
test_features_copy = test_features.copy()
test_features_copy["Age"].fillna(test_features_copy["Age"].mean(),inplace=True)
# test_target = test_data['Survived']



dcv = DictVectorizer()
features_copy = features_copy.to_dict(orient="records")
data_features = dcv.fit_transform(features_copy)
test_features_copy = test_features_copy.to_dict(orient="records")
test_feature = dcv.fit_transform(test_features_copy)

rfc = RandomForestClassifier(n_estimators=30)
dct = DecisionTreeClassifier(criterion="entropy")
x_train,x_test,y_train,y_test = train_test_split(data_features,data_target,test_size=0.2)
rfc_s = cross_val_score(rfc,data_features,data_target,cv=10)
dct_s = cross_val_score(dct,data_features,data_target,cv=10)
rfc.fit(data_features,data_target)
dct.fit(data_features,data_target)
plt.plot(range(1,11),rfc_s,label="Random Forest",color="red")
plt.plot(range(1,11),dct_s,label="Decision Tree",color="green")
plt.legend(loc = "upper left")
plt.title("decision process")
plt.show()
# print(dct.score(x_test,y_test))
# print(rfc.score(x_test,y_test))
test_pred_rfc = rfc.predict(test_feature)
test_pred_dct = dct.predict(test_feature)
accuracy_rfc = accuracy_score(test_pred_rfc,test_feature)
accuracy_dtc = accuracy_score(test_pred_dct,test_feature)
print(accuracy_rfc,accuracy_dtc)



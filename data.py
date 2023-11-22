# import sklearn
# import pandas as pd
# from sklearn import tree
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from sklearn.preprocessing import StandardScaler
# from sklearn.feature_extraction import DictVectorizer
# import numpy as np
#
# filename = "csv_file/tennis.csv"
# data = pd.read_csv(filename)
# #print(data.columns)
# data_features = data[["Outlook","Temperature","Humidity","Windy"]]
# data_target = data["PlayTennis"]
#
# dvt = DictVectorizer()
# data_feature = data_features.to_dict(orient="records")
# data_features = dvt.fit_transform(data_feature)
#
# dtc = DecisionTreeClassifier(criterion="gini")
# x_train,x_test,y_train,y_test = train_test_split(data_features,data_target,test_size=0.2)
# dtc.fit(x_train,y_train)
# y_pred = dtc.predict(x_test)
# accuracy = accuracy_score(y_test,y_pred)
# print(accuracy)


import os
import jieba

# 获取jieba库的自带词典路径
dict_path = os.path.join(os.path.dirname(jieba.__file__), 'dict.txt')

# 打开词典文件并查看内容
with open(dict_path, 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)
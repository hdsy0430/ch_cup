# -*- coding: UTF-8 -*-
'''
@Project ：ch_cup 
@File    ：day_05.py
@IDE     ：PyCharm 
@Author  ：温情止于晚风
@Date    ：2023/10/14 15:28 
'''

#PCA SVM

import sklearn
from sklearn.svm import SVC
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.metrics import accuracy_score

import matplotlib.pyplot as plt

minist = load_digits()
x , y = minist.data ,minist.target
# print(x.shape)
# print(len(set(y)))
scaler = StandardScaler()
scaler.fit_transform(x)

pca = PCA(n_components=0.95)
x_pca = pca.fit_transform(x)

x_train,x_test,y_tran,y_test = train_test_split(x_pca,y,test_size=0.2,random_state=42)

svm = SVC(C=0.5)
svm.fit(x_train,y_tran)
y_pred = svm.predict(x_test)
accuracy = accuracy_score(y_test,y_pred)
svm_s = cross_val_score(svm,x_pca,y,cv=10)
plt.title(" svm predict")
plt.plot(range(1,11),svm_s,color="red",label="svm")
plt.legend(loc="upper left")
plt.show()
print(accuracy)


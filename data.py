import sklearn
import pandas as pd
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction import DictVectorizer
import numpy as np

filename = "tennis.csv"
data = pd.read_csv(filename)
#print(data.columns)
data_features = data[["Outlook","Temperature","Humidity","Windy"]]
data_target = data["PlayTennis"]

dvt = DictVectorizer()
data_feature = data_features.to_dict(orient="records")
data_features = dvt.fit_transform(data_feature)

dtc = DecisionTreeClassifier(criterion="gini")
x_train,x_test,y_train,y_test = train_test_split(data_features,data_target,test_size=0.2)
dtc.fit(x_train,y_train)
y_pred = dtc.predict(x_test)
accuracy = accuracy_score(y_test,y_pred)
print(accuracy)

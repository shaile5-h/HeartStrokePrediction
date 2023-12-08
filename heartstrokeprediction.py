# -*- coding: utf-8 -*-
"""HeartStrokePrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xW-B2pStyNp_tmFxsrmCweCH2q3FvWAr
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv('/content/healthcare-dataset-stroke-data.csv')
df.head()

df.shape

df.isnull().sum()

import math


def average(data_,feature_):
    sum_=0
    count=0
    #feature_='bmi'
    for c in data_[feature_]:
        if(not math.isnan(c)):
            sum_=sum_+c
            count+=1
    return sum_ /count

def fillna(data,feature):
    for i in range(len(data[feature])):
        if(math.isnan(data[feature][i])) :
            data[feature][i]=average(data,feature)


fillna(df,'bmi')

print(df.isnull().sum())

import seaborn as sns
plt.figure(figsize=(15,10))
sns.heatmap(df.corr(),annot=True,fmt='.2')

count=df['stroke'].value_counts()
label=['0','1']
plt.figure(figsize=(13,9))
plt.pie(count,labels=label)
print(count)

# drop the id as it is not correlated feature
df=df.drop(['id'],axis=1)
df.isnull().sum()

from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
for col in df.columns:
    df[col] = le.fit_transform(df[col])

df.head()

from sklearn.model_selection  import train_test_split
y = df.iloc[:,-1]
X = df.iloc[:,:-1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

# Handling skewed data
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
smote = SMOTE(sampling_strategy='auto', random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

print(pd.Series(y_resampled).value_counts())

#Decision tree classifier

from sklearn.tree import DecisionTreeClassifier

classifier= DecisionTreeClassifier(criterion='entropy', random_state=0)
classifier.fit(X_resampled, y_resampled)
y_pred1=classifier.predict(X_test)

accuracy1 = accuracy_score(y_test, y_pred1)
confusion1 = confusion_matrix(y_test, y_pred1)
classification_rep1 = classification_report(y_test, y_pred1)

print("Accuracy:", accuracy1)
print("Confusion Matrix:\n", confusion1)
print("Classification Report:\n", classification_rep1)

# XGBoost
import xgboost as xgb
clf = xgb.XGBClassifier(objective='binary:logistic', eval_metric='logloss')
clf.fit(X_resampled, y_resampled)
y_pred2 = clf.predict(X_test)

accuracy2 = accuracy_score(y_test, y_pred2)
confusion2 = confusion_matrix(y_test, y_pred2)
classification_rep2 = classification_report(y_test, y_pred2)

print("Accuracy:", accuracy2)
print("Confusion Matrix:\n", confusion2)
print("Classification Report:\n", classification_rep2)

# KNN
from sklearn.neighbors import KNeighborsClassifier
knn=KNeighborsClassifier()
knn.fit(X_resampled, y_resampled)
y_pred3 = clf.predict(X_test)

accuracy3 = accuracy_score(y_test, y_pred3)
confusion3 = confusion_matrix(y_test, y_pred3)
classification_rep3 = classification_report(y_test, y_pred3)

print("Accuracy:", accuracy3)
print("Confusion Matrix:\n", confusion3)
print("Classification Report:\n", classification_rep3)

# Support vector machine
from sklearn.svm import SVC
svm_classifier = SVC(kernel='rbf', C=2, gamma='scale')
svm_classifier.fit(X_resampled, y_resampled)
y_pred4 = svm_classifier.predict(X_test)

accuracy4 = accuracy_score(y_test, y_pred4)
confusion4 = confusion_matrix(y_test, y_pred4)
classification_rep4 = classification_report(y_test, y_pred4)

print("Accuracy:", accuracy4)
print("Confusion Matrix:\n", confusion4)
print("Classification Report:\n", classification_rep4)
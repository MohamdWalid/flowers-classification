# -*- coding: utf-8 -*-
"""pattern_Assignment3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mEi7OXPt4B_iF5FwqYNyu2hnvl-umq-L
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets

iris = datasets.load_iris()
input = iris.data
output = iris.target.reshape(-1,1)

print(output)

print(input)

data = np.concatenate([input,output],axis=1)

print(data)

np.random.shuffle(data)

data = pd.DataFrame(data , columns=['SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm','Species'])

print(data)
# 0 for Iris-setosa
# 1 for Iris-versicolor
# 2 for Iris-virginica

colors = ['pink','yellow','gray']
label = ['Iris-setosa' , 'Iris-versicolor', 'Iris-virginica']
for i in range(0,3):
  plt.scatter(data['SepalLengthCm'].loc[data['Species'] == i],data['SepalWidthCm'].loc[data['Species'] == i] , c = colors[i] , label = label[i])

plt.xlabel('SepalLengthCm')
plt.ylabel('SepalWidthCm')
plt.legend()

colors = ['pink','yellow','gray']
label = ['Iris-setosa' , 'Iris-versicolor', 'Iris-virginica']
for i in range(0,3):
  plt.scatter(data['PetalLengthCm'].loc[data['Species'] == i],data['PetalWidthCm'].loc[data['Species'] == i] , c = colors[i] , label = label[i])

plt.xlabel('PetalLengthCm')
plt.ylabel('PetalWidthCm')
plt.legend()

train = data.iloc[:120,:]
test =  data.iloc[120:,:]

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split
LDA = LinearDiscriminantAnalysis()
LDA.fit(train.iloc[:,:-1],train.iloc[:,-1])
print(LDA.score(test.iloc[:,:-1],test.iloc[:,-1]))

def train_function(label):
   data = train.copy()
   data['Species'] = train['Species'].map(lambda x : 1 if x ==label else -1)
   x = np.array(data.iloc[:,:-1])
   y = np.array(data.iloc[:,-1:])
   x = np.concatenate([x,np.ones((x.shape[0],1))] , axis = 1)
   W = (np.linalg.inv((x*y).T.dot(x*y))).dot((x*y).T.dot(y*y))
   return W

save_weights = []
save_weights.append(train_function(0)) # if > 0 then Iris-setosa
save_weights.append(train_function(2)) # if > 0 then Iris-virginica
save_weights.append(train_function(1))

data = test.copy()
x = np.array(data.iloc[:,:-1])
y = np.array(data.iloc[:,-1:])
ones = np.ones((x.shape[0],1))
x = np.concatenate([x,ones] , axis = 1) 
label = []
for i in range(0,30):
  if(x[i:i+1][:].dot(save_weights[0])>0):
     if(x[i:i+1][:].dot(save_weights[1])>0):
         label.append(3)
     else:
         label.append(0)

  else:
     if(x[i:i+1][:].dot(save_weights[1])>0):
         label.append(2)
     else:
         label.append(1)

z = np.array(label).reshape(-1,1)

print(np.count_nonzero((z==y))/30)
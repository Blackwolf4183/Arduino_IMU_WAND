import pandas as pd
import os
from skimage.transform import resize
from skimage.io import imread
import numpy as np
import matplotlib.pyplot as plt

from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import pickle




Categories=['lumos','revelio','leviosa']
flat_data_arr=[] #input array
target_arr=[] #output array
datadir='./dataset/' 



def loadDataset():
    #path which contains all the categories of images
    for i in Categories:
        
        print(f'loading... category : {i}')
        path=os.path.join(datadir,i)
        for img in os.listdir(path):
            img_array=imread(os.path.join(path,img))
            #img_resized=resize(img_array,(150,150,3))
            flat_data_arr.append(img_array.flatten())
            target_arr.append(Categories.index(i))
        print(f'loaded category:{i} successfully')
    flat_data=np.array(flat_data_arr)
    target=np.array(target_arr)
    df=pd.DataFrame(flat_data) #dataframe
    df['Target']=target
    x=df.iloc[:,:-1] #input data 
    y=df.iloc[:,-1] #output data

    return x,y


def generateModel(x,y):
    param_grid={'C':[0.1,1,10,100],'gamma':[0.0001,0.001,0.1,1],'kernel':['rbf','poly']}
    svc=svm.SVC(probability=True)
    model=GridSearchCV(svc,param_grid)
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.20,random_state=77,stratify=y)
    print('Splitted Successfully')
    model.fit(x_train,y_train)
    print('The Model is trained well with the given images')
    # model.best_params_ contains the best parameters obtained from GridSearchCV
    return model, x_train, y_train

def testModel(model, x_test, y_test):
    y_pred=model.predict(x_test)
    print("The predicted Data is :")
    print(y_pred)
    print("The actual data is:")
    print(np.array(y_test))
    print(f"The model is {accuracy_score(y_pred,y_test)*100}% accurate")
    

def makePredictionWithImage(imgPath, model):
    testing_path = './test/'
    testImage = imread(os.path.join(testing_path,'lumos2.jpeg'))
    l=[testImage.flatten()]
    probability=model.predict_proba(l)

    for ind,val in enumerate(Categories):
        print(f'{val} = {probability[0][ind]*100}%')

    print("The predicted image is : "+Categories[model.predict(l)[0]])

def makePrediction(imgArr, model):
    l=[imgArr.flatten()]
    probability=model.predict_proba(l)

    for ind,val in enumerate(Categories):
        print(f'{val} = {probability[0][ind]*100}%')

    predictedIndex = model.predict(l)[0]
    print("The predicted image is : "+Categories[model.predict(l)[0]])
    return Categories, probability, predictedIndex


def saveModel(model, filename):
    pickle.dump(model, open(filename, "wb"))

def loadModel(filename):
    loaded_model = pickle.load(open(filename, "rb"))
    return loaded_model


#TODO: test again weird probabilities on linux
""" x,y = loadDataset()
model,x_train,y_train = generateModel(x,y)
testModel(model,x_train,y_train) """

""" model = loadModel("svm.pickle")
makePrediction("asd",model) """
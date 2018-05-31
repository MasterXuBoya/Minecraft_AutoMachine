import numpy as np
from PIL import Image
import cv2
import time
import util
from configure import config
from sklearn.externals import joblib
from sklearn import linear_model

if __name__=='__main__':
    Num=5
    x=[]
    y=[]
    for i in range(Num):
        for j in range(9):
            for k in range(9):
                x_single=cv2.imread(r'Image_cell/%s_%s_%s.png'%(i+1,j,k))
                print(x_single.shape)
                x_single=np.array(x_single)
                x_single=x_single.reshape(-1)
                x.append(x_single)
        y_single=np.load(r'Label/label_%s.npy'%(i+1))
        y_single=y_single.reshape(1,-1)
        y.append(y_single)
    x=np.array(x)
    y=np.array(y).reshape(-1)
    print(x.shape)
    print(y.shape)
    print(y)

    clf = linear_model.LogisticRegression(C=1e5)
    clf.fit(x,y)
    joblib.dump(clf,'linear_model.pkl')



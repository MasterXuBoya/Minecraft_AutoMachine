import numpy as np
from PIL import Image
import cv2
import time
import util
from configure import config
from pymouse import PyMouse
from sklearn.externals import joblib
import sys

if __name__=='__main__':

    row = config['grid_num']
    column = config['grid_num']
    grid = config['grid_w']
    count=10
    data = np.full((9, 9), 0)

    clf = joblib.load('linear_model.pkl')


    while True:
        print("********************%s****************************"%(count))
        t1=time.time()
        filename=r'Image/%s.png'%(count)
        img=util.shotByWinAPI(filename)
        t2=time.time()
        print("Screen spend time :%s s"%(t2-t1))
        print(img.shape)
        Image.fromarray(img.astype('uint8')).show()

        for i in range(row):
            for j in range(column):
                x=j*grid
                y=i*grid
                cell=img[y:y+grid,x:x+grid]
                #Image.fromarray(cell.astype('uint8')).show()

                cell = cv2.resize(cell, (31, 31), interpolation=cv2.INTER_CUBIC)
                cell=cell[4:27,4:27]
                #Image.fromarray(cell.astype('uint8')).show()

                #cv2.imwrite(r'Image_cell/%s_%s_%s.png'%(count,i,j),cell)
                cell=np.array(cell).reshape(-1)
                pred_cell = clf.predict([cell])
                #print(pred_cell)
                data[i,j]=pred_cell[0]
        print(data)



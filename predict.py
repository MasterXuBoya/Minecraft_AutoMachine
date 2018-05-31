import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import time
import util
from configure import config
from scipy.stats import mode
from pymouse import PyMouse
from PIL import ImageGrab
from sklearn.externals import joblib



def load_train():
    train = np.full((6, grid * grid*3), 1)
    str_train=['1','2','3','empty','flag','unclicked']
    for i in range(6):
        train_path=r'Mode/'+str_train[i]+'.npy'
        cell=np.load(train_path)
        #Image.fromarray(cell.astype('uint8')).show()
        #print(mode(cell))
        train[i] = cell.reshape(1, -1)
    return train

def getCell(i,j):
    x = j * grid
    y = i * grid
    print(x, y)
    cell = img[y:y + grid, x:x + grid]
    return cell



if __name__=='__main__':

    #im = ImageGrab.grab((54,100,350,279))
    #im.save(r'haha.jpg')

    row = config['grid_num']
    column = config['grid_num']
    grid = config['grid_w']
    count=10
    data=np.full((9,9),0)
    clf = joblib.load('linear_model.pkl')

    while True:
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
                cell=cell[4:27,4:27]
                #Image.fromarray(cell.astype('uint8')).show()
                #cv2.imwrite(r'Image_cell/%s_%s_%s.png'%(count,i,j),cell)

                cell=np.array(cell).reshape(-1)
                pred_cell = clf.predict([cell])
                #print(pred_cell)
                data[i,j]=pred_cell[0]
        print(data)











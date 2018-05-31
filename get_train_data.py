import numpy as np
from PIL import Image
import cv2
import time
import util
from configure import config

if __name__=='__main__':

    row = config['grid_num']
    column = config['grid_num']
    grid = config['grid_w']
    count=5
    data=np.full((9,9),0)
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
            cv2.imwrite(r'Image_cell/%s_%s_%s.png'%(count,i,j),cell)

    label=np.full((9,9),0)
    i=0
    file=open(r'D:/test.txt').readlines()
    for line in file:
        tmp=line.strip().split(' ')
        #print(tmp)
        label[i]=tmp
        i+=1
    print(label)
    np.save(r'Label/label_%s.npy' % (count),label)


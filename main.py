import numpy as np
from PIL import Image
import cv2
import time
import util
from configure import config
from pymouse import PyMouse
from sklearn.externals import joblib
import sys

m = PyMouse()
data = np.full((9, 9), 0)
data_pre=np.full((9,9),0)
flag_num=False
dx = [-1, -1, -1, 0, 0, 1, 1, 1]
dy = [-1, 0, 1, -1, 1, -1, 0, 1]

def get_location(x,y):
    x_postion=config['projection_x']+config['grid_w']*(y+0.5)
    y_position=config['projection_y']+config['grid_w']*(x+0.5)
    return int(x_postion),int(y_position)

def add_flag(x,y):
    global flag_num
    global data
    surrunding_num=0
    for i in range(8):
        xx=x+dx[i]
        yy=y+dy[i]
        if xx>=0 and xx<9 and yy>=0 and yy<9 and (data[xx,yy]==5 or data[xx,yy]==4):
            surrunding_num+=1
    #print("the current location is :",x,y)
    #print('surrounding num is :',surrunding_num)
    if surrunding_num == data[x,y] + 1:
        for i in range(8):
            xx = x + dx[i]
            yy = y + dy[i]
            if xx>=0 and xx<9 and yy>=0 and yy<9 and data[xx,yy]==5:
                flag_num = True
                x_positon,y_position=get_location(xx,yy)
                print("the current location is :", xx, yy)
                #print(x_positon,y_position)
                m.click(x_positon,y_position,2)
                data[xx,yy]=4
                time.sleep(0.001)


if __name__=='__main__':

    row = config['grid_num']
    column = config['grid_num']
    grid = config['grid_w']
    count=10

    clf = joblib.load('linear_model.pkl')
    m.click(104, 90, 1)
    sum_img_pre=0

    while True:
        print("********************%s****************************"%(count))
        t1=time.time()
        filename=r'Image/%s.png'%(count)
        img=util.shotByWinAPI(filename)
        t2=time.time()
        print("Screen spend time :%s s"%(t2-t1))
        print(img.shape)
        #Image.fromarray(img.astype('uint8')).show()

        '''
        sum_img=np.sum(np.array(img))
        print(sum_img_pre,sum_img)
        if sum_img_pre >= sum_img-2000 and sum_img_pre <= sum_img + 2000:
            print("********************************重复截图")
            continue
        sum_img_pre=sum_img
        '''
        for i in range(row):
            for j in range(column):
                x=j*grid
                y=i*grid
                cell=img[y:y+grid,x:x+grid]
                cell = cv2.resize(cell, (31, 31), interpolation=cv2.INTER_CUBIC)
                cell=cell[4:27,4:27]
                #Image.fromarray(cell.astype('uint8')).show()
                #cv2.imwrite(r'Image_cell/%s_%s_%s.png'%(count,i,j),cell)

                cell=np.array(cell).reshape(-1)
                pred_cell = clf.predict([cell])
                #print(pred_cell)
                data[i,j]=pred_cell[0]
        print(data)

        print(data_pre)
        if np.sum(data == data_pre) == 81:  # 截图重复
            print("********************************重复截图")
            #time.sleep(0.5)
            #continue
        data_pre = data.copy()
        #***************************************************************
        flag_num = False
        unclicked_num=0
        for i in range(9):#标注flag
            for j in range(9):
                if data[i,j]<3:#标有数字
                    add_flag(i,j)

        for i in range(9):#双击
            for j in range(9):
                if data[i,j]<3:
                    num_cell_flag=0
                    num_cell_unclicked=0
                    for k in range(8):
                        xx = i + dx[k]
                        yy = j + dy[k]
                        if xx >= 0 and xx < 9 and yy >= 0 and yy < 9 :
                            if data[xx,yy] == 4:
                                num_cell_flag+=1
                            if data[xx,yy] == 4 or data[xx,yy]==5:
                                num_cell_unclicked+=1
                    print(num_cell_flag,num_cell_unclicked)
                    if num_cell_flag==data[i,j]+1 and num_cell_flag<num_cell_unclicked:
                        x_position,y_positon=get_location(i,j)
                        print(i,j)
                        m.click(x_position,y_positon,1|2)
                        flag_num=True
                    time.sleep(0.001)
        print(flag_num)
        if flag_num==False:#没找一个可以标flag的
            num_global_5=np.sum(data==5)
            random_num=np.random.randint(num_global_5)
            s=0
            for i in range(row):
                for j in range(row):
                    if data[i,j]==5:
                        if s==random_num:
                            x_position, y_positon = get_location(i, j)
                            print("random location is :",i, j)
                            m.click(x_position, y_positon, 1)
                        s += 1

        if ~(data==5).any():
            print("Game Finished!")
            sys.exit(0)
        #time.sleep(1)
        if count==35:
            sys.exit(0)
        count+=1

















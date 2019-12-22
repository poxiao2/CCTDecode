# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 20:56:18 2019

@author: 34086
"""


#-*- coding: UTF-8 -*-  

import numpy as np

import os

from PIL import Image

from PIL import ImageDraw


#绘制CCT图像的函数，n为等分数 
def DrawCCT(N,size,CCT_list):
    
    #单位角度
    unit_angle=360/N
    
    #计算CCT序列代表的最小值
    CCT_value=B2I(CCT_list,N)
    
    #存放CCT图像的路径
    CCT_PATH='CCT_IMG/'
    
    #判断路径是否存在，不存在就新建文件夹
    if_dir_exists=os.path.exists(CCT_PATH)
    if not if_dir_exists:
        os.makedirs(CCT_PATH)
    
    #得到文件名
    file_name=str(CCT_value)+'.png'
    
    #得到文件路径
    file_path=CCT_PATH+file_name
    
    if_file_exists=os.path.exists(file_path)
    if not if_file_exists:
        
        print(CCT_list)
        print(CCT_value)
        
        #生成深黑色绘图画布
        CCT_img_array = np.ndarray((size, size, 3), np.uint8)

        CCT_img_array[:, :, 0] = 0
        CCT_img_array[:, :, 1] = 0
        CCT_img_array[:, :, 2] = 0

        image = Image.fromarray(CCT_img_array)

        #创建绘制对象
        draw = ImageDraw.Draw(image)

        #-----------绘制CCT--------------#
        #尺寸：  1:2:2:20
    
       
    
        #根据CCT数组循环绘制扇形
        for i in range(0,N):
            if CCT_list[i]==1:
                draw.pieslice((0.125*size,0.125*size,0.875*size,0.875*size),i*unit_angle,(i+1)*unit_angle,fill='white')
        
        
        #绘制黑色内圆
        draw.ellipse((0.25*size, 0.25*size, 0.75*size, 0.75*size), 'black', 'black')
        
         #绘制白色内圆
        draw.ellipse((0.375*size, 0.375*size, 0.625*size, 0.625*size), 'white', 'white')
    
        
        #保存CCT图片
        image.save(file_path)
        #image.show()

    return

def CCT_table(N,size):
    
    max_value=2**N
    
    CCT_list=[]
    
    for i in range(0,max_value):
        CCT_list=I2B(i,N)
        DrawCCT(N,size,CCT_list)
        
    return

#将整数转换为2进制list的函数
def I2B(value,N):
    #指定list的长度
    array=[' ']*N
    
    for i in range(0,N):
        if value>0:
            array[i]=value%2
            #python中的整除，向下取整
            value=value//2
        else:
            array[i]=0
    
    return array

#将二进制list转换为最小整数的函数
def B2I(array,N):
    min_value=10000
    temp=0
    for i in range(0,N):
        temp=0
        for j in range(0,N):
            if array[j]==1:
                temp=temp+2**j
        if temp<min_value:
            min_value=temp
        array=MoveBit(array,1)
    
    for i in range(0,N):
        temp=0
        for j in range(0,N):
            if array[j]==1:
                temp=temp+2**j
        if temp==min_value:
            break
        array=MoveBit(array,1)
    return min_value

#将list向左移位函数               
def MoveBit(lst, k):
    temp = lst[:]
    for i in range(k):
        temp.append(temp.pop(0))
    return temp

#DrawCCT(8,500,[0,0,0,0,0,0,1,1])
if __name__=='__main__':
    CCT_table(12,2500)
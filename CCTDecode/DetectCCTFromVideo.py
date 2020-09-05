# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 18:47:25 2019

@author: 23872
"""

import cv2
import numpy as np
import argparse
from CCTDecodeRelease import *
import sys

def CallCamera(N,R,color='white'):
    #########图像读取部分
#    cap=cv2.VideoCapture('2.wmv') #调用目录下的视频
    cap=cv2.VideoCapture(0)  #调用摄像头‘0’一般是打开电脑自带摄像头，‘1’是打开外部摄像头（只有一个摄像头的情况）
    #显示图像
    while True: 
        ret,frame=cap.read()#读取图像(frame就是读取的视频帧，对frame处理就是对整个视频的处理)
        #######例如将图像灰度化处理，
#        img=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)#转灰度
        code_table,img=CCT_extract(frame,N,R,color)
        cv2.imshow("img",img)
#        ########图像不处理的情况
#        cv2.imshow("frame",frame)    
     
        input=cv2.waitKey(20)
        if input==ord('q'):#如过输入的是q就break，结束图像显示，鼠标点击视频画面输入字符
            break
        
    cap.release()#释放摄像头
    cv2.destroyAllWindows()#销毁窗口
    
#分割命令行参数的函数
def parse_args():
    parser = argparse.ArgumentParser(description='Detect and Decode the CCT from video.')

    parser.add_argument('--bit_n', dest='bit_n',
                        help='CCT bit number',
                        default=12, type=int)
    parser.add_argument('--threshold', dest='threshold',
                        help='threshold for contour filter, which between 0 and 1',
                        default=0.85, type=float)
    parser.add_argument('--color', dest='color',
                        help='the color of CCT mark(white over black / black over white)',
                        default='white', type=str)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args       
     
if __name__=='__main__':
    args = parse_args()
    CallCamera(args.bit_n,args.threshold,args.color)
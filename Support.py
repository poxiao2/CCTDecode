# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 15:33:39 2019

@author: 34086
"""

import os
import numpy as np
import math
import re
import cv2

#全局变量

#读取照片xml文件提取照片参数的函数
"""
返回值xml为3*3的参数矩阵
第一行三个参数分别为内方位元素：x0,y0,f
第二行三个参数分别为摄影中心绝对坐标：Xs,Ys,Zs
第三行三个参数分别为相片的三个姿态角：p,w,k
"""
def ReadXmlFile(xml_filepath=''):
    xml=np.zeros((3,3)) #创建一个3*3的零矩阵
    fo=open(xml_filepath,'r')
    lines=fo.readlines()
    for line in lines:
        str1=line.split(':') 
        str2=str1[1].split('=')
        if str2[0]=='GpsLatitude ':
            xml[1][0]=float(str2[1])
        if str2[0]=='GpsLongtitude ':
            xml[1][1]=float(str2[1])
        if str2[0]=='AbsoluteAltitude ':
            xml[1][2]=float(str2[1])
        if str2[0]=='CalibratedOpticalCenterX ':
            xml[0][0]=float(str2[1])
        if str2[0]=='CalibratedOpticalCenterY ':
            xml[0][1]=float(str2[1])
        if str2[0]=='CalibratedFocalLength ':
            xml[0][2]=float(str2[1])
            
        if str2[0]=='GimbalPitchDegree ':    
            xml[2][0]=-float(str2[1])
        if str2[0]=='GimbalRollDegree ':
            xml[2][1]=float(str2[1])
        if str2[0]=='GimbalYawDegree ':
            xml[2][2]=float(str2[1])
            
#        if str2[0]=='FlightPitchDegree ':    
#            xml[2][0]=xml[2][0]+float(str2[1])+90
#        if str2[0]=='FlightRollDegree ':
#            xml[2][1]=xml[2][1]+float(str2[1])

       
    
    fo.close()
            
    #[1][0],xml[1][1],xml[1][2]=BLH2XYZ(xml[1][0],xml[1][1],xml[1][2])
    xml[2][0]=xml[2][0]*math.pi/180
    xml[2][1]=xml[2][1]*math.pi/180
    xml[2][2]=xml[2][2]*math.pi/180    

    return xml

#根据照片参数和物方点坐标通过共线方程计算像点坐标的函数
#输入值为xml参数矩阵和物方点XYZ坐标，输出为对应的像点坐标
def CLE(xml,A_XYZ):
    
    #内方位元素
    x0=xml[0,0]
    y0=xml[0,1]
    f=xml[0,2]
    
    #外方位元素
    Xs,Ys=LatLon2XY(xml[1,0], xml[1,1])
    Zs=xml[1,2]   
    p=xml[2,0]
    w=xml[2,1]
    k=xml[2,2]
    
    #物方点坐标
    Xa=A_XYZ[0]
    Ya=A_XYZ[1]
    Za=A_XYZ[2]
        
    #计算旋转矩阵
    sinp=math.sin(p*math.pi/180)
    sinw=math.sin(w*math.pi/180)
    sink=math.sin(k*math.pi/180)
    cosp=math.cos(p*math.pi/180)
    cosw=math.cos(w*math.pi/180)
    cosk=math.cos(k*math.pi/180)

    a1=cosp*cosk-sinp*sinw*sink
    a2=cosp*sink+sinp*sinw*cosk
    a3=-sinp*cosw
    
    b1=-cosw*sink
    b2=cosw*cosk
    b3=sinw
    
    c1=sinp*cosk+cosp*sinw*sink
    c2=sinp*sink-cosp*sinw*cosk
    c3=cosp*cosw
    
    #根据共线方程计算像点坐标
    x=x0-f*(a1*(Xa-Xs)+b1*(Ya-Ys)+c1*(Za-Zs))/(a3*(Xa-Xs)+b3*(Ya-Ys)+c3*(Za-Zs))
    y=y0-f*(a2*(Xa-Xs)+b2*(Ya-Ys)+c2*(Za-Zs))/(a3*(Xa-Xs)+b3*(Ya-Ys)+c3*(Za-Zs))
    
    return x,y

#读取控制点文件的函数，文件格式为：点号，纬度，经度，高度（WGS-84坐标系）
#返回值为一个列表
def ReadControlPoints(file_path):
    fo=open(file_path,'r')
    lines=fo.readlines()
    ControlPoints=[]
    for line in lines:
        str=line.split(',')
        ControlPoints.append([int(str[0]),float(str[1]),float(str[2]),float(str[3])])
    fo.close()    
    return ControlPoints
#高斯投影正算函数，返回高斯坐标:x,y
def LatLon2XY(latitude, longitude):
    a = 6378137.0
    # b = 6356752.3142
    # c = 6399593.6258
    # alpha = 1 / 298.257223563
    e2 = 0.0066943799013
    # epep = 0.00673949674227


    #将经纬度转换为弧度
    latitude2Rad = (math.pi / 180.0) * latitude

    beltNo = int((longitude + 1.5) / 3.0) #计算3度带投影度带号
    
    L = beltNo * 3 #计算中央经线
    
    l0 = longitude - L #经差
    tsin = math.sin(latitude2Rad)
    tcos = math.cos(latitude2Rad)
    t = math.tan(latitude2Rad)
    m = (math.pi / 180.0) * l0 * tcos
    et2 = e2 * pow(tcos, 2)
    et3 = e2 * pow(tsin, 2)
    X = 111132.9558 * latitude - 16038.6496 * math.sin(2 * latitude2Rad) + 16.8607 * math.sin(
        4 * latitude2Rad) - 0.0220 * math.sin(6 * latitude2Rad)
    N = a / math.sqrt(1 - et3)

    x = X + N * t * (0.5 * pow(m, 2) + (5.0 - pow(t, 2) + 9.0 * et2 + 4 * pow(et2, 2)) * pow(m, 4) / 24.0 + (
    61.0 - 58.0 * pow(t, 2) + pow(t, 4)) * pow(m, 6) / 720.0)
    y = 500000 + N * (m + (1.0 - pow(t, 2) + et2) * pow(m, 3) / 6.0 + (
    5.0 - 18.0 * pow(t, 2) + pow(t, 4) + 14.0 * et2 - 58.0 * et2 * pow(t, 2)) * pow(m, 5) / 120.0)

    return x, y

#将大地坐标转换为WGS84下的地心空间直角坐标的函数
def BLH2XYZ(B,L,H):
    a=6378137 
    e2_1=0.00669437999013
    e2_2=0.00673949674227
    
    B=B*math.pi/180
    L=L*math.pi/180
    
    W=math.sqrt(1-e2_1*math.sin(B)*math.sin(B))
    #V=math.sqrt(1+e2_2*math.cos(B)*math.cos(B))
    N=a/W
    X=(N+H)*math.cos(B)*math.cos(L)
    Y=(N+H)*math.cos(B)*math.sin(L)
    Z=(N*(1-e2_1)+H)*math.sin(B)
    
    return X,Y,Z

#提取无人机照片XML字段信息的函数，输入参数为存放照片的文件夹路径
#该函数在照片同目录下生成同名的txt文件
def XmlExtract(MyPath):
    if MyPath=="":
        pass
    else:
        for root, dir, files in os.walk(MyPath):
            for filename in files:
                with open(os.path.join(root,(filename.split('.')[0]+".txt")),mode="a") as f:
                    if(filename.endswith('.txt')!=True):

                        with Image.open(os.path.join(root, filename)) as im:
                            for segment, content in im.applist:
                                marker, body = content.split(b'\x00', 1)
                                if segment == 'APP1' and marker == b'http://ns.adobe.com/xap/1.0/':
                                    # parse the XML string with any method you like
                                    str1 = str(body, encoding="utf-8")
                                    p1 = re.compile(r'[<](.*?)[>]', re.S)
                                    listXMP = re.findall(p1, str1)
                                    list1 = listXMP[3].split('\n')
                                    for itemdata in list1:
                                        list2 = itemdata.strip().split('=')
                                        f.writelines(list2[0] + " = " + list2[1][1:-1]+'\n')

                    f.close()

#知乎大神的cv2读中文路径图像的函数
def cv_imread(file_path):
    cv_img=cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
    return cv_img

#最小二乘仿射变换函数
def my_getAffineTransform(src,dst):
    m=len(src)
    A=np.zeros((2*m,6))
    b=np.zeros((2*m,1))
    for i in range(m):
        for j in range(2):
            if j==0:
                A[2*i+j][0]=src[i][0]
                A[2*i+j][1]=src[i][1]
                A[2*i+j][4]=1
                b[2*i+j][0]=dst[i][0]
            if j==1:
                A[2*i+j][2]=src[i][0]
                A[2*i+j][3]=src[i][1]
                A[2*i+j][5]=1
                b[2*i+j][0]=dst[i][1]

    Nbb=np.linalg.inv((A.T).dot(A))
    x=(Nbb.dot(A.T)).dot(b)
    
    M=np.zeros((2,3))
    M[0][0]=x[0][0]
    M[0][1]=x[1][0]
    M[0][2]=x[4][0]
    M[1][0]=x[2][0]
    M[1][1]=x[3][0]
    M[1][2]=x[5][0]
    
    return M

#计算仿射变换矩阵与单点相乘的结果
def PointAffineTransform(M,P):
    x=M[0][0]*P[0]+M[0][1]*P[1]+M[0][2]
    y=M[1][0]*P[0]+M[1][1]*P[1]+M[1][2]
    return x,y

if __name__ == "__main__":
    points=ReadControlPoints('ControlPoints.txt')
    print(points[0])
        
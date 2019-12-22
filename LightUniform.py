# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 22:10:00 2019

@author: 23872
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

def compute(img, min_percentile, max_percentile):
    #计算分位点，目的是去掉图1的直方图两头的异常情况
    max_percentile_pixel = np.percentile(img, max_percentile)
    min_percentile_pixel = np.percentile(img, min_percentile)

    return max_percentile_pixel, min_percentile_pixel


def aug_img(src):
#    print('lightness:',get_lightness(src))
    # 先计算分位点，去掉像素值中少数异常值，这个分位点可以自己配置。
    max_percentile_pixel, min_percentile_pixel = compute(src, 10, 90)
#    print('max:',max_percentile_pixel)
#    print('min:',min_percentile_pixel)
    # 去掉分位值区间之外的值
    src[src>=max_percentile_pixel] = max_percentile_pixel
    src[src<=min_percentile_pixel] = min_percentile_pixel

	# 将分位值区间拉伸到0到255，这里取了255*0.1与255*0.9是因为可能会出现像素值溢出的情况，所以最好不要设置为0到255。
    out = np.zeros(src.shape, src.dtype)
    cv2.normalize(src, out, 0,255,cv2.NORM_MINMAX)

    return out

def get_lightness(src):
	# 计算亮度
    hsv_image = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    lightness = hsv_image[:,:,2].mean()
    
    return  lightness

if __name__=='__main__':
    img = cv2.imread("./data/cct14_1.png")
    plt.hist(img.ravel(), 256)
    plt.show()
    img = aug(img)
    plt.imshow(img)
    plt.show()
    plt.hist(img.ravel(), 256)
    plt.show()
    plt.imshow(img)
    plt.show()
    print('ok')

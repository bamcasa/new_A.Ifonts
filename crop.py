#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('dark_background')


# # Read Input Image

# In[3]:


path, dirs, files = next(os.walk("test1"))
print(len(files))

for file in files:
    img_ori = cv2.imread(f'test1/{file}')

    height, width, channel = img_ori.shape

    # plt.figure(figsize=(12, 10))
    # cv2.imshow("img_ori",img_ori)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # # Convert Image to Grayscale

    # In[4]:

    # hsv = cv2.cvtColor(img_ori, cv2.COLOR_BGR2HSV)
    # gray = hsv[:,:,2]
    gray = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)

    # cv2.imshow("gray",gray)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # # Maximize Contrast (Optional)

    # In[5]:

    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    imgTopHat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, structuringElement)
    imgBlackHat = cv2.morphologyEx(
        gray, cv2.MORPH_BLACKHAT, structuringElement)

    imgGrayscalePlusTopHat = cv2.add(gray, imgTopHat)
    gray = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

    # cv2.imshow("gray",gray)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # # Adaptive Thresholding

    # In[6]:

    img_blurred = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)

    img_thresh = cv2.adaptiveThreshold(
        img_blurred,
        maxValue=255.0,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=19,
        C=9
    )

    # cv2.imshow("gray",gray)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # # Find Contours

    # In[ ]:

    contours, _ = cv2.findContours(
        img_thresh,
        cv2.RETR_LIST,
        method=cv2.CHAIN_APPROX_SIMPLE
    )

    temp_result = np.zeros((height, width, channel), dtype=np.uint8)

    cv2.drawContours(temp_result, contours=contours,
                     contourIdx=-1, color=(255, 255, 255))

    # cv2.imshow("temp_result",temp_result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # # Prepare Data

    # In[10]:

    temp_result = np.zeros((height, width, channel), dtype=np.uint8)

    contours_dict = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(temp_result, pt1=(x, y), pt2=(
            x + w, y + h), color=(255, 255, 255), thickness=2)

        # insert to dict
        contours_dict.append({
            'contour': contour,
            'x': x,
            'y': y,
            'w': w,
            'h': h,
            'cx': x + (w / 2),
            'cy': y + (h / 2)
        })

    # cv2.imshow("temp_result",temp_result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    MIN_AREA = 80
    MIN_WIDTH, MIN_HEIGHT = 4, 4
    MIN_RATIO, MAX_RATIO = 0.3, 5.0
    # 수치 조정 해야함 <------------------------------------------------------------------------------------------------------------

    possible_contours = []

    cnt = 0
    for d in contours_dict:
        area = d['w'] * d['h']
        ratio = d['w'] / d['h']

        if area > MIN_AREA and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT and MIN_RATIO < ratio < MAX_RATIO:
            d['idx'] = cnt
            cnt += 1
            possible_contours.append(d)

    # visualize possible contours

    dst = []

    for d in possible_contours:
        #     cv2.drawContours(temp_result, d['contour'], -1, (255, 255, 255))
        if d['h'] >= 40 and d['w'] >= 40:
            dst.append(img_ori[d['y']:d['y'] + d['h'], d['x']:d['x'] + d['w']])

    number = 1
    for img in dst:
        cv2.imwrite(f"crop_image/{number}_{file}", img)
        print(f"crop_image/{number}_{file}")
        number += 1

    # for d in possible_contours:
        #     cv2.drawContours(temp_result, d['contour'], -1, (255, 255, 255))
    #    cv2.rectangle(img_ori, pt1=(d['x'], d['y']), pt2=(d['x'] + d['w'], d['y'] + d['h']), color=(211, 200, 86),
    #                  thickness=2)

    #cv2.imshow("img_ori", img_ori)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

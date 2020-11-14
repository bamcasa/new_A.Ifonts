import cv2
import numpy as np
import os

if not(os.path.isdir("crop_image")):
    os.makedirs("crop_image")

path, dirs, files = next(os.walk("INPUT_IMAGE"))
print(len(files))


for file in files:
    img_ori = cv2.imread(f'INPUT_IMAGE/{file}')
    #img_ori = cv2.resize(img_ori, dsize=(0, 0), fx=0.1, fy=0.1, interpolation=cv2.INTER_AREA)
    #이미지가 클 경우에만 사용
    height, width, channel = img_ori.shape
    #print(height,width)

    gray = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)

    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    imgTopHat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, structuringElement)
    imgBlackHat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, structuringElement)

    imgGrayscalePlusTopHat = cv2.add(gray, imgTopHat)
    gray = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

    img_blurred = cv2.GaussianBlur(gray, (9, 9), 0)

    img_thresh = cv2.adaptiveThreshold(
        img_blurred,
        maxValue=255.0,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=19,
        C=9
    )

    contours, _ = cv2.findContours(
        img_thresh,
        cv2.RETR_LIST,
        method=cv2.CHAIN_APPROX_SIMPLE
    )

    temp_result = np.zeros((height, width, channel), dtype=np.uint8)

    cv2.drawContours(temp_result, contours=contours, contourIdx=-1, color=(255, 255, 255))

    temp_result = np.zeros((height, width, channel), dtype=np.uint8)

    contours_dict = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(temp_result, pt1=(x, y), pt2=(x + w, y + h), color=(255, 255, 255), thickness=2)
        # cv2.rectangle(img_ori, pt1=(x, y), pt2=(x + w, y + h), color=(255, 255, 255), thickness=2)

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

    MIN_AREA = 40
    MIN_WIDTH, MIN_HEIGHT = 4, 4
    MIN_RATIO, MAX_RATIO = 0.3, 10.0
    # 수치 조정 해야함 <------------------------------------------------------------------------------------------------------------

    possible_contours = []

    sum_height = 0
    sum_width = 0

    cnt = 0
    for d in contours_dict:
        area = d['w'] * d['h']
        ratio = d['w'] / d['h']

        sum_width += d['w']
        sum_height += d['h']

        # if area > MIN_AREA and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT and MIN_RATIO < ratio < MAX_RATIO:
        d['idx'] = cnt
        cnt += 1
        possible_contours.append(d)

    avg_height = sum_height / len(possible_contours)
    avg_width = sum_width / len(possible_contours)

    print(len(possible_contours))

    print(avg_width, avg_height)
    dst = []

    for d in possible_contours:
        # cv2.drawContours(temp_result, d['contour'], -1, (255, 255, 255))
        # print(d['h'],"  ",d['w'])
        if d['h'] >= avg_height and d['w'] >= avg_width:
            dst.append(img_ori[d['y']:d['y'] + d['h'], d['x']:d['x'] + d['w']])

    #cv2.imshow("img_ori", img_ori)
    #cv2.imshow("temp_result", temp_result)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    number = 1

    for img in dst:
        cv2.imwrite(f"crop_image/{number}_{file}", img)
        print(f"crop_image/{number}_{file}")
        number += 1

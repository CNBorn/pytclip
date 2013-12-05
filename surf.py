import numpy as np
from math import ceil
import cv2

def detect_character(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    surf = cv2.SURF()
    mask = np.uint8(np.ones(gray.shape))
    surf_points = surf.detect(gray, mask)

    height, width, depth = img.shape
    start_x = 0
    end_x = height

    X = 0
    Y = 1

    section_index = 0
    total = 0
    section_num = {}

    for i in surf_points:
        if (i.pt[X] > start_x and i.pt[X] < end_x):
            section_index = int(ceil(i.pt[Y]/10.0))
            section_num.setdefault(section_index, 0)
            section_num[section_index] += 1
            total += 1

    avg = total / len(section_num)

    slice_total = 10
    slice_num = len(section_num) / slice_total
    slice_counter = 0
    for m in xrange(slice_total):
        for n in xrange(m*slice_num, (m+1)*slice_num):
            if section_num.get(n,0) >= avg:
                slice_counter += 1
                break

    if (slice_counter >= slice_total):
        return -1

    con_num = 4
    flag = 0

    for k,v in section_num.iteritems():
        if v > avg and flag == 0:
            counter += 1
        else:
            counter = 0
        if counter >= con_num and flag == 0:
            sY = k
            flag = 1
    
    if sY > con_num and sY < (height / 4):
        return 0 if (sY - con_num -11 ) * slice_total < 0 else (sY - con_num -11) * slice_total

    elif sY > con_num:
        return (sY - con_num) * slice_total

    return sY * 10


import numpy as np
import cv2
from matplotlib import pyplot as plt

for i in range(6):
    path = f'./Images/roi_{i}.png'
    # path = './Images/inna.jpg'
    # path = './Images/pobrane.jpg'
    cube_img = cv2.imread(path)
    cv2.imshow("Rubiks Cube Solver", cube_img)
    cv2.waitKey(0)
    gray = cv2.cvtColor(cube_img, cv2.COLOR_BGR2GRAY)
    dst = cv2.equalizeHist(gray)
    thresh = 60
    im_bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("Rubiks Cube Solver", im_bw)
    cv2.waitKey(0)
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(im_bw, kernel, iterations=1)
    cv2.imshow("Erosion", erosion)
    cv2.waitKey(0)
    dilatation = cv2.dilate(erosion, kernel, iterations=1)
    cv2.imshow("Rubiks Cube Solver", dilatation)
    cv2.waitKey(0)
    img = cv2.GaussianBlur(erosion, (5, 5), 0)
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    print(len(contours))
    coordinates = [None] * len(contours) # *9?
    ctr = 0
    for j in range(len(contours)):
        max_x = max(contours[j], key=lambda x: x[0][0])
        max_y = max(contours[j], key=lambda x: x[0][1])
        min_x = min(contours[j], key=lambda x: x[0][0])
        min_y = min(contours[j], key=lambda x: x[0][1])
        top_left = (min_x[0][0], min_y[0][1])
        bottom_right = (max_x[0][0], max_y[0][1])
        # check if square
        side1 = bottom_right[0] - top_left[0]
        side2 = bottom_right[1] - top_left[1]
        if side1/side2 > 0.6 and side1/side2 < 1.4 and side2*side1 > 3000 and side2*side1 < 30000:
            coord = [top_left, bottom_right]
            coordinates[ctr] = coord
            ctr += 1

    coordinates = [x for x in coordinates if x is not None]

    for j in range(len(coordinates)):
        cube_img = cv2.rectangle(cube_img, coordinates[j][0], coordinates[j][1], color=(255,0,255), thickness=1)
        print(coordinates[j])
        cv2.imshow('Rubiks Cube Solver', cube_img)
        cv2.waitKey(0)

    #check if square


    # cv2.drawContours(cube_img, coordinates, -1, (0, 255, 0), 3)
    cv2.imshow('Rubiks Cube Solver', cube_img)
    cv2.waitKey(0)

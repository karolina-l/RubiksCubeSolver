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
    cv2.imshow("Rubiks Cube Solver", gray)
    cv2.waitKey(0)
    dst = cv2.equalizeHist(gray)
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    # dst = clahe.apply(gray)
    cv2.imshow("Rubiks Cube Solver", dst)
    cv2.waitKey(0)
    img_gauss = cv2.GaussianBlur(dst, (5, 5), 0) # do przeniesienia
    thresh = 110
    im_bw = cv2.threshold(img_gauss, thresh, 255, cv2.THRESH_BINARY)[ 1]
    cv2.imshow("Rubiks Cube Solver", im_bw)
    cv2.waitKey(0)
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(im_bw, kernel, iterations=1)
    cv2.imshow("Erosion", erosion)
    cv2.waitKey(0)
    dilatation = cv2.dilate(erosion, kernel, iterations=1)
    cv2.imshow("Rubiks Cube Solver", dilatation)
    cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    #print(len(contours))
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
    coo_sorted = [None] * len(coordinates)
    for j in range(len(coordinates)):
        middle = ((coordinates[j][1][0]-coordinates[j][0][0])/2 + coordinates[j][0][0],
                  (coordinates[j][1][1]-coordinates[j][0][1])/2 + coordinates[j][0][1])

        if middle[0] < 107 and middle[1] < 107:
            coo_sorted[0] = coordinates[j]
        elif middle[0] > 107 and middle[0] < 214 and middle[1] < 107:
            coo_sorted[1] = coordinates[j]
        elif middle[0] > 214 and middle[1] < 107:
            coo_sorted[2] = coordinates[j]
        elif middle[0] < 107 and middle[1] > 107 and middle[1] < 214:
            coo_sorted[3] = coordinates[j]
        elif middle[0] > 107 and middle[0] < 214 and middle[1] > 107 and middle[1] < 214:
            coo_sorted[4] = coordinates[j]
        elif middle[0] > 214 and middle[1] > 107 and middle[1] < 214:
            coo_sorted[5] = coordinates[j]
        elif middle[0] < 107 and middle[1] > 214:
            coo_sorted[6] = coordinates[j]
        elif middle[0] > 107 and middle[0] < 214 and middle[1] > 214:
            coo_sorted[7] = coordinates[j]
        elif middle[0] > 214 and middle[1] > 214:
            coo_sorted[8] = coordinates[j]

    for j in range(len(coo_sorted)):
        cube_img = cv2.rectangle(cube_img, coo_sorted[j][0], coo_sorted[j][1], color=(255,0,255), thickness=1)
        #print(coordinates[j])
        cv2.imshow('Rubiks Cube Solver', cube_img)
        cv2.waitKey(0)

    #check if square


    # cv2.drawContours(cube_img, coordinates, -1, (0, 255, 0), 3)
    cv2.imshow('Rubiks Cube Solver', cube_img)
    cv2.waitKey(0)

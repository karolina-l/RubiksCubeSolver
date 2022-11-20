import numpy as np
import cv2
import color_ranges as cr

img_ctr = 0
grid_start = (160, 80)
grid_end = (480, 400)
grid_color = (255, 0, 255)
grid_thickness = 2

def dilationAndMask(color_mask, imageFrame):
    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernel = np.ones((5, 5), "uint8")

    color_mask = cv2.dilate(color_mask, kernel)
    res = cv2.bitwise_and(imageFrame, imageFrame, mask=color_mask)
    return color_mask, res


def contour(color_mask, color_name, color_r, color_g, color_b, frame):
    contours, hierarchy = cv2.findContours(color_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    areas = list()

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 3000:
            areas.append(area)
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y),
                                       (x + w, y + h),
                                       (color_b, color_g, color_r), 2)

            cv2.putText(frame, f"{color_name} Color", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (color_b, color_g, color_r))
    return color_name, sum(areas)

def getCoordsSortedAndROIimg(i):
    path = f'./Images/works/cube_{i}.png'
    cube_img = cv2.imread(path)

    roi_img = cube_img[grid_start[1]:grid_end[1], grid_start[0]:grid_end[0]]

    gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
    dst = cv2.equalizeHist(gray)
    img_gauss = cv2.GaussianBlur(dst, (5, 5), 0)
    thresh = 110
    im_bw = cv2.threshold(img_gauss, thresh, 255, cv2.THRESH_BINARY)[1]
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(im_bw, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    coordinates = [None] * len(contours)
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
        if side1 != 0 and side2 != 0 and side1 / side2 > 0.6 and side1 / side2 < 1.4 \
                and side2 * side1 > 3000 and side2 * side1 < 30000:
            coord = [top_left, bottom_right]
            coordinates[ctr] = coord
            ctr += 1

    coordinates = [x for x in coordinates if x is not None]
    coo_sorted = [None] * len(coordinates)
    for j in range(len(coordinates)):
        middle = ((coordinates[j][1][0] - coordinates[j][0][0]) / 2 + coordinates[j][0][0],
                  (coordinates[j][1][1] - coordinates[j][0][1]) / 2 + coordinates[j][0][1])

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

    return coo_sorted, roi_img

def sliceService(coo_sorted, roi_img):
    face = []
    for a in range(9):
        slice = roi_img[coo_sorted[a][0][1]:coo_sorted[a][1][1], coo_sorted[a][0][0]:coo_sorted[a][1][0]]
        # Convert slice from RGB to HSV
        hsvFrame = cv2.cvtColor(slice, cv2.COLOR_BGR2HSV)

        # define masks
        red_mask_1 = cv2.inRange(hsvFrame, cr.red_lower_1, cr.red_upper_1)
        red_mask_2 = cv2.inRange(hsvFrame, cr.red_lower_2, cr.red_upper_2)
        green_mask = cv2.inRange(hsvFrame, cr.green_lower, cr.green_upper)
        blue_mask = cv2.inRange(hsvFrame, cr.blue_lower, cr.blue_upper)
        yellow_mask = cv2.inRange(hsvFrame, cr.yellow_lower, cr.yellow_upper)
        white_mask = cv2.inRange(hsvFrame, cr.white_lower, cr.white_upper)
        orange_mask = cv2.inRange(hsvFrame, cr.orange_lower, cr.orange_upper)

        # Morphological Transform, Dilation
        red_mask_1, res_red = dilationAndMask(red_mask_1, slice)
        red_mask_2, res_red = dilationAndMask(red_mask_2, slice)
        green_mask, res_green = dilationAndMask(green_mask, slice)
        blue_mask, res_blue = dilationAndMask(blue_mask, slice)
        yellow_mask, res_yellow = dilationAndMask(yellow_mask, slice)
        white_mask, res_white = dilationAndMask(white_mask, slice)
        orange_mask, res_orange = dilationAndMask(orange_mask, slice)

        # Creating contours to track colors
        r1_col, r1_area = contour(red_mask_1, "r", 255, 0, 0, slice)  # red F
        r2_col, r2_area = contour(red_mask_2, "r", 255, 0, 0, slice)  # red F
        g_col, g_area = contour(green_mask, "g", 0, 255, 0, slice)  # green R
        b_col, b_area = contour(blue_mask, "b", 0, 0, 255, slice)  # blue L
        y_col, y_area = contour(yellow_mask, "y", 255, 255, 0, slice)  # yellow U
        w_col, w_area = contour(white_mask, "w", 255, 255, 255, slice)  # white D
        o_col, o_area = contour(orange_mask, "o", 255, 128, 0, slice)  # orange B

        r_col = r1_col
        r_area = r1_area + r2_area
        col_areas = list()
        col_areas.append({'color': r_col, 'area': r_area})
        col_areas.append({'color': g_col, 'area': g_area})
        col_areas.append({'color': b_col, 'area': b_area})
        col_areas.append({'color': y_col, 'area': y_area})
        col_areas.append({'color': w_col, 'area': w_area})
        col_areas.append({'color': o_col, 'area': o_area})

        detected = max(col_areas, key=lambda x: x['area'])

        face.append(detected['color'])

    return face

def faceSorting(cube_faces, face):
    if face[4] == 'y':  # yellow
        cube_faces[0] = face
    elif face[4] == 'g':  # green
        cube_faces[1] = face
    elif face[4] == 'r':  # red
        cube_faces[2] = face
    elif face[4] == 'w':  # white
        cube_faces[3] = face
    elif face[4] == 'b':  # blue
        cube_faces[4] = face
    elif face[4] == 'o':  # orange
        cube_faces[5] = face

def cubeFormatConversion(cube_faces):
    for i in range(6):
        for j in range(9):
            if cube_faces[i][j] == 'y':  # yellow
                cube_faces[i][j] = 'U'
            elif cube_faces[i][j] == 'g':  # green
                cube_faces[i][j] = 'R'
            elif cube_faces[i][j] == 'r':  # red
                cube_faces[i][j] = 'F'
            elif cube_faces[i][j] == 'w':  # white
                cube_faces[i][j] = 'D'
            elif cube_faces[i][j] == 'b':  # blue
                cube_faces[i][j] = 'L'
            elif cube_faces[i][j] == 'o':  # orange
                cube_faces[i][j] = 'B'

    cube_aos = [None] * 6
    for i in range(6):
        cube_aos[i] = ''.join(cube_faces[i])

    cube_str = ''.join(cube_aos)

    return cube_str

def toSingmatserNotation(sol_s):
    sol_l = sol_s.split()
    sol_l = sol_l[:-1]

    for i in range(len(sol_l)):
        if sol_l[i].find('3') != -1:
            sol_l[i] = sol_l[i].replace('3', "'")

    sol_s = ' '.join(sol_l)
    return sol_s

def checkIfNine(cube_str):
    occurences = [0,0,0,0,0,0]
    control = 9
    occurences[0] = (cube_str.count('r'), 'red')
    occurences[1] = (cube_str.count('g'), 'green')
    occurences[2] = (cube_str.count('b'), 'blue')
    occurences[3] = (cube_str.count('y'), 'yellow')
    occurences[4] = (cube_str.count('o'), 'orange')
    occurences[5] = (cube_str.count('w'), 'white')
    for i in range(6):
        if occurences[i][0] < 9:
            control = i
    if control == 9:
        return "Each color appears 9 times"
    else:
         return f"There is {occurences[control][1]} color missing"

import numpy as np
import cv2
import color_ranges as cr
import copy
import twophase.solver as sv

# Capturing video through webcam
webcam = cv2.VideoCapture(0)

def DilationAndMask(color_mask, imageFrame):
    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernel = np.ones((5, 5), "uint8")

    color_mask = cv2.dilate(color_mask, kernel)
    res = cv2.bitwise_and(imageFrame, imageFrame, mask=color_mask)
    return color_mask, res


def Contour(color_mask, color_name, color_r, color_g, color_b, frame):
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


def showUD(face):
    spacing = 18 * ' '
    for i in range(0,7,3):
        print(spacing + str(face[i:i+3]))

def show(cube):
    print("Sprawdz czy kolory są na odpowiednich kafelkach.")
    cube_duplicate = 6 * [None]
    cube_duplicate[0] = cube[0]
    cube_duplicate[1] = cube[4]
    cube_duplicate[2] = cube[2]
    cube_duplicate[3] = cube[1]
    cube_duplicate[4] = cube[5]
    cube_duplicate[5] = cube[3]
    showUD(cube_duplicate[0])
    for row in range(0,7,3):
        long_row = []
        for side in range(1,5):
            long_row.append(cube_duplicate[side][row:row+3])
        print(long_row)
    showUD(cube_duplicate[5])


img_ctr = 0
grid_start = (160, 80)
grid_end = (480, 400)
grid_color = (255, 0, 255)
grid_thickness = 2

# Start a while loop
while (1):

    # Capturing 6 images from camera
    while (img_ctr < 6):
        ret, imageFrame = webcam.read()
        img_cpy = copy.copy(imageFrame)
        img_cpy = cv2.rectangle(img_cpy, grid_start, grid_end, grid_color, grid_thickness)
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Rubiks Cube Solver", img_cpy)
        action = cv2.waitKey(1)
        if action%256 == 32:
            captured_img = f"./Images/cube_{img_ctr}.png"
            cv2.imwrite(captured_img, imageFrame)
            print(f"{captured_img} written!")
            img_ctr += 1

    # print("idziemy dalej")
    cube_faces = [None] * 6
    for i in range(6):
        path = f'./Images/cube_{i}.png'
        cube_img = cv2.imread(path)
        # cv2.imshow("Rubiks Cube Solver", cube_img)

        # selecting ROI
        # isFromCenter = False
        # r = cv2.selectROI("Rubiks Cube Solver", cube_img, isFromCenter)
        # roi_img = cube_img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        roi_img = cube_img[grid_start[1]:grid_end[1], grid_start[0]:grid_end[0]]
        captured_img = f"./Images/roi_{i}.png" # będzie do usunięcia
        cv2.imwrite(captured_img, roi_img) # będzie do usunięcia

        # cv2.imshow("Rubiks Cube Solver", roi_img)
        # height, width, _ = roi_img.shape
        # cv2.waitKey(0)

        gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Rubiks Cube Solver", gray)
        # cv2.waitKey(0)
        dst = cv2.equalizeHist(gray)
        img_gauss = cv2.GaussianBlur(dst, (5, 5), 0)  # do przeniesienia
        thresh = 110
        im_bw = cv2.threshold(img_gauss, thresh, 255, cv2.THRESH_BINARY)[1]
        kernel = np.ones((5, 5), np.uint8)
        erosion = cv2.erode(im_bw, kernel, iterations=1)
        # cv2.imshow("Erosion", erosion)
        # cv2.waitKey(0)
        contours, hierarchy = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print(len(contours))
        coordinates = [None] * len(contours)  # *9?
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

#         for j in range(len(coo_sorted)):
#             cube_img = cv2.rectangle(cube_img, coo_sorted[j][0], coo_sorted[j][1], color=(255, 0, 255), thickness=1)
#             # print(coordinates[j])
#             cv2.imshow('Rubiks Cube Solver', roi_img)
#             cv2.waitKey(0)

        # getting singular tiles
        slice_ctr = 0
        face = []
        for a in range(9):
                slice = roi_img[coo_sorted[a][0][1]:coo_sorted[a][1][1], coo_sorted[a][0][0]:coo_sorted[a][1][0]]
                captured_img = f"./Images/slice_{i}_{slice_ctr}.png"  # będzie do usunięcia
                slice_ctr += 1 # będzie do usunięcia
                cv2.imwrite(captured_img, slice) # będzie do usunięcia
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
                red_mask_1, res_red = DilationAndMask(red_mask_1, slice)
                red_mask_2, res_red = DilationAndMask(red_mask_2, slice)
                green_mask, res_green = DilationAndMask(green_mask, slice)
                blue_mask, res_blue = DilationAndMask(blue_mask, slice)
                yellow_mask, res_yellow = DilationAndMask(yellow_mask, slice)
                white_mask, res_white = DilationAndMask(white_mask, slice)
                orange_mask, res_orange = DilationAndMask(orange_mask, slice)

                # Creating contours to track colors
                r1_col, r1_area = Contour(red_mask_1, "r", 255, 0, 0, slice) # red F
                r2_col, r2_area = Contour(red_mask_2, "r", 255, 0, 0, slice) # red F
                g_col, g_area = Contour(green_mask, "g", 0, 255, 0, slice) # green R
                b_col, b_area = Contour(blue_mask, "b", 0, 0, 255, slice) # blue L
                y_col, y_area = Contour(yellow_mask, "y", 255, 255, 0, slice) # yellow U
                w_col, w_area = Contour(white_mask, "w", 255, 255, 255, slice) # white D
                o_col, o_area = Contour(orange_mask, "o", 255, 128, 0, slice) # orange B

                r_col = r1_col
                r_area = r1_area + r2_area
                col_areas = list()
                col_areas.append({'color': r_col, 'area': r_area})
                col_areas.append({'color': g_col, 'area': g_area})
                col_areas.append({'color': b_col, 'area': b_area})
                col_areas.append({'color': y_col, 'area': y_area})
                col_areas.append({'color': w_col, 'area': w_area})
                col_areas.append({'color': o_col, 'area': o_area})

                detected = max(col_areas, key=lambda x:x['area'])

                # print(f"this tile is {detected['color']}")
                face.append(detected['color'])

                # cv2.destroyWindow("Rubiks Cube Solver")
                # cv2.imshow("Rubiks Cube Solver", slice)
        # cv2.waitKey(0)

        #showUD(face)


        if face[4] == 'y': # yellow
            cube_faces[0] = face
        elif face[4] == 'g': # green
            cube_faces[1] = face
        elif face[4] == 'r': # red
            cube_faces[2] = face
        elif face[4] == 'w': # white
            cube_faces[3] = face
        elif face[4] == 'b': # blue
            cube_faces[4] = face
        elif face[4] == 'o': # orange
            cube_faces[5] = face

    # kolejność do wyświetlania w cube_faces: 0,4,2,1,5,3

    temp = [str(i) for i in range(9)]
    temp_cube = [copy.copy(temp), copy.copy(temp), copy.copy(temp), copy.copy(temp), copy.copy(temp), copy.copy(temp)]
    color_list = ['y', 'g', 'r', 'w', 'b', 'o']
    for i in range(6):
        temp_cube[i][4] = color_list[i]

    show(cube_faces)

    correct = input('czy kolory się zgadzają? y/n')
    while correct == 'n':
        show(temp_cube)
        side, no = input('podaj kolor ścianki i numer błędnego kafelka:')
        new_tile = input('podaj poprawny kolor (b/g/y/w/r/o)')
        if side == 'y':
            cube_faces[0][int(no)] = new_tile
        elif side == 'g':
            cube_faces[1][int(no)] = new_tile
        elif side == 'r':
            cube_faces[2][int(no)] = new_tile
        elif side == 'w':
            cube_faces[3][int(no)] = new_tile
        elif side == 'b':
            cube_faces[4][int(no)] = new_tile
        elif side == 'o':
            cube_faces[5][int(no)] = new_tile

        show(cube_faces)
        correct = input('czy teraz jest poprawnie? y/n')

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

    print(f'solution: {sv.solve(cube_str)}')
    cv2.waitKey(0)

    if cv2.waitKey(1) == 27:
        webcam.release()
        cv2.destroyAllWindows()
        break

import numpy as np
import cv2
import color_ranges as cr

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

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y),
                                       (x + w, y + h),
                                       (color_b, color_g, color_r), 2)

            cv2.putText(frame, color_name + " Color", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (color_b, color_g, color_r))


img_ctr = 0
grid_start = (160, 80)
grid_end = (480, 400)
grid_color = (255, 0, 255)
grid_thickness = 2
# Start a while loop
while (1):

    # Reading the video from the
    # webcam in image frames
    # cv2.namedWindow("test")
    while (img_ctr < 6):
        ret, imageFrame = webcam.read()
        imageFrame = cv2.rectangle(imageFrame, grid_start, grid_end, grid_color, grid_thickness)
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Rubiks Cube Solver", imageFrame)
        action = cv2.waitKey(1)
        if action%256 == 32:
            captured_img = f"./Images/cube_{img_ctr}.png"
            cv2.imwrite(captured_img, imageFrame)
            print(f"{captured_img} written!")
            img_ctr += 1

    # print("idziemy dalej")
    # for i in range(5):
    #     path = f'./Images/cube_{i}.png'
    #     cube_img = cv2.imread(path)
    #     # Convert the imageFrame in
    #     # BGR(RGB color space) to
    #     # HSV(hue-saturation-value)
    #     # color space
    #     hsvFrame = cv2.cvtColor(cube_img, cv2.COLOR_BGR2HSV)
    #
    #     # define masks
    #     red_mask = cv2.inRange(hsvFrame, cr.red_lower, cr.red_upper)
    #     green_mask = cv2.inRange(hsvFrame, cr.green_lower, cr.green_upper)
    #     blue_mask = cv2.inRange(hsvFrame, cr.blue_lower, cr.blue_upper)
    #     yellow_mask = cv2.inRange(hsvFrame, cr.yellow_lower, cr.yellow_upper)
    #     white_mask = cv2.inRange(hsvFrame, cr.white_lower, cr.white_upper)
    #     orange_mask = cv2.inRange(hsvFrame, cr.orange_lower, cr.orange_upper)
    #
    #     # Morphological Transform, Dilation
    #     red_mask, res_red = DilationAndMask(red_mask, cube_img)
    #     green_mask, res_green = DilationAndMask(green_mask, cube_img)
    #     blue_mask, res_blue = DilationAndMask(blue_mask, cube_img)
    #     yellow_mask, res_yellow = DilationAndMask(yellow_mask, cube_img)
    #     white_mask, res_white = DilationAndMask(white_mask, cube_img)
    #     orange_mask, res_orange = DilationAndMask(orange_mask, cube_img)
    #
    #     # Creating contours to track colors
    #     Contour(red_mask, "Red", 255, 0, 0, cube_img)
    #     Contour(green_mask, "Green", 0, 255, 0, cube_img)
    #     Contour(blue_mask, "Blue", 0, 0, 255, cube_img)
    #     Contour(yellow_mask, "Yellow", 255, 255, 0, cube_img)
    #     Contour(white_mask, "White", 255, 255, 255, cube_img)
    #     Contour(orange_mask, "Orange", 255, 128, 0, cube_img)
    #
    #     cv2.imshow("Rubiks Cube Solver", cube_img)
    #     cv2.waitKey(0)

    # Program Termination
    # cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)

    if cv2.waitKey(1) == 27:
        webcam.release()
        cv2.destroyAllWindows()
        break

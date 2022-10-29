import numpy as np
import cv2
import color_ranges as cr

# Capturing video through webcam
webcam = cv2.VideoCapture(0)


def DilationAndMask(color_mask):
    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    color_mask = cv2.dilate(color_mask, kernal)
    res = cv2.bitwise_and(imageFrame, imageFrame,
                          mask=color_mask)
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


# Start a while loop
while (1):

    # Reading the video from the
    # webcam in image frames
    _, imageFrame = webcam.read()

    # Convert the imageFrame in 
    # BGR(RGB color space) to 
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # define masks
    red_mask = cv2.inRange(hsvFrame, cr.red_lower, cr.red_upper)
    green_mask = cv2.inRange(hsvFrame, cr.green_lower, cr.green_upper)
    blue_mask = cv2.inRange(hsvFrame, cr.blue_lower, cr.blue_upper)
    yellow_mask = cv2.inRange(hsvFrame, cr.yellow_lower, cr.yellow_upper)
    white_mask = cv2.inRange(hsvFrame, cr.white_lower, cr.white_upper)
    orange_mask = cv2.inRange(hsvFrame, cr.orange_lower, cr.orange_upper)

    # Morphological Transform, Dilation
    red_mask, res_red = DilationAndMask(red_mask)
    green_mask, res_green = DilationAndMask(green_mask)
    blue_mask, res_blue = DilationAndMask(blue_mask)
    yellow_mask, res_yellow = DilationAndMask(yellow_mask)
    white_mask, res_white = DilationAndMask(white_mask)
    orange_mask, res_orange = DilationAndMask(orange_mask)

    # Creating contours to track colors
    Contour(red_mask, "Red", 255, 0, 0, imageFrame)
    Contour(green_mask, "Green", 0, 255, 0, imageFrame)
    Contour(blue_mask, "Blue", 0, 0, 255, imageFrame)
    Contour(yellow_mask, "Yellow", 255, 255, 0, imageFrame)
    Contour(white_mask, "White", 255, 255, 255, imageFrame)
    Contour(orange_mask, "Orange", 255, 128, 0, imageFrame)

    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        # cap.release()
        cv2.destroyAllWindows()
        break

import PySimpleGUI as sg
import cv2
import numpy as np
import twophase.solver as sv
import cube_preparation as cp
import copy
import cube_show as cs

webcam = cv2.VideoCapture(0)
img_ctr = 0

def PopupDropDown(title, text, values):
    window = sg.Window(title,
        [[sg.Text(text)],
        [sg.DropDown(values, key='-DROP-')],
        [sg.OK()]
    ])
    event, values = window.read()
    window.close()
    return None if event != 'OK' else values['-DROP-']

def whatPosition(number):
    if number.startswith('0'):
        if number.endswith('11') or number.endswith('8') or number.endswith('5') or number.endswith('2'):
            i = 2
        elif number.endswith('10') or number.endswith('7') or number.endswith('4') or (number.endswith('1') and len(number) <3):
            i = 1
        elif number.endswith('9') or number.endswith('6') or number.endswith('3') or (number.endswith('0') and len(number) <3):
            i = 0
    elif number.startswith('1'):
        if number.endswith('11') or number.endswith('8') or number.endswith('5') or number.endswith('2'):
            i = 5
        elif number.endswith('10') or number.endswith('7') or number.endswith('4') or (number.endswith('1') and len(number) <3):
            i = 4
        elif number.endswith('9') or number.endswith('6') or number.endswith('3') or (number.endswith('0') and len(number) <3):
            i = 3
    elif number.startswith('2'):
        if number.endswith('11') or number.endswith('8') or number.endswith('5') or number.endswith('2'):
            i = 8
        elif number.endswith('10') or number.endswith('7') or number.endswith('4') or (number.endswith('1') and len(number) <3):
            i = 7
        elif number.endswith('9') or number.endswith('6') or number.endswith('3') or (number.endswith('0') and len(number) < 3):
            i = 6
    return i

def getPositionToChange(event, color):
    i = 99
    j = 99
    if event.endswith('00'):
        i = 0
    elif event.endswith('01'):
        i = 1
    elif event.endswith('02'):
        i = 2
    elif event.endswith('10'):
        i = 3
    elif event.endswith('11'):
        i = 4
    elif event.endswith('12'):
        i = 5
    elif event.endswith('20'):
        i = 6
    elif event.endswith('21'):
        i = 7
    elif event.endswith('22'):
        i = 8

    if event.startswith('U'):
        j = 0
    elif event.startswith('D'):
        j = 5
    elif event.startswith('C'):
        number = event[1:]
        if number.endswith('9') or len(number) > 2:
            j = 4
            i = whatPosition(number)
        elif number.endswith('8') or number.endswith('7') or number.endswith('6'):
            j = 3
            i = whatPosition(number)
        elif number.endswith('5') or number.endswith('4') or number.endswith('3'):
            j = 2
            i = whatPosition(number)
        elif (number.endswith('2') or number.endswith('1') or number.endswith('0')) and len(number) < 3:
            j = 1
            i = whatPosition(number)

    if color == 'red':
        color_sym = 'r'
    elif color == 'green':
        color_sym = 'g'
    elif color == 'blue':
        color_sym = 'b'
    elif color == 'orange':
        color_sym = 'o'
    elif color == 'white':
        color_sym = 'w'
    elif color == 'yellow':
        color_sym = 'y'
    return j, i, color_sym


# ----------- Create the 4 layouts this Window will display -----------
layout1 = [[sg.Text("Let's get started", size=(100, 1), justification='center', font='Helvetica 20')],
           [sg.Push(), sg.Button("Take photos"), sg.Push()]]

text_l2 = "Place a cube in an area bounded by a pink rectangle. The order of walls is not important, but you " \
               "shall remember that red wall is the front one and yellow wall is the top one. You can tell " \
               "the color of the wall by its center element. "
layout2 = [[sg.Text(text_l2, size=(85, None), font='Helvetica 15')],
           [sg.Image(key='-IMG-'),sg.Push(), sg.Text(f"Images to take: {6-img_ctr}", size=(20, 1), key='-CTR-', font='Helvetica 15'), sg.Push()],
           [sg.Button("Photo"), sg.Button("Done")]]

buttonsU = [[sg.Button(' ', size=3, pad=(0,0), key=f'U{j}{i}', button_color=('black', 'black')) for i in range(3)] for j in range(3)]
buttonsD = [[sg.Button(' ', size=3, pad=(0,0), key=f'D{j}{i}', button_color=('black', 'black')) for i in range(3)] for j in range(3)]
buttonsC = [[sg.Button(' ', size=3, pad=(0,0), key=f'C{j}{i}', button_color=('black', 'black')) for i in range(12)] for j in range(3)]
layout3 = [[sg.Text("Check colors. To correct a mistake, click the tile and choose new color.", size=(68, 1), font='Helvetica 15')],
            [sg.Text('', size=(85, 1), key='-ILE-', font='Helvetica 15')],
            [sg.Column(buttonsU, key='u1', pad=(0,0))],
            [sg.Column(buttonsC, key='c1', pad=(0,0))],
            [sg.Column(buttonsD, key='d1', pad=(0,0))],
            [sg.Button("All colors are correct")]]

layout4 = [[sg.Text("Your solution", size=(100, 1), justification='center', font='Helvetica 20')],
           [sg.Text('', size=(100,2), justification='center', key='-SOL-', font='Helvetica 17')]]

# ----------- Create actual layout using Columns and a row of Buttons
layout = [[sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-'),
           sg.Column(layout3, visible=False, key='-COL3-'),  sg.Column(layout4, visible=False, key='-COL4-')],
          [sg.Button('Try Again'), sg.Button('Exit')]]

window = sg.Window('Swapping the contents of a window', layout, size=(1000, 650))

layout = 1  # The currently visible layout
recording = False
while True:
    event, values = window.read(timeout=20)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Try Again':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 1
        recording = False
        img_ctr = 0
        window[f'-COL{layout}-'].update(visible=True)


    elif event == 'Take photos':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 2
        window[f'-COL{layout}-'].update(visible=True)
        window['-CTR-'].update(f"Images to take: {6 - img_ctr}")
        recording = True


    elif event == 'Done' and img_ctr >= 6:
        recording = False
        img = np.full((480, 640), 255)
        imgbytes = cv2.imencode('.png', img)[1].tobytes()
        window['-IMG-'].update(data=imgbytes)

        # ----------cube solving part-----------
        cube_faces = [None] * 6
        for i in range(6):
            coo_sorted, roi_img = cp.getCoordsSortedAndROIimg(i)
            face = cp.sliceService(coo_sorted, roi_img)
            cp.faceSorting(cube_faces, face)
        cube_order = cs.cubeOrder(cube_faces)
        co_flat = cs.flatten(cube_order)
        co_str = ''.join(co_flat)
        info = cp.checkIfNine(co_str)
        # --------------------------------------

        window[f'-COL{layout}-'].update(visible=False)
        layout = 3
        window['-ILE-'].update(info)
        cs.showUD(cube_order[0], 'U', window)
        cs.showC(cube_order, window)
        cs.showUD(cube_order[5], 'D', window)
        window[f'-COL{layout}-'].update(visible=True)


    elif event == 'All colors are correct':
        # ----------cube solving part-----------
        cube_str = cp.cubeFormatConversion(cube_faces)
        solution = sv.solve(cube_str)
        solution = cp.toSingmatserNotation(solution)
        window['-SOL-'].update(solution)
        # --------------------------------------

        window[f'-COL{layout}-'].update(visible=False)
        layout = 4
        window[f'-COL{layout}-'].update(visible=True)


    elif event == 'Photo' and img_ctr < 6:
        ret, frame = webcam.read()
        cv2.imwrite(f'./Images/cube_{img_ctr}.png', frame)
        img_ctr += 1
        window['-CTR-'].update(f"Images to take: {6-img_ctr}")


    elif (event.startswith('U') or event.startswith('C') or event.startswith('D')) and layout == 3:
        values = ["red", "white", "yellow", "green", "blue", "orange"]
        color = PopupDropDown('Color correction', 'Please select correct color and confirm choice', values)
        window[event].update(button_color=color)
        j, i, color_sym = getPositionToChange(event, color)
        cube_order[j][i] = color_sym
        co_flat = cs.flatten(cube_order)
        co_str = ''.join(co_flat)
        info = cp.checkIfNine(co_str)
        window['-ILE-'].update(info)

    if recording:
        grid_start = (160, 80)
        grid_end = (480, 400)
        grid_color = (255, 0, 255)
        grid_thickness = 2

        ret, frame = webcam.read()
        img_cpy = copy.copy(frame)
        img_cpy = cv2.rectangle(img_cpy, grid_start, grid_end, grid_color, grid_thickness)
        imgbytes = cv2.imencode('.png', img_cpy)[1].tobytes()
        window['-IMG-'].update(data=imgbytes)
window.close()
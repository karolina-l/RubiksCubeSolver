import PySimpleGUI as sg
from textwrap import wrap
import cv2
import numpy as np

webcam = cv2.VideoCapture(0)

img_ctr = 0

# ----------- Create the 3 layouts this Window will display -----------
layout1 = [[sg.Text("Let's get started", size=(40, 1), justification='center', font='Helvetica 20')],
           [sg.Button("Take photos")]]

text_l2 = "Place a cube in an area bounded by a pink rectangle. The order of walls is not important, but you " \
               "shall remember that red wall is the front one and yellow wall is the top one. You can tell " \
               "the color of the wall by its center element. "
layout2 = [[sg.Text(text_l2, size=(68, None), font='Helvetica 15')],
           [sg.Image(key='-IMG-'), sg.Text(f"Images to take: {6-img_ctr}", size=(20, 1), key='-CTR-', font='Helvetica 10')],
           [sg.Button("Photo"), sg.Button("Done")]]

layout3 = [[sg.Text("Check colors. To correct a mistake, click the tile and choose new color.", size=(68, 1), font='Helvetica 15')],
           [sg.Button("All colors are correct")]]

layout4 = [[sg.Text("Your solution", size=(20, 1), justification='center', font='Helvetica 20')]]

# ----------- Create actual layout using Columns and a row of Buttons
layout = [[sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-'),
           sg.Column(layout3, visible=False, key='-COL3-'),  sg.Column(layout4, visible=False, key='-COL4-')],
          [sg.Button('Try Again'), sg.Button('Exit')]]

window = sg.Window('Swapping the contents of a window', layout, size=(800, 600))

layout = 1  # The currently visible layout
recording = False
while True:
    event, values = window.read(timeout=20)
    # print(event, values)
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
        recording = True
    elif event == 'Done' and img_ctr >= 6:
        recording = False
        img = np.full((480, 640), 255)
        imgbytes = cv2.imencode('.png', img)[1].tobytes()
        window['-IMG-'].update(data=imgbytes)
        window[f'-COL{layout}-'].update(visible=False)
        layout = 3
        window[f'-COL{layout}-'].update(visible=True)
    elif event == 'All colors are correct':
        window[f'-COL{layout}-'].update(visible=False)
        layout = 4
        window[f'-COL{layout}-'].update(visible=True)
    elif event == 'Photo' and img_ctr < 6:
        ret, frame = webcam.read()
        cv2.imwrite(f'./GUI/cube_{img_ctr}.png', frame)
        img_ctr += 1
        window['-CTR-'].update(f"Images to take: {6-img_ctr}")

    if recording:
        ret, frame = webcam.read()
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
        window['-IMG-'].update(data=imgbytes)
window.close()
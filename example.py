"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
import pyautogui

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
x = 200
y = 200
x_max,y_max = pyautogui.size()
pyautogui.moveTo(x, y, duration = 0.1)
while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
        pyautogui.click(pyautogui.position())
    elif gaze.is_right():
        text = "Looking left"
        x = x - 10
        if x < 0:
            x = x_max
            y = y + 10
            pyautogui.moveTo(x, y, duration=0.1)
        pyautogui.moveRel(-10, 0, duration=0.1)
    elif gaze.is_left():
        text = "Looking right"
        x = x + 10
        if x > x_max :
            x = 0
            y = y+10
            pyautogui.moveTo(x, y, duration=0.1)
        pyautogui.moveRel(10, 0, duration=0.1)


    elif gaze.is_center():
        text = "Looking center"
    ratio = gaze.vertical_ratio()
    print(ratio)
    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147,58, 31), 1)

    frame = cv2.resize(frame,(1600,1000))
    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
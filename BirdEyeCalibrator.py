import matplotlib.pyplot as plt
import cv2
import numpy as np
import pickle

'''
CALIBRATOR HOW TO USE

This piece of code produces a very simple gui to set the src and dst points
of the bird eye view transform for a custom image. The Transformation Matrix is then saved
in a pickle file for later use

All you have to do is:
- Set IMAGE_SRC to be the path to yourt image
- Set PICKLE_DST to be the desired destination for the pickle file

- RUN THE PROGRAM
    keep in mind that each green point will be mapped to the blue point with the same number
- Select the src points by left clicking (green points)
- Select the dst points by left clicking (blue points)
- Enjoy
'''


def dist(a, b):
    return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)


def drawDot(src, pos, text, col):
    # Draws a colored dot with the associeted number onto an image (Src)

    cv2.circle(src, pos, CIRCLE_RADIUS, col, -1)

    textPos = [pos[0] - CIRCLE_RADIUS//2, pos[1] + CIRCLE_RADIUS//2]
    cv2.putText(src, text, textPos,
                cv2.FONT_HERSHEY_SIMPLEX, FONT_SIZE, TEXT_COLOR, FONT_THICK)


def drawDots(disp):
    for (i, p) in enumerate(SRC+DST):
        drawDot(disp, p, str(i % 4), SRC_COLOR if i < 4 else DST_COLOR)


def handleMouse(event, x, y, flags, param):
    global counter, coord, image, color, setuped, selected, SRC, DST
    coord = [x, y]

    if not setuped:
        if event == cv2.EVENT_LBUTTONDOWN:
            if counter < 4:
                SRC.append(coord)
            else:
                DST.append(coord)

            counter += 1

        if counter == 4:
            color = DST_COLOR
    else:
        if event == cv2.EVENT_LBUTTONDOWN:
            for i, p in enumerate(SRC+DST):
                if dist(coord, p) < MIN_DIST_SELECT:
                    selected = i
                    break

        if selected != -1:
            if selected < 4:
                SRC[selected] = coord
            else:
                DST[selected - 4] = coord

        if event == cv2.EVENT_LBUTTONUP:
            selected = -1


def computeTransform():
    return cv2.getPerspectiveTransform(np.float32(SRC), np.float32(DST))


def transformImage(img, Matrix):
    return cv2.warpPerspective(img, Matrix, img.shape[:2][::-1])


IMAGE_SRC = './b.png'
PICKLE_DST = './BirdEyeMatrix.pkl'

CIRCLE_RADIUS = 10
SRC_COLOR = (50, 168, 82)
DST_COLOR = (168, 50, 50)

FONT_SIZE = 0.5
TEXT_COLOR = (255, 255, 255)
FONT_THICK = 1

MIN_DIST_SELECT = 10

SRC = []
DST = []

# The dots' color
color = SRC_COLOR

# The number of clicks
counter = 0

# The mouse coordinates
coord = [0, 0]

# The computed Matrix
Matrix = [[]]

# Source image
image = cv2.imread(IMAGE_SRC)

# A copy of the image where the dots will be drawn
dotted_image = image.copy()

# Window setup
cv2.namedWindow('image')
cv2.setMouseCallback('image', handleMouse)

keepGoing = True

setuped = False

selected = -1

while (counter < 8 and keepGoing):
    # A copy of the dotted image to display the preview of the new dot
    disp = dotted_image.copy()

    drawDots(disp)

    drawDot(disp, coord, str(counter % 4), color)

    cv2.imshow('image', disp)
    cv2.waitKey(1)

    # Exit the loop when the window is closed
    if cv2.getWindowProperty("image", cv2.WND_PROP_VISIBLE) < 1:
        keepGoing = False
        break

setuped = True

while (keepGoing):
    disp = dotted_image.copy()
    drawDots(disp)

    # Coputes and save the perspective transform
    Matrix = computeTransform()

    tranformedImaged = transformImage(image, Matrix)
    newImage = np.concatenate((disp, tranformedImaged), axis=1)

    cv2.imshow("image", newImage)
    cv2.waitKey(1)

    # Exit the loop when the window is closed
    if cv2.getWindowProperty("image", cv2.WND_PROP_VISIBLE) < 1:
        keepGoing = False
        break

cv2.destroyAllWindows()

# Save the Matrix
pickle.dump(Matrix, open(PICKLE_DST, 'wb'))

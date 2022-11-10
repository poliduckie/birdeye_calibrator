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


def drawDot(src):
    # Draws a colored dot with the associeted number onto an image (Src)

    cv2.circle(src, coord, CIRCLE_RADIUS, color, -1)
    cv2.putText(src, str(counter % 4), coord,
                cv2.FONT_HERSHEY_SIMPLEX, FONT_SIZE, TEXT_COLOR, FONT_THICK)


def handleMouse(event, x, y, flags, param):
    global counter, coord, image, color

    coord = [x, y]

    if event == cv2.EVENT_LBUTTONDOWN:
        drawDot(dotted_image)

        if counter < 4:
            SRC.append(coord)
        else:
            DST.append(coord)

        counter += 1

    if counter == 4:
        color = DST_COLOR


def computeTransform():
    return cv2.getPerspectiveTransform(np.float32(SRC), np.float32(DST))


def transformImage(img, Matrix):
    return cv2.warpPerspective(img, Matrix, img.shape[:2][::-1])


IMAGE_SRC = './Source.png'
PICKLE_DST = './BirdEyeMatrix.pkl'

CIRCLE_RADIUS = 10
SRC_COLOR = (50, 168, 82)
DST_COLOR = (168, 50, 50)

FONT_SIZE = 1
TEXT_COLOR = (255, 255, 255)
FONT_THICK = 2

SRC = []
DST = []

color = SRC_COLOR

counter = 0
coord = [0, 0]

image = cv2.imread(IMAGE_SRC)
dotted_image = image.copy()

cv2.namedWindow('image')
cv2.setMouseCallback('image', handleMouse)

keepGoing = True

while keepGoing:
    disp = dotted_image.copy()

    if counter == 8:
        Matrix = computeTransform()

        pickle.dump(Matrix, open(PICKLE_DST, 'wb'))

        print(f'Matrix saved in {PICKLE_DST}')

        cv2.imshow("image", transformImage(image, Matrix))
        cv2.waitKey(0)
        keepGoing = False
        break

    drawDot(disp)

    cv2.imshow('image', disp)
    cv2.waitKey(1)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        keepGoing = False
        break

cv2.destroyAllWindows()

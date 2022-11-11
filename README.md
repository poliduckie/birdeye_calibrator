# Bird eye calibrator
This is a really simple UI to find a perspective transform matrix fitting your needs.

## Perspective transform
With a **Perspective Transformation**, we can change the perspective of a given image or video for getting better insights into the required information.

The transformation acts just by deforming (and not changing) the content of the image.

In this case the implementation of the algorithm is offloaded to the OpenCV library.

For more information:
- [On how the algorithm works](https://www.tutorialspoint.com/dip/perspective_transformation.htm)
- [On how to use the OpenCV implementation of the algorithm](https://www.geeksforgeeks.org/perspective-transformation-python-opencv/)

## The problem
In order to perform the transformation OpenCV first requires you to compute a transformation Matrix. To do that you need four **Source points** and four **Destination points**. Each of the source points will be then mapped by the transformation to a destination point on the transformed image.

![info on the SRC and DST points](https://miro.medium.com/max/786/1*hM1WgvKKnUzDcECPbSmbuw.png)
*The source points are the red coordinates on the left, the destination points are on the right*

Now adjusting those points can be a bit dreadful if you have to adjust some numbers in code, recompute, guess what's wrong, adjust, recompute, guess... over and over and over untill you run out of patiance. 

## My solution
This simple gui is meant to simplify the feedback loop to find the optimal set of control points on the image you need to transform. 

When you close the window the tranformation Matrix computed will be saved usign the pickle library perfect for future usage. 

### How to use?
1. You need the Matplotlib, OpenCv and pickle library to run the script
2. Adjust **IMAGE_SRC** as the path to your image
3. Adjust **PICKLE_DST** as the path where you'd like the resulting pickle file to be
4. Run the script
5. On the window choose your 8 points by left clicking on the desired location, **the source points are green**, **the destination points are blue**. Keep in mind that each src point will be maped to the dst point with the same number
6. On the right the transformed image will appear
7. Adjust the points by moving the cursor while keeping the left mouse button pressed
8. Close the window, the matrix will be saved
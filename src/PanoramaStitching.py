import cv2 as cv
import numpy as np

from src import RANSACAlgorithm
from src.RANSACAlgorithm import project


# Determine image size by projecting image2 corners onto image1
def stitch(image1, image2, hom, homInv):
    image2_h, image2_w, image2_ch = image2.shape

    xp1, yp1 = project(0, 0, homInv)                        # Top-Left Corner
    xp2, yp2 = project(0, image2_h-1, homInv)               # Top-Right Corner
    xp3, yp3 = project(image2_w-1, 0, homInv)               # Bottom-Left Corner
    xp4, yp4 = project(image2_w-1, image2_h-1, homInv)      # Bottom-Right Corner

    # Calculate new width
    # To determine the new size of the stitched image, we have to add the values from
    # image2 corners that fall outside of image1's width and height.
    image1_h, image1_w, image1_ch = image1.shape

    # Added 0 when finding the minimum values, because if image2 corners fall within image1's size, then padding is 0
    min_x = np.round(min(0, xp1, xp2, xp3, xp4)).astype(int)    # The offset for x when adding stitched values of image2
    min_y = np.round(min(0, yp1, yp2, yp3, yp4)).astype(int)    # The offset for y when adding stitched values of image2
    offset_x = np.abs(min_x)   # This is the padding added to the right of image1's width (offset of x)
    offset_y = np.abs(min_y)   # This is the padding added to the top of image1's height (offset of y)

    # I added image1's height and width when finding the maximum value of image2's projected corners
    # so the padding will be 0 if image2's corners fall within image1's height and width
    max_x = np.round(max(image1_w, xp1, xp2, xp3, xp4)).astype(int)
    max_y = np.round(max(image1_h, yp1, yp2, yp3, yp4)).astype(int)

    # To find the padding values for the left and bottom of image1, we only want to find the offset to pad it with, so we
    # subtract the maximum x and y values found from projecting image2's corners with image1's height and width respectively
    new_width = offset_x + image1_w + np.abs(image1_w-max_x)
    new_height = offset_y + image1_h + np.abs(image1_h-max_y)

    stitched_image = np.zeros((new_height, new_width, 3))

    # Add image1 onto stitched_image
    for y in range(image1_h):
        for x in range(image1_w):
            # The offset for x is the min_x value we calculated earlier, and likewise for y
            stitched_image[y+offset_y, x+offset_x] = image1[y, x]

    # Project stitched_image onto image2
    stitched_image_h, stitched_image_w, c = stitched_image.shape

    # We want to get the pixel values of image2, starting at its top corners (min_y, min_x)
    # Since we know that image1 will always be in the right place, we only have to deal with the offsets from the top (y)
    # and left(x) side when we copy image2 onto the stitched_image (min_y, min_x).
    print("\tTransferring pixels from the second image to the stitched image")
    for y in range(min_y, stitched_image_h):
        for x in range(min_x, stitched_image_w):
            if y+offset_y < stitched_image_h and x+offset_x < stitched_image_w:
                xp_stitched, yp_stitched = project(x, y, hom)
                if 0 < xp_stitched < image2_w and 0 < yp_stitched < image2_h:
                    pixel = cv.getRectSubPix(image2, (1, 1), (xp_stitched, yp_stitched))
                    stitched_image[y+offset_y, x+offset_x] = pixel

    stitched_image = stitched_image.astype(np.uint8)

    return stitched_image


# This function takes two images as parameters and returns the stitched image
def stitch_two_images(image1, image2, siftDisplayName, saveSiftMatches, siftFilePath,
                      ransacDisplayName, saveRansacMatches, ransacFilePath, ransacIterations, ransacThreshold):
    # Part 2: SIFT Descriptors
    # Source: https://docs.opencv.org/master/dc/dc3/tutorial_py_matcher.html
    sift = cv.xfeatures2d.SIFT_create()

    # Use SIFT to compute key points and descriptors
    kp1, des1 = sift.detectAndCompute(image1, None)
    kp2, des2 = sift.detectAndCompute(image2, None)

    # Apply ratio test
    bf = cv.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    # Apply ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append([m])

    if saveSiftMatches:
        sift_matches = cv.drawMatchesKnn(image1, kp1, image2, kp2, matches1to2=good_matches, outImg=None,
                                      flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv.imwrite(siftFilePath, sift_matches)
        cv.imshow(siftDisplayName, sift_matches)
        cv.waitKey(0)
        cv.destroyAllWindows()
    # End source

    # Part 3: RANSAC
    hom, homInv = RANSACAlgorithm.init(good_matches, kp1, kp2, ransacIterations, ransacThreshold, image1, image2,
                                       ransacDisplayName, saveRansacMatches, ransacFilePath)
    stitched_image = stitch(image1, image2, hom, homInv)

    return stitched_image

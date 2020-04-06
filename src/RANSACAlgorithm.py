import numpy as np
import cv2 as cv
import random
import warnings


def fxn():
    warnings.warn("Runtime", RuntimeWarning)


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()


def init(matches, kp1, kp2, numIterations, inlierThreshold, image1Display, image2Display, displayName, saveRansacMatches, ransacFilePath):
    kp_matches = get_key_point_matches(kp1, kp2, matches)
    return RANSAC(matches, kp1, kp2, kp_matches, numIterations, inlierThreshold, image1Display, image2Display, displayName, saveRansacMatches, ransacFilePath)


# Part 3 A.
def project(x1, y1, H):
    # Referenced Lecture Slides
    homogeneous_coordinates = np.array([x1, y1, 1])
    projective_transformation = H.dot(homogeneous_coordinates)
    w = projective_transformation[2]
    xp = projective_transformation[0]/w
    yp = projective_transformation[1]/w

    # a = np.array([[[x1, y1]]], dtype='float32')
    # hom_test = cv.perspectiveTransform(a, H)

    return xp, yp


# Part 3 B.
def compute_inlier_count(H, kp_matches, inlierThreshold):
    inlier_count = 0
    # Matches contains the pairs of key point coordinates
    # matches =  [ [[x1, y1],[x2, y2]], [[x3, y3], [x4, y4]], ... ]
    for match in kp_matches:
        distance = calculate_projected_distance(match, H)
        if distance < inlierThreshold:
            inlier_count = inlier_count + 1

    len(match)
    return inlier_count


# Calculate the projected distance of the first pair of points in a match to the second pair of points
def calculate_projected_distance(kp_match, H):
    x1 = kp_match[0].pt[0]
    y1 = kp_match[0].pt[1]

    x2 = kp_match[1].pt[0]
    y2 = kp_match[1].pt[1]

    xp, yp = project(x1, y1, H)
    distance = np.sqrt((xp - x2) ** 2 + (yp - y2) ** 2)
    return distance


def RANSAC(matches, kp1, kp2, kp_matches, numIterations, inlierThreshold, image1, image2, displayName, save_ransac_matches, ransacFilePath):
    # matches is an array containing pairs of matching coordinates:
    # i.e. matches =  [ [[x1, y1], [x2, y2]], [[x3, y3], [x4,y4]] ]

    maxInliers = 0
    highest_score_H = np.zeros((3, 3))

    for i in range(0, numIterations):
        # Randomly select 4 pairs of potentially matching points from matches
        inlier_src_pts = np.zeros((4, 2))
        inlier_dst_pts = np.zeros((4, 2))
        for j in range(4):
            randomInt = random.randint(0, len(kp_matches)-1)
            inlier_src_pts[j] = kp_matches[randomInt][0].pt
            inlier_dst_pts[j] = kp_matches[randomInt][1].pt

        # Compute homography for these 4 points
        H, status = cv.findHomography(inlier_src_pts, inlier_dst_pts, 0)

        # Compute number of inliers
        total_inliers = compute_inlier_count(H, kp_matches, inlierThreshold)
        if total_inliers > maxInliers:  # Update maximum number of inliers if current inlier count is higher
            maxInliers = total_inliers
            print('\tmaxInliers updated', maxInliers)
            highest_score_H = H

    # Find all inlier matches using the highest scoring homography to calculate new refined homography
    inlier_matches = []
    kp_1 = []
    kp_2 = []
    inlier_src_pts = []
    inlier_dst_pts = []
    for i, match in enumerate(kp_matches):
        distance = calculate_projected_distance(match, highest_score_H)
        if distance < inlierThreshold:
            inlier_src_pts.append(match[0].pt)
            inlier_dst_pts.append(match[1].pt)
            kp_1.append(match[0])
            kp_2.append(match[1])
            inlier_matches.append(matches[i])

    # Convert list inlier_src_pts and inlier_dst_pts into array to find homography
    inlier_src_pts = np.asarray(inlier_src_pts)
    inlier_dst_pts = np.asarray(inlier_dst_pts)

    # Find refined homography using only inlier matches found earlier
    hom, status = cv.findHomography(inlier_src_pts, inlier_dst_pts)
    homInv = np.linalg.inv(hom)     # Inverse of hom

    # Display inlier matches
    matching_image = cv.vconcat(image1, image2)
    matching_image = cv.drawMatchesKnn(image1, kp1, image2, kp2, matches1to2=inlier_matches, outImg=matching_image, flags=2)
    if save_ransac_matches:
        print("RANSAC Matches saved to " + ransacFilePath)
        cv.imwrite(ransacFilePath, matching_image)
    cv.imshow(displayName, matching_image)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return hom, homInv


# get_key_point_matches creates an array containing the x,y coordinates of image1 and image2 for each match
def get_key_point_matches(keypoints1, keypoints2, matches):
    kp_matches = []
    # Reference: https://www.learnopencv.com/image-alignment-feature-based-using-opencv-c-python/
    for i, match in enumerate(matches):
        img1_match = keypoints1[match[0].queryIdx]
        img2_match = keypoints2[match[0].trainIdx]
        kp_matches.append([img1_match, img2_match])

    return kp_matches

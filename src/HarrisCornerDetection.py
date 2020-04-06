# Melanie Taing (40009850)
# Assignment 2
# COMP 425
# Lab GI-X

import numpy as np
import cv2 as cv


# Sobel operator kernels to calculate image gradients
def gradient_x(img):
    sobel_x = np.array([[-1 / 8, 0, 1 / 8],
                        [-2 / 8, 0, 2 / 8],
                        [-1 / 8, 0, 1 / 8]], dtype=np.float32)
    return cv.filter2D(img, -1, sobel_x)


def gradient_y(img):
    sobel_y = np.array([[1 / 8, 2 / 8, 1 / 8],
                        [0, 0, 0],
                        [-1 / 8, -2 / 8, -1 / 8]], dtype=np.float32)
    return cv.filter2D(img, -1, sobel_y)


# Calculating gradient angle (theta)
def gradient_angle(Ix, Iy):
    angle_gradient = (np.arctan2(Iy, Ix) + np.pi) * 180 / np.pi
    d = np.hypot(Ix, Iy)
    d = d / d.max() * 255
    return d, angle_gradient


def gradient_magnitude(Ix, Iy):
    magnitude = np.sqrt(Ix ** 2 + Iy ** 2)
    return magnitude


def calculate_harris_corner_response(Ix, Iy, sigma):
    # Compute Ix^2, Iy^2, IxIy
    Ixx = Ix * Ix
    Iyy = Iy * Iy
    Ixy = Ix * Iy

    # Apply Gaussian to Ixx, Iyy and Ixy with sigma given
    Ixx = cv.GaussianBlur(Ixx, (sigma, sigma), 1, 1)
    Iyy = cv.GaussianBlur(Iyy, (sigma, sigma), 1, 1)
    Ixy = cv.GaussianBlur(Ixy, (sigma, sigma), 1, 1)

    k = 0.04
    # Harris Operator c(H) = det(H)/trace(H)+k
    det_H = Ixx * Iyy - Ixy ** 2
    trace_H = Ixx + Iyy
    harris_response = det_H / (trace_H + k)

    return harris_response


def local_maximum_neighborhood(response_image, x, y):
    # Local maximum suppression
    width = response_image.shape[0]
    height = response_image.shape[1]

    local_max = response_image[x, y]
    # If the response is not the local maximum in a 3x3 neighborhood, then suppress it

    # Top left neighbor
    if response_image[max(0, x - 1), max(0, y - 1)] > local_max:
        return False

    # Top neighbor
    if response_image[x, max(0, y - 1)] > local_max:
        return False

    # Top right neighbor
    if response_image[min(width - 1, x + 1), max(0, y - 1)] > local_max:
        return False

    # Left neighbor
    if response_image[max(0, x - 1), y] > local_max:
        return False

    # Right neighbor
    if response_image[min(width - 1, x + 1), y] > local_max:
        return False

    # Bottom left neighbor
    if response_image[max(0, x - 1), min(height - 1, y + 1)] > local_max:
        return False

    # Bottom neighbor
    if response_image[x, min(height - 1, y + 1)] > local_max:
        return False

    # Bottom right neighbor
    if response_image[min(width - 1, x + 1), min(height - 1, y + 1)] > local_max:
        return False

    return True


def draw_interest_pts(original_image, harris_response, threshold, descriptors_interest_points, interest_pts):
    harris_corners = original_image.copy()
    # Source: COMP 425 Lab 3 (TA: Farhan Rahman Wasee)
    # Draw circles for interest points
    for y in range(original_image.shape[1]):
        for x in range(original_image.shape[0]):
            if (int(harris_response[x, y]) > threshold) and local_maximum_neighborhood(harris_response, x, y):
                # Draw circles for interest points with response above threshold and the local max in 3x3 neighborhood
                cv.circle(harris_corners, (y, x), 5, (0, 0, 255), 1)
                interest_pts.append([y, x])
            else:
                descriptors_interest_points[x, y] = 0
    # End source
    return harris_corners


def find_dominant_orientation(interest_points, Ix, Iy):
    w = Ix.shape[0]
    h = Ix.shape[1]

    # Calculate gradient direction (theta)
    d, theta = gradient_angle(Ix, Iy)

    # Calculate edge strength (magnitude)
    vote_strength = gradient_magnitude(Ix, Iy)

    new_interest_pts = []
    num_bins = 36
    for point in interest_points:
        # Initialize a histogram with 36 bins to determine dominant orientation for each point
        x = point[0]
        y = point[1]

        # Source: https://medium.com/@lerner98/implementing-sift-in-python-36c619df7945
        hist = np.zeros(num_bins, dtype=np.float32)
        # Check the neighboring 16x16 region
        for j in range(max(0, y - 7), min(h - 1, y + 8)):
            for i in range(max(0, x - 7), min(w - 1, x + 8)):
                orientation = theta[i, j]
                bin_number = int(np.floor(orientation) / 10) - 1
                weight = vote_strength[i, j]
                hist[bin_number] += weight
                # a.append(np.degrees(theta[i, j]))

        max_bin_count = np.argmax(hist)
        dominant_orientation = np.argmax(hist) * (1 / 36 * 360)
        new_interest_pts.append([x, y, dominant_orientation])

    return new_interest_pts


def find_interest_points(src, thresh_percent, saveCornerImage, savedImagePath):
    # Convert to image to gray scale
    grayscale_img = np.float32(cv.cvtColor(src, cv.COLOR_BGR2GRAY))

    # Calculate image gradient for x and y
    Ix = gradient_x(grayscale_img)
    Iy = gradient_y(grayscale_img)

    harris_response = calculate_harris_corner_response(Ix, Iy, 3)
    descriptors_interest_points = harris_response.copy()
    interest_points = []
    key_points = []

    # Source:
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html
    thresh = thresh_percent * harris_response.max()
    # End source

    # Harris corner
    harris_corners = draw_interest_pts(src, harris_response, thresh, descriptors_interest_points, interest_points)
    if saveCornerImage:
        print("Saving Harris Corner Response " + savedImagePath)
        cv.imwrite(savedImagePath, harris_corners)

    #  KeyPoint (float x, float y, float _size, float _angle=-1, float _response=0, int _octave=0, int _class_id=-1)
    # for point in interest_points:
    #     key_points.append(cv.KeyPoint(point[0], point[1], _size=3))
    #
    # return key_points

    return harris_corners

import cv2 as cv
from src import HarrisCornerDetection
from src.PanoramaStitching import stitch_two_images
import os

harris_threshold = 0.20
ransacIterations = 100
ransacThreshold = 5


def main():
    # Load Boxes, Rainier1 and Rainier2 images
    boxes = cv.imread("project_images/Boxes.png")
    rainier1 = cv.imread("project_images/Rainier1.png")
    rainier2 = cv.imread("project_images/Rainier2.png")

    # Create output folder
    create_directory("project_images/output")

    # Part 1: Harris Corner Detection
    # 1A. Harris Corner for Boxes.png
    boxes_corners = HarrisCornerDetection.find_interest_points(boxes, harris_threshold,
                                                               saveCornerImage=True,
                                                               savedImagePath="project_images/output/1a.png")
    # 1B. Harris Corner for Rainier1.png
    rainier1_corners = HarrisCornerDetection.find_interest_points(rainier1, harris_threshold,
                                                                  saveCornerImage=True,
                                                                  savedImagePath="project_images/output/1b.png")
    # 1C. Harris Corner for Rainier2.png
    rainier2_corners = HarrisCornerDetection.find_interest_points(rainier2, harris_threshold,
                                                                  saveCornerImage=True,
                                                                  savedImagePath="project_images/output/1c.png")
    cv.imshow("1a. Boxes Harris Corner Detection (src/project_images/output/1a.png)", boxes_corners)
    cv.imshow("1b. Rainier1 Harris Corner Detection (src/project_images/output/1b.png)", rainier1_corners)
    cv.imshow("1c. Rainier2 Harris Corner Detection (src/project_images/output/1c.png)", rainier2_corners)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # Part 2, 3 and Bonus #1
    stitch_rainier(rainier1, rainier2, ransacIterations=ransacIterations, ransacThreshold=ransacThreshold)

    # Bonus #2 Stitching images taken with my phone
    japan1 = cv.imread("project_images/bonus_images/Japan1.jpg")
    japan2 = cv.imread("project_images/bonus_images/Japan2.JPG")
    japan3 = cv.imread("project_images/bonus_images/Japan3.JPG")
    bonus2_stitch_japan(japan1, japan2, japan3, ransacIterations=ransacIterations, ransacThreshold=ransacThreshold)

    # Bonus #3 Hanging
    """
    hanging1 = cv.imread("project_images/Hanging1.png")
    hanging2 = cv.imread("project_images/Hanging2.png")
    hanging_stitched = stitch_two_images(hanging1, hanging2,
                                         ransacDisplayName="13. RANSAC Matches for Hanging1 and Hanging2 "
                                                           "(src/project_images/output/Bonus3a_Hanging_RANSAC.png)",
                                         siftDisplayName="",
                                         siftFilePath="",
                                         saveSiftMatches=False,
                                         saveRansacMatches=True,
                                         ransacFilePath="project_images/output/Bonus3a_Hanging_RANSAC.png",
                                         ransacIterations=ransacIterations,
                                         ransacThreshold=ransacThreshold
                                         )
    cv.imshow("14. Hanging Stitched (src/project_images/output/Bonus3b_Hanging_Stitched.png)", hanging_stitched)
    cv.imwrite("project_images/output/Bonus3b_Hanging_Stitched.png", hanging_stitched)
    cv.waitKey(0)
    cv.destroyAllWindows()
    """


# Source: https://www.tutorialspoint.com/How-can-I-create-a-directory-if-it-does-not-exist-using-Python
def create_directory(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def stitch_rainier(rainier1, rainier2, ransacIterations, ransacThreshold):
    # Stitching Rainier1 and Rainier2
    print("Stitching Rainier1 and Rainier2")
    stitched_image = stitch_two_images(rainier1, rainier2,
                                       siftDisplayName="2. SIFT matches for Rainier 1-2 (src/project_images/output/2.png)",
                                       siftFilePath="project_images/output/2.png",
                                       saveSiftMatches=True,
                                       ransacDisplayName="3. RANSAC Matches for Rainier1 and Rainier2 (src/project_images/output/3.png)",
                                       saveRansacMatches=True,
                                       ransacFilePath="project_images/output/3.png",
                                       ransacIterations=ransacIterations,
                                       ransacThreshold=ransacThreshold
                                       )
    Rainier1_2_file_path = "project_images/output/4.png"
    cv.imwrite(Rainier1_2_file_path, stitched_image)  # Save Rainier1 and Rainier 2 Stitched to project_images/4.png
    print("Rainier1 and Rainier2 Stitched saved to " + Rainier1_2_file_path)

    cv.imshow("4. Stitched Rainier1 and Rainier2 (R1-2) (src/project_images/output/4.png)", stitched_image)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # Stitching Rainier3, Rainier4, Rainier5, Rainier6
    for i in range(3, 7):  # We want to load Rainier 3-6
        image = cv.imread("project_images/Rainier" + str(i) + ".png")
        print("Stitching Rainier" + str(i))
        stitched_image = stitch_two_images(stitched_image, image,
                                           siftDisplayName="",
                                           siftFilePath="",
                                           saveSiftMatches=False,
                                           ransacDisplayName="{}. RANSAC Matches for R1-{} and Rainier{} (R1-{}) "
                                           .format(i+2, i-1, i, i),
                                           saveRansacMatches=False,
                                           ransacFilePath="",
                                           ransacIterations=ransacIterations,
                                           ransacThreshold=ransacThreshold
                                           )

    stitched_file_path = "project_images/output/5.png"
    cv.imwrite(stitched_file_path, stitched_image)
    print("Rainier All Stitched saved to " + stitched_file_path)
    # Resize for displaying purposes only, the output is saved in original size
    # Source: https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
    scale_percent = 100
    width = int(stitched_image.shape[1] * scale_percent / 100)
    height = int(stitched_image.shape[0] * scale_percent / 100)
    dsize = (width, height)
    stitched_image = cv.resize(stitched_image, dsize, interpolation=cv.INTER_AREA)
    # End source

    cv.imshow("9. Stitched Rainier1-6 (Scaled 50% for Displaying) (src/project_images/output5.png)", stitched_image)
    cv.waitKey(0)
    cv.destroyAllWindows()


def bonus2_stitch_japan(japan1, japan2, japan3, ransacIterations, ransacThreshold):
    jp1_jp2_stitched = stitch_two_images(japan1, japan2,
                                         siftDisplayName="",
                                         siftFilePath="",
                                         saveSiftMatches=False,
                                         ransacDisplayName="10. RANSAC Matches for Japan1 and Japan2 (JP1-2) "
                                                           "(src/project_images/output/Bonus2a_RANSAC_jp1_2.png) ",
                                         saveRansacMatches=True,
                                         ransacFilePath="project_images/output/Bonus2a_RANSAC_jp1_2.png",
                                         ransacIterations=ransacIterations,
                                         ransacThreshold=ransacThreshold)
    jp_all_stitched = stitch_two_images(jp1_jp2_stitched, japan3,
                                        siftDisplayName="",
                                        siftFilePath="",
                                        saveSiftMatches=False,
                                        ransacDisplayName="11. JP1-3 RANSAC Matches "
                                                          "(src/project_images/output/Bonus2b_RANSAC_jp1_2_3.png)",
                                        saveRansacMatches=True,
                                        ransacFilePath="project_images/output/Bonus2b_RANSAC_jp1_2_3.png",
                                        ransacIterations=ransacIterations,
                                        ransacThreshold=ransacThreshold
                                        )
    jp_stitched_path = "project_images/output/Bonus2c_Japan_AllStitched.png"
    cv.imwrite(jp_stitched_path, jp_all_stitched)
    print("Stitched Japan1-3 saved to " + jp_stitched_path)
    cv.imshow("12. Stitched Japan1-3 (src/project_images/output/Bonus2c_Japan_AllStitched.png)", jp_all_stitched)
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()

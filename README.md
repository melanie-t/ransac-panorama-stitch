# RANSAC Panorama Stitching

Python Version 3.7

## THE PROJECT
This project stitches images together to create a Panorama. Images are taken from different perspectives and transformed to fit together by using SIFT feature detection and RANSAC algorithm for homography transformations.


## BONUSES IMPLEMENTED
* Bonus #1
<br>The image of Rainier AllStitched is saved at src/project_images/5.png

* Bonus #2
<br>The images that I used for Bonus #2 are found in src/project_images/bonus_images, and they were taken with my phone. The resulting stitched image is saved at src/project_images/Bonus2c_Japan_AllStitched.png

* Bonus #3
<br>I commented out the code, because I used SIFT to stitch Hanging1 and Hanging2. I was trying to implement my own descriptor, but couldn't get it to work.

## SET UP INSTRUCTIONS
1.	Ensure that your Python version is 3.7 and pip is installed
    * Python 3.7	https://www.python.org/downloads/release/python-370/
    * pip 		https://pip.pypa.io/en/stable/installing/

2. 	Open the project folder (Project_RANSAC) as a Python project in your choice of IDE (i.e. PyCharm)
    <br>Set the working directory is set to `/Project_RANSAC/src`

3.	Select Python 3.7 as your interpreter
<br> OpenCV Contrib v.3.4.2.16 files are found in the project folder.
    * Required Packages
        * numpy
        <br>`pip install numpy`
        * OpenCV Contrib v.3.4.2.16
            * 64-bit: opencv_contrib_python-3.4.2.16-cp37-cp37m-win_amd64.whl
            <br>`pip install opencv_contrib_python-3.4.2.16-cp37-cp37m-win_amd64.whl`
            * 32-bit: opencv_contrib_python-3.4.2.16-cp37-cp37m-win32.whl
            <br>`pip install opencv_contrib_python-3.4.2.16-cp37-cp37m-win32.whl`

## RUNNING THE PROJECT
* Harris Corner Response threshold, RANSAC Iterations and RANSAC threshold can be specified in the global variables found in `Main.py` (Line 6-8)
1.	Run `Main.py` to execute the program
2.	Output images are saved in src/project_images/output. 
<br>For testing purposes, you can delete the output folder.
<br>To go to the next image, press spacebar
<br>The sequence of the images are as follows:

			1.	a. Boxes Harris Corner Detection 				(src/project_images/output/1a.png)
				b. Rainier1 Harris Corner Detection 			(src/project_images/output/1b.png)
				c. Rainier2 Harris Corner Detection 			(src/project_images/output/1c.png)
			2.	SIFT matches for Rainier 1-2 					(src/project_images/output/2.png)
			3. 	RANSAC Matches for Rainier1 and Rainier2 		(src/project_images/output/3.png)
			4. 	Stitched Rainier1 and Rainier2 (R1-2) 			(src/project_images/output/4.png)

			(BONUS)

			5. 	RANSAC Matches for R1-2 and Rainier3 (R1-3)
			6. 	RANSAC Matches for R1-3 and Rainier4 (R1-4)
			7. 	RANSAC Matches for R1-4 and Rainier5 (R1-5)
			8. 	RANSAC Matches for R1-5 and Rainier6 (R1-6)
			9.	Stitched Rainier1-6	(Scaled 50% For Displaying) (src/project_images/output/5.png)
			10.	RANSAC Matches for Japan1 and Japan2 (JP1-2) 	(src/project_images/output/Bonus2a_RANSAC_jp1_2.png)
			11.	RANSAC Matches for JP1-2 and Japan3 (JP1-3)		(src/project_images/output/Bonus2b_RANSAC_jp1_2_3.png")
			12. Stitched Japan1-3 								(src/project_images/output/Bonus2c_Japan_AllStitched.png)
			13. RANSAC Matches for Hanging1 and Hanging1-2		(src/project_images/output/Bonus3a_Hanging_RANSAC.png)
			14. Stitched Hanging1-2								(src/project_images/output/Bonus3b_Hanging_Stitched.png)

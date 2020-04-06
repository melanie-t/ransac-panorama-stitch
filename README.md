# RANSAC Panorama Stitching

Python Version 3.7

# THE PROJECT
This project stitches images together to create a Panorama. Images are taken from different perspectives and transformed to fit together by using SIFT feature detection and RANSAC algorithm for homography transformations.

# SET UP INSTRUCTIONS
1.	Ensure that your Python version is 3.7 and pip is installed
    * Python 3.7<br>https://www.python.org/downloads/release/python-370/
    * pip<br>https://pip.pypa.io/en/stable/installing/

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

# RUNNING THE PROJECT
* Harris Corner Response threshold, RANSAC Iterations and RANSAC threshold can be specified in the global variables found in `Main.py` (Line 6-8)
1.	Run `Main.py` to execute the program
2.	To go to the next image, press any key (excluding Esc). Output images are saved in `src/project_images/output`
	* The sequence of the images are as follows:
		1.	a. Boxes Harris Corner Detection 				
			b. Rainier1 Harris Corner Detection 			
			c. Rainier2 Harris Corner Detection 			
		2. SIFT matches for Rainier 1-2 				
		3. RANSAC Matches for Rainier1 and Rainier2 		
		4. Stitched Rainier1 and Rainier2 (R1-2) 			
		5. RANSAC Matches for R1-2 and Rainier3 (R1-3)
		6. RANSAC Matches for R1-3 and Rainier4 (R1-4)
		7. RANSAC Matches for R1-4 and Rainier5 (R1-5)
		8. RANSAC Matches for R1-5 and Rainier6 (R1-6)
		9. Stitched Rainier1-6	(Scaled 50% For Displaying) 
		10. RANSAC Matches for Japan1 and Japan2 (JP1-2) 	
		11. RANSAC Matches for JP1-2 and Japan3 (JP1-3)		
		12. Stitched Japan1-3 								
		13. RANSAC Matches for Hanging1 and Hanging1-2		
		14. Stitched Hanging1-2						

# OpenCV-Distance-Angle-Demo

Check out the Medium article [here!](https://medium.com/@ariwasch/how-to-track-distance-and-angle-of-an-object-using-opencv-1f1966d418b4)

Using this demo, you can set a target color and enter the variables to get the distance and angle of the target object. 

<img src="https://cdn-images-1.medium.com/max/1200/1*DQuAcCjhgQDZnid2ZfNttg.gif" width="361.5" height="538.875" /> <img src="https://cdn-images-1.medium.com/max/1200/1*ki4GDHUC_ea4l8Gzf5dqIw.png" width="361.5" height="538.875" />

### Input Variables
* Known Width: width of the object in any physical unit (Ex: cm, inches)
* Known Height: height of the object in any physical unit (Ex: cm, inches)
* Known distance from object: any distance from the camera to the object in the chosen unit above. 
* Pixel height at above distance from camera: pixel height of the object when the distance is the same as the known distance from object.

### Side Note
To prevent swapping of the width and height, this demo locks the width and height meaning that one is always greater than the other. This can cause inaccurate measurements after reaching a certain angle.

## Installation and setup
* git clone "https://github.com/ariwasch/OpenCV-Distance-Angle-Demo"
* pip3 install -r requirements.txt
* python3 main.py


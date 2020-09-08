# LidarCommunication
Progam for communicating with the Benewake CE30-C LiDAR
At the moment it is only compatible with python 2.7 due to socket problems. 

The purpous of the program is to start recording at a given command, at a given FPS up to 20 Hz wich is the natural limit of the CE30-C.
The program saves the point cloud files induvidualy in a folder in .txt format, one file for each scan. 

Run the program with the command (granted you have python 2.7 installed):

$ py -2 main.py 


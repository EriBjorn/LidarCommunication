import os
import shutil
import signal
import lidar_tcp as com
from lidar_tcp import _recvdata, _recvhex, _sendmsg, sock
from undistortion import _init_fisheye_map, _remap
import numpy as np

import time


#
#
#

# Size of matrix

WIDTH = 320
HEIGHT = 24
TOTALDATA = WIDTH * HEIGHT * 2



#
#
#

# camera intrinsic matrix

cameraMatrix = np.zeros((3, 3))
cameraMatrix[0, 0] = 149.905
cameraMatrix[0, 1] = 0.0
cameraMatrix[0, 2] = 159.5
cameraMatrix[1, 1] = 150.24
cameraMatrix[1, 2] = 11.5
cameraMatrix[2, 2] = 1.0




# def format():
#     outfile.point_format
#     print("Format:\n")
#     for spec in outfile.point_format:
#         print(spec.name)


#
#
#

# distortion coefficients

distCoeffs = np.array([-0.059868055, -0.001303471, 0.010260736, -0.006102915])

#
#
#

# init undistorted map

mapX, mapY = _init_fisheye_map(cameraMatrix, distCoeffs, 24, 660)


# ctrl+C to stop LiDAR and quit
def quit(signum, frame):
    _sendmsg(com.sock, com.cmdStop)
    _sendmsg(com.sock, com.cmdDisconnect)


signal.signal(signal.SIGINT, quit)
signal.signal(signal.SIGTERM, quit)

#
#
#

# TODO format?

# Saving point cloud to specific file. parm = name of file. must end i .las or .npy

#data = open("pointcloud.txt", "w")
#data = open("pointcloud.npy", "w")
#data = open3d.io.write_point_cloud("pointcloud.ply", print_progress=True)


#
#
#

# Makes a directory for saving the files

filename = raw_input("Name of file: ")


if os.path.isdir(filename):
    shutil.rmtree(filename)
directory = filename
path = filename
os.makedirs(path)
print("Directory '% s' created" % directory)


filename_csv = filename+"/csv"
os.mkdir(filename_csv)

filename_txt = filename+"/txt"
os.mkdir(filename_txt)

filename_npy = filename+"/npy"
os.mkdir(filename_npy)


#
#
#

# Starts the show.


def main():
    fps = raw_input("Set FPS : ")
    com.connection()                                # Establish the TCP socket connection
    _sendmsg(sock, "setFps " + str(fps))            # Edit the number after "setFps" to set the fps(hz)
    _sendmsg(sock, com.cmdStart)


    #_sendmsg(sock, com.nearestPointOn)

    frame_n = 0
    n = 50
    while True:
        try:
            for i in range(n):

                data_csv = open(str(filename_csv) + "/pcl%s.csv" % i, 'w')
                data_txt = open(str(filename_txt) + "/pcl%s.txt" % i, 'w')
                data_npy = open(str(filename_npy) + "/pcl%s.npy" % i, 'w')

                distData = _recvdata(sock, HEIGHT, WIDTH)
                ampData = _recvdata(sock, HEIGHT, WIDTH)
                nearPt = _recvhex(sock, 3)

                if distData is None or ampData is None or nearPt is None:
                    break

                # Saving to txt format
                data_csv.write("Frame " + str(frame_n) + ':\n')
                data_csv.write("Distance:\n")
                np.savetxt(data_csv, distData, fmt='%d', newline='\n', delimiter=',')
                data_csv.write("Amplitude:\n")
                np.savetxt(data_csv, ampData, fmt='%d', newline='\n', delimiter=',')



                data_txt.write("Frame " + str(frame_n) + ':\n')
                data_txt.write("Distance:\n")
                np.savetxt(data_txt, distData, fmt='%d', newline='\n', delimiter=' ')
                data_txt.write("Amplitude:\n")
                np.savetxt(data_txt, ampData, fmt='%d', newline='\n', delimiter=' ')


                ######### undistorted ###########

                # saving undistorted to csv
                undistortData = _remap(distData, mapX, mapY, 24, 660)
                data_csv.write("Undistorted distance:\n")
                np.savetxt(data_csv, undistortData, fmt='%d', newline='\n', delimiter=',')

                # saving undistored to txt
                data_txt.write("Undistorted distance:\n")
                np.savetxt(data_txt, undistortData, fmt='%d', newline='\n', delimiter=' ')


                ####### Saving to numpy array ##########
                np.save(data_npy, distData)
                np.save(data_npy, ampData)
                np.save(data_npy, undistortData)


                # data.write("Nearest Point " + "\n")
                # np.savetxt(data, nearPt, fmt='%d', newline='\n', delimiter=' ')

                frame_n += 1

                #if frame_n >= n:
            _sendmsg(sock, com.cmdStop)

        except Exception:
            break

    com.quit()


if __name__ == '__main__':
    main()

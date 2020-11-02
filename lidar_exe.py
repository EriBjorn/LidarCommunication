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

# init undistortion map

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

# Saving pointcloud to specific file. parm = name of file. must end i .las or .npy

#data = open("pointcloud.txt", "w")
#data = open("pointcloud.npy", "w")
#data = open3d.io.write_point_cloud("pointcloud.ply", print_progress=True)


#
#
#

# Makes a directory for saving the files (edit path to avoid error)

filename = raw_input("Name of file: ")


if os.path.isdir(filename):
    shutil.rmtree(filename)
directory = filename
parent_dir = "C:\Users\ebjor\Documents\Python Scripts\Lidar\LidarCommunication"
path = os.path.join(parent_dir, directory)

os.makedirs(path)
print("Directory '% s' created" % directory)


def main():
    fps = raw_input("Set FPS : ")
    com.connection()                      # Establish the TCP socket connection
    _sendmsg(sock, "setFps " + str(fps))            # Edit the number after "setFps" to set the fps(hz)
    _sendmsg(sock, com.cmdStart)

    #_sendmsg(sock, com.nearestPointOn)

    frame_n = 0
    n = 50
    while True:
        try:
            for i in range(n):

                data = open("pointCloud/pcl%s.txt" % i, 'w')

                distData = _recvdata(sock, HEIGHT, WIDTH)
                ampData = _recvdata(sock, HEIGHT, WIDTH)
                nearPt = _recvhex(sock, 3)
                if distData is None or ampData is None or nearPt is None:
                    break

                data.write("Frame " + str(frame_n) + ':\n')
                data.write("Distance:\n")
                np.savetxt(data, distData, fmt='%d', newline='\n', delimiter=' ')
                # np.save(data, distData)
                data.write("Amplitude:\n")
                np.savetxt(data, ampData, fmt='%d', newline='\n', delimiter=' ')
                # np.save(data, ampData)

                # undistorted
                undistortData = _remap(distData, mapX, mapY, 24, 660)
                data.write("Undistorted distance:\n")
                np.savetxt(data, undistortData, fmt='%d', newline='\n', delimiter=' ')
                # np.save(data, undistortData)

                # data.write("Nearest Point " + "\n")
                # np.savetxt(data, nearPt, fmt='%d', newline='\n', delimiter=' ')

                frame_n +=
            _sendmsg(sock, com.cmdStop)

        except Exception:
            break

    com.quit()


if __name__ == '__main__':
    main()

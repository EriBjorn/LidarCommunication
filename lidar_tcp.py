import socket
import time
import numpy as np
import signal

# Client side -socket communication.

start = time.time()
debugging = True


def debug(text):
    if debugging:
        print(text)


#
#
#


HOST = '192.168.1.80'  # IP of the Benewake ce30c
PORT = 50660  # Communication port for ce30c

cmdStart = "getDistanceAndAmplitudeSorted"                     # Command to START measurement. Hz is default 20 fps
cmdStartTrigger = "getDistanceAndAmplitudeSortedTimes times"   # Command to START measurement, Trigger mode
cmdStop = "join"                                               # Command to STOP measurement
cmdDisconnect = "disconnect"                                   # Command to kill TCP-socket
setFps = "setFps 1"                                          # Command to set FPS of lidar, default is 20 Hz
nearestPointOn = "enableFeatures 1"                            # Command to Returns distance of nearest point
nearestPointOff = "disableFeatures 1"                          # Command to disable Returns distance of nearest point




#
#
#

# Initialise "sock" as socket variable.

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



#
#
#

# Send TCP message

def _sendmsg(s, _msg):
    msg_len = len(_msg)
    total_sent = 0
    _msg += "\0" * (50 - msg_len)
    b = bytearray(_msg, 'utf8')
    while total_sent < 50:
        chunk_len = s.send(b[total_sent:])
        total_sent += chunk_len


#
#
#

# Connect with TCP socket


def connection():
    sock.setsockopt(socket.SOL_SOCKET, socket.TCP_NODELAY, 1)
    sock.connect(('192.168.1.80', 50660))
    sock.settimeout(2)
    print("connected")


#
#
#

# Receiving nearest point

def _recvhex(sock, _len):
    string = ''
    bytes_read = 0
    while bytes_read < _len:
        try:
            chunk = sock.recv(_len - bytes_read)
        except socket.timeout:
            print("Receiver timeout")
            return None
        bytes_read += len(chunk)
        string += chunk
    array = np.fromstring(string, dtype=np.ubyte)
    return array


#
#
#

# Recive incoming TCP traffic


def _recvdata(s, _row, _colum):
    string = ''
    bytes_read = 0
    bytes_n = _row * _colum * 2
    while bytes_read < bytes_n:
        try:
            chunk = s.recv(bytes_n - bytes_read)
        except socket.timeout:
            print("Receiver timeout")
            return None
        bytes_read += len(chunk)
        string += chunk
    array = np.fromstring(string, dtype=np.uint16)
    array.shape = (_row, _colum)
    return array


#
#
#

# Initiates communication

def starter():
    _sendmsg(sock, cmdStart)  # Send message to start recording
    debug("Start Command sent \n")


#
#
#

# Sets FPS (Must be an integer between 0 and 20)

def setFPS(command, hz):
    fps = command + hz
    print(fps)
    _sendmsg(sock, fps)




#
#
#

# Stops communication 

def quit():
    debug("entered quit")
    _sendmsg(sock, cmdStop)  # Send message to stop recording
    debug("stop command sent")
    _sendmsg(sock, cmdDisconnect)  # Send message to end socket communication
    debug("disconnected")

#
#
#

#


# end = time.time()
# print(f"\nTime to read: {round(end - start, 5)} seconds.")

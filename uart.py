#!/usr/bin/env python
# serial_port_loopback.py
# Will also work on Python3.
# Serial port testing for a RaspberryPi.

from __future__ import print_function
import serial
import time
import struct
import matplotlib.pyplot as plt
import numpy as np
#import numpy as np

def main():
    #send_test_string (SET_POWER_ON())
    send_test_string (GET_DISTANCE())
    
   
def GET_DISTANCE():
    test_string = bytearray()
    test_string.append(0xF5)
    test_string.append(0x20)
    test_string.append(0x00)
    for i in range(7):
        test_string.append(0x00)
    test_string.append(0x98)
    test_string.append(0x53)
    test_string.append(0xE9)
    test_string.append(0x9B)
    return test_string
def SET_POWER_OFF():
    test_string = bytearray()
    test_string.append(0xF5)
    test_string.append(0x40)
    test_string.append(0x00)
    for i in range(7):
        test_string.append(0x00)
        
    # test_string.append(0x9C)
    # test_string.append(0xD7)
    # test_string.append(0xD6)
    # test_string.append(0x91)
    test_string.append(0x56)
    test_string.append(0x0B)
    test_string.append(0x77)
    test_string.append(0xCA)
    print (test_string)
    return test_string
def SET_POWER_ON():
    test_string = bytearray()
    test_string.append(0xF5)
    test_string.append(0x40)
    test_string.append(0x01)
    for i in range(7):
        test_string.append(0x00)    
    test_string.append(0x9C)
    test_string.append(0xD7)
    test_string.append(0xD6)
    test_string.append(0x91)
    #print (test_string)
    return test_string
#test_string = b"Testing 1 2 3 4" ### Will also work

#port_list = ["/dev/serial0", "/dev/ttyAMA0", "/dev/serial1", "/dev/ttyS0"]

#for port in port_list:
def send_test_string (test_string):
    port = "/dev/serial0"
    #WRITE

    try:
        serialPort = serial.Serial(port, 921600, timeout = 2)
        serialPort.flushInput()
        serialPort.flushOutput()
        print("Opened port", port, "for testing:")
        bytes_sent = serialPort  .write(test_string)
        print ("Sent", bytes_sent, "bytes")
    except IOError:
        print ("Failed at", port, "\n")
    except KeyboardInterrupt:
        print ("interupt at", port, "\n")
        time.sleep(.1)

    #READ
    i=0
    a = np.zeros((64,1))
    try:
        for i in range (65):
            
            loopback = serialPort.read(4)
            combined = struct.unpack("<I", loopback)[0]
            if ( i > 0):
                a[i-1] = combined
            #print (i-1, "=   ",combined)#,"\n")
    except IOError:
        print ("Failed at", port, "\n")
        serialPort.close()
    except KeyboardInterrupt:
        print ("interupt at", port, "\n")
        serialPort.close()
        time.sleep(.1)
    print("hello")
    plt.imshow(a.reshape(8,8), cmap='hot', interpolation='nearest',vmax=30000)
    plt.show()
if __name__ == "__main__":
    # execute only if run as a script
    main()


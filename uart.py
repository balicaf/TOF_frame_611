#!/usr/bin/env python
# serial_port_loopback.py
# Will also work on Python3.
# Serial port testing for a RaspberryPi.

from __future__ import print_function
import serial
import time
import struct
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import matplotlib.animation as animation
import time
import csv

def main():
    #send_test_string (SET_POWER_ON())
    send_test_string (GET_DISTANCE())
    #send_test_string (SET_POWER_OFF())
   
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
    #   n,print (test_string)
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
    a = np.zeros((64,1))
    if test_string[0:2] == b'\xf5@':# == "GET_DISTANCE()":
        nbFrames = 1
    else:# test_string == "SET_POWER_OFF()" or "SET_POWER_ON()":
        nbFrames = 128
    b = np.zeros((64,nbFrames))
    fig = plt.figure()
    ims = []
    tic = time.perf_counter()
    print("go!!!!") 
    for j in range(nbFrames):
        try:
            serialPort = serial.Serial(port, 921600, timeout = 2)
            serialPort.flushInput()
            serialPort.flushOutput()
            #print("Opened port", port, "for testing:")
            bytes_sent = serialPort  .write(test_string)
            #print ("Sent", bytes_sent, "bytes")
        except IOError:
            print ("Failed at", port, "\n")
        except KeyboardInterrupt:
            print ("interupt at", port, "\n")
            time.sleep(.1)

    #READ
        if test_string[0:2] == b'\xf5@':#"SET_POWER_OFF()" or "SET_POWER_ON()":
            print(test_string[0:2])
            return
        else:
            try:
                if j!=0:
                    time2wait =0.033 - (time.perf_counter()-timeSpent)
                    #print(time2wait)
                    if time2wait>0:
                        time.sleep(time2wait)#to have 30 fps exactly
                timeSpent = time.perf_counter()            
                
                for i in range (65):

                    loopback = serialPort.read(4)
                    combined = struct.unpack("<I", loopback)[0]
                    if ( i > 0):
                        a[i-1] = combined
                        b[i-1][j] = combined
                    #print (i-1, "=   ",combined)#,"\n")
            except IOError:
                print ("Failed at", port, "\n")
                serialPort.close()
            except KeyboardInterrupt:
                print ("interupt at", port, "\n")
                serialPort.close()
                time.sleep(.1)
            #print("hello")
            im = plt.imshow(a.reshape(8,8),origin='lower',
                            cmap='hot',
                            interpolation='nearest',
                            vmin=3000, vmax=25000)
                            #norm=colors.LogNorm(vmin=3000, vmax=90000))
            ims.append([im])
#    plt.show()    
#    bMed = np.median(b, axis=1)
#    im = plt.imshow(bMed.reshape(8,8), cmap='hot',
#                        interpolation='nearest')#,
#                        vmin=3000, vmax=90000)
#plt.show()
    toc = time.perf_counter()
    print(toc-tic)
#         with open("new_file3.csv","w+") as my_csv:
#             csvWriter = csv.writer(my_csv,delimiter=',')
#             csvWriter.writerows(b)
    ani = animation.ArtistAnimation(fig, ims, interval=33,
                                    blit=True, repeat_delay=1000)
    #ani.save('dynamic-imageT2.mp4')#save video as mp4
    toc = time.perf_counter()
    print(toc-tic)
    plt.show()#just show the figure
if __name__ == "__main__":
    # execute only if run as a script
    main()


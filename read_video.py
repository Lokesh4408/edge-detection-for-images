import cv2
import numpy as np
import sys
#import os

path = sys.argv[1]

cap = cv2.VideoCapture(path)

if (cap.isOpened()==False):
    print("Error opening video stream or file")


while(cap.isOpened()):
    ret, frame = cap.read()
    if(ret==True):
        #display the resulting frame
        cv2.imshow('output', frame) 
        if cv2.waitKey(10) & 0xFF == ord('q'):
             break
    else:
        break         
               
cap.release()
cv2.destroyAllWindows() 


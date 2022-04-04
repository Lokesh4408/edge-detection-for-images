import numpy as np
import cv2

#Program to capture a video from a camera and display Original and R,G,B, components live on the screen

cap = cv2.VideoCapture(2)

while(True):
    # Capture frame-by-frame
    [ret, frame] = cap.read()
    cv2.imshow('Original',frame)

    # Display the resulting frame
    k=cv2.waitKey(1)
    
    if k==27:
       break
    elif k==32:
       cv2.imwrite('/home/lokesh/Desktop/Fraunhofer/sample6.jpg', frame) 
       cv2.imshow('Snapshot',frame) 

    if k== ord('q'):
       break     

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

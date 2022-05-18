import cv2
import numpy as np

cap = cv2.VideoCapture(0)

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('RGB_captured.mp4', fourcc, 60.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    b,g,r = cv2.split(frame)
    frame = cv2.merge([r,g,b])

    if(ret==True):
        #out.write(frame)
        cv2.imshow('rgb_frame', frame) 
        if cv2.waitKey(10) & 0xFF == ord('q'):
             break
    else:
        print("Error: Failed to access camera")
        break         
               
cap.release()
cv2.destroyAllWindows() 


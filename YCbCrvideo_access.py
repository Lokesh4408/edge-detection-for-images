import cv2
import numpy as np

cap = cv2.VideoCapture(0)

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('RGB_captured.mp4', fourcc, 60.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    #YCrCb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)#...if input is BGR
    Y = (0.299*frame[:,:,2])/255+ (0.587*frame[:,:,1])/255+(0.114*frame[:,:,0])/255
    Cb = ((0.4997*frame[:,:,0])/255-(0.16864*frame[:,:,2])/255-(0.33107*frame[:,:,1])/255)+0.5
    Cr = (0.499813*frame[:,:,2])/255-(0.418531*frame[:,:,1])/255-(0.081282*frame[:,:,0])/255+0.5

    if(ret==True):
        #out.write(frame)
        cv2.imshow('Original', frame)
        #cv2.imshow('YCbCr', YCbCr)
        cv2.imshow('Luminance Y', Y)
        cv2.imshow('Cb component', Cb)
        cv2.imshow('Cr component', Cr)
         
        if cv2.waitKey(10) & 0xFF == ord('q'):
             break
    else:
        print("Error: Failed to access camera")
        break         
               
cap.release()
cv2.destroyAllWindows() 


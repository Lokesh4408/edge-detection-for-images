import numpy as np
import cv2
import pickle
import time
import scipy.signal
import utils as vc

#downsample factor
N = 8
cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print('width',width)
print('height',height)
cap_duration = 60 #seconds
f=open('video_raw_data_uint8.txt', 'wb')

start = time.time()
#lowpass filter
filt1 = np.ones((8,8))/8
filt2 = scipy.signal.convolve2d(filt1,filt1)/8
filteron = False

#while(int(time.time() - start) < cap_duration):  
for n in range(25):
    print('frame no:', n)
    ret, frame = cap.read()
    [r, c, p] = frame.shape
    Cb_ds = np.zeros((r,c))
    Cr_ds = np.zeros((r,c))

    if ret==True:
        YCbCr = vc.rgb2ycbcr(frame)
        #ycbcr_cs = np.zeros([r, c, p], dtype='uint8')
        ycbcr_cs = vc.chroma_subsampling_4_2_0(frame)
        #out.write(YCbCr)# writing frames into a video file
        cv2.imshow('output_original',frame)
        #cv2.imshow('YCbCr', YCbCr)
        #cv2.imshow('ycbcr_chromasampled', ycbcr_cs)
        if filteron == True:
           YCbCr[:,:,1] = scipy.signal.convolve2d(YCbCr[:,:,1],filt2,mode='same')
           YCbCr[:,:,2] = scipy.signal.convolve2d(YCbCr[:,:,2],filt2,mode='same')
        #downsample filtered frame
        Cb_ds[::N,::N] = YCbCr[::N,::N,1]
        Cr_ds[::N,::N] = YCbCr[::N,::N,2]
        cv2.imshow('downsampled_Cb after filtering', Cb_ds)
        cv2.imshow('downsampled_Cr after filtering', Cr_ds)
        #for upsampling and filtering
        '''if filteron == True:
            Cb_filt = scipy.signal.convolve2d(Cb_ds,filt2,mode='same')
            Cr_filt = scipy.signal.convolve2d(Cr_ds,filt2,mode='same')
        else:
            Cb_filt = Cb_ds.copy()
            Cr_filt = Cr_ds.copy()'''
        #printing them into windows
        #cv2.putText(Cb_ds,"Down- and upsampling and LP filtering Demo", (20,50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,128,128))
        cv2.putText(Cb_ds,"Toggle LP filter on/off: key f", (20,100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,128,128))
        cv2.putText(Cb_ds,"Quit: key q", (20,150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,128,128))
        cv2.imshow('Downsampled Cb-component',Cb_ds)
        #Here goes the processing to reduce data... 
        #reduced = YCbCr.copy()#frame.copy()
        reduced = ycbcr_cs.copy()
        #reduced = downsampled
        reduced=np.array(reduced,dtype='uint8')#reduced for the Cb and Cr components use the int8 type (for regular frame: uint8)
        #"Serialize" the captured video frame (convert it to a string) 
        #using pickle, and write/append it to file f:
        #pickle.dump(reduced,f)
        key = cv2.waitKey(50) & 0xFF
        if key == ord('f'):
            filteron = not filteron
        if key == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
#f.close()
cv2.destroyAllWindows()

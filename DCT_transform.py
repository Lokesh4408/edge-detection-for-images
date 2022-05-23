import numpy as np
import cv2
import sys
import pickle

import vc_utilities as vc

# Constants
window_names = {
    "rgb": "Video RGB - live",
    "y_dct": "Y_DCT",
    "cb_dct": "Cb420_DCT",
    "cr_dct": "Cr420_DCT",
}

original_filename = "videorecord.txt"
original_ycbcr_filename = "videorecord_ycbcr.txt"
compressed_filename = "videorecord_DS_DCT_compressed.txt"

g_quality_dct = 0.25

# Utilities

def windows_open():
    for (_,window_name) in window_names.items():
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) == False:
            return False
    return True

#=================
# Main Event Loop
#=================

def main(cap, fps, duration, quality=0.25):
    # number of frames to capture during recording
    capture_frames = fps*duration
    # index of frame to record, recording is off if it is >= capture_frames
    rec_frame = capture_frames + 1

    while(True):
        ret, bgr = cap.read()

        if (ret == False):
            break
            
        #show captured frame:
        cv2.imshow(window_names["rgb"], bgr)

        # Processing
        ycbcr = vc.bgr_to_ycbcr(bgr)
        Y, Cb_downsampled, Cr_downsampled = vc.downsample420(ycbcr)
        Y_freqreduction = vc.freqred(Y, quality)
        Cb_freqreduction = vc.freqred(Cb_downsampled, quality)
        Cr_freqreduction = vc.freqred(Cr_downsampled, quality)    

        # Show intermediate
        cv2.imshow(window_names["y_dct"], Y_freqreduction)
        cv2.imshow(window_names["cb_dct"], Cb_freqreduction)
        cv2.imshow(window_names["cr_dct"], Cr_freqreduction)

        cv2.resizeWindow(window_names["y_dct"], Y.shape[::-1])
        cv2.resizeWindow(window_names["cb_dct"], Y.shape[::-1])
        cv2.resizeWindow(window_names["cr_dct"], Y.shape[::-1])

        Y_compressed = Y_freqreduction
        Cb_compressed = Cb_freqreduction
        Cr_compressed = Cr_freqreduction

        #Checks if Recording is running, and dumps Frames to file
        if (rec_frame < capture_frames):
            # write to file
            pickle.dump(bgr, original_file)
            pickle.dump(ycbcr, original_ycbcr_file)
            pickle.dump(Y_compressed, compressed_file)
            pickle.dump(Cb_compressed, compressed_file)
            pickle.dump(Cr_compressed, compressed_file)
            rec_frame += 1
            print("frame: ", rec_frame)

        keycode = cv2.waitKey(1) & 0xFF
        # Press q or Esc quits program
        if keycode == ord('q') or keycode == 27:
            break
        # Press r starts/restarts record for set duration, Resets frame count and reopens the file to reset it
        elif keycode == ord('r'):
            original_file = open(original_filename, 'wb')
            original_ycbcr_file = open(original_ycbcr_filename, 'wb')
            compressed_file = open(compressed_filename, 'wb')
            rec_frame = 0
        
        # Stops Record if fps * duration is reached
        if (rec_frame == capture_frames):
            print("done recording\n")
            original_file.close()
            original_ycbcr_file.close()
            compressed_file.close()
            vc.print_size_and_compare(original_ycbcr_filename, compressed_filename)
            vc.print_size_and_compare(compressed_filename, original_ycbcr_filename)
            rec_frame += 1 # don't execute this block again

        if not windows_open():
            print("exiting because not all windows seem to be open")
            break

    # Release everything if job is finished
    cap.release()
    cv2.destroyAllWindows()

# execute only if run as a script
if __name__ == "__main__":
    if len(sys.argv) < 2:
        cap = cv2.VideoCapture(0)
    else: 
        cap = cv2.VideoCapture(int(sys.argv[1]))
    main(cap, 25, 1, g_quality_dct)

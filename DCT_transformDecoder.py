import pickle
import cv2
import numpy as np

import vc_utilities as vc
from encframewk import compressed_filename, original_filename, g_quality_dct

window_name = "Video Reconstruced RGB - RecordPlayback"

def main(fname, fps, quality=0.25):
    compressed_file = open(fname, 'rb')
    original_file = open(original_filename, 'rb')
    frame_count = 0

    while (True):
    #load next frame from file f and "de-pickle" it, convert from a string back to matrix or tensor:
    #If file reached end, start from the beginning 0 byte (seek(0)) and reset framecounter   
        try:
            Y_compressed = pickle.load(compressed_file)
            Cb_compressed = pickle.load(compressed_file)
            Cr_compressed = pickle.load(compressed_file)
            original_bgr = pickle.load(original_file)
            frame_count += 1
            print("Frame: ", frame_count)
        except:
            frame_count = 0
            compressed_file.seek(0)
            original_file.seek(0)

        # Decode
        ycbcr = vc.upsample420(
            vc.ifreqred(Y_compressed, quality),
            vc.ifreqred(Cb_compressed, quality),
            vc.ifreqred(Cr_compressed, quality),
        )
        bgr = vc.ycbcr_to_bgr(ycbcr)

        #Display FrameCount on Play
        cv2.putText(bgr, "Frame: " + str(frame_count), (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2)

        cv2.imshow(window_name, bgr)
        cv2.imshow("Original", original_bgr)
        diff = (bgr - original_bgr/255)+.5
        cv2.imshow("Diff", diff)

        #Wait for key for 40ms, to get about 25 frames per second playback 
        #(depends also on speed of the machine, and recording frame rate, try out):
        if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
            break

        # break if window closed
        if not cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE):
            break


    # Destroy everything if job is finished
    cv2.destroyAllWindows()

# execute only if run as a script
if __name__ == "__main__":
    main(compressed_filename, 25, g_quality_dct)

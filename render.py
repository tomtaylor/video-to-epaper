#!/usr/bin/env python
import cv2
import epd7in5
import sys
from PIL import Image

def resize(image_pil, width, height):
    '''
    Resize PIL image keeping ratio and using white background.
    '''
    if image_pil.width / width > image_pil.height / height:
        # It must be fixed by width
        print("width")
        resize_width = width
        resize_height = int(round(height * (width / image_pil.width)))
    else:
        # Fixed by height
        print("height")
        resize_width = int(round(float(width) * (float(height) / image_pil.height)))
        resize_height = height

    print(resize_width)
    print(resize_height)

    image_resize = image_pil.resize((resize_width, resize_height), Image.ANTIALIAS)
    background = Image.new('RGB', (width, height), (0, 0, 0, 0))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)
    return background


cap = cv2.VideoCapture(sys.argv[1])
frame_count = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
print(frame_count)
cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, int(sys.argv[2]) - 1)
ret, cv_frame = cap.read()


pil_frame = Image.fromarray(cv_frame)
size = (640, 384)
pil_frame.thumbnail(size, Image.ANTIALIAS)
background = Image.new('RGB', size)
background.paste(
    pil_frame, (int((size[0] - pil_frame.size[0]) / 2), int((size[1] - pil_frame.size[1]) / 2))
)

epd = epd7in5.EPD()
epd.init()
epd.display(epd.getbuffer(background))
epd.sleep()


#cv2.imwrite("frame-7000.png", frame)

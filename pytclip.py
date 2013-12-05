import cv2
from cv2 import resize
from surf import detect_character
import argparse

FACIAL_CASADE_CONF = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"

X = 0
Y = 1
HEIGHT = 3


def detect_face(img):
    height, width, depth = img.shape
    cascade = cv2.CascadeClassifier(FACIAL_CASADE_CONF)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = cascade.detectMultiScale(img_gray, 1.1, 2, cv2.cv.CV_HAAR_SCALE_IMAGE, (30,30))

    if len(rects) == 0:
        return -1

    height = rects[-1][HEIGHT]
    sY = rects[-1][Y] - height / 2
    if sY > height / 2:
        return -1
    else:
        return 0 if sY < 0 else sY

def tclip(source_path, dest_path, dest_width, dest_height, debug_mode=False):

    img = cv2.imread(source_path)
    height, width, depth = img.shape

    ratio = 300.0 / width
    tmp_size = (int(width * ratio), int(height * ratio))
    resize(img, tmp_size)
    
    result = detect_face(img)
    if result == -1:
        result = detect_character(img)
        
    result = -1 if result == -1 else int(float(result / ratio))

    if debug_mode:
        print dest_width, width
        print dest_height, height

    ratio_width = float(dest_width) / width
    ratio_height = float(dest_height) / height

    if ratio_width > ratio_height:
        ratio = ratio_width
    else:
        ratio = ratio_height

    if debug_mode:
        print "ratio", ratio

    result = -1 if result == -1 else int(result * ratio)

    tmp_size = (int(width * ratio), int(height * ratio))

    if debug_mode:
        print "resize image width", tmp_size[X]
        print "resize image height", tmp_size[Y]

    dest_img = resize(img, tmp_size)
    d_height, d_width, d_depth = dest_img.shape

    clip_left = 0
    clip_right = 0
    if ratio_width > ratio_height:
        if result == -1:
            clip_top = -((d_height - dest_height) / 2)
            clip_bootom = clip_top
        else:
            if d_height - result >= dest_height:
                clip_top = -result;
                clip_bottom = -(d_height - result - dest_height)
            else:
                clip_top = -(d_height - dest_height)
    else:
        clip_left = -((d_width - dest_width)/2)
        clip_right = clip_left

    if debug_mode:
        print clip_top, clip_bottom
        print clip_left, clip_right
        print d_width, d_height
        print width+clip_right, height+clip_bottom

    crop_img = dest_img[clip_left:d_height+clip_bottom, clip_top:d_width+clip_right]

    cv2.imwrite(dest_path, crop_img);

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s")
    parser.add_argument("-d")
    parser.add_argument("--width", default=300)
    parser.add_argument("--height", default=180)
    parser.add_argument("-m", default=False)

    args = parser.parse_args()
    tclip(args.s, args.d, args.width, args.height, args.m)

if __name__ == "__main__":
    main()

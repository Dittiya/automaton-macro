import cv2 as cv
import cv2.typing as cvType
import typing

Mat = cvType.MatLike

def blur(img: Mat, size: typing.Tuple = (7,7)) -> Mat:
    img_blur = cv.GaussianBlur(img, size, 1)

    return img_blur

def detect_lines(img: Mat) -> typing.List:
    lines = []


    return lines

def CropArea(img: Mat) -> Mat:
    height, width = img.shape

    min_height = int(0.3*height)
    max_height = int(0.85*height)
    min_width = int(0.3*width)

    cropped_image = img[min_height:max_height, min_width:width]

    return cropped_image

def RegionOfInterest():
    # Storing 4 regions
    rois = []

    return None
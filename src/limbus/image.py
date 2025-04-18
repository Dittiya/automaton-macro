from cv2.typing import MatLike
import cv2
import numpy

def read_image(dir: str) -> MatLike:
    img = cv2.imread(dir)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img

def gray_image(img: MatLike) -> MatLike:
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def blur_image(img: MatLike, kernel: tuple=(3,3)) -> MatLike:
    return cv2.GaussianBlur(img, kernel, 0)

def canny_edge_detection(img: MatLike, low_threshold: int=50, high_threshold: int=150) -> MatLike:
    return cv2.Canny(img, low_threshold, high_threshold)

def thresholding(img: MatLike, threshold: int=50) -> MatLike:
    _, thresh = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    return thresh

def process_image(img: MatLike, flags=[]):
    """
    list of flags: gray, blur, canny, thresh
    """
    im = img

    for flag in flags:
        match flag:
            case "gray":
                im = gray_image(im)
            case "blur":
                im = blur_image(im)
            case "canny":
                im = canny_edge_detection(im, 50, 100)
            case "thresh":
                mean, median = numpy.mean(im), numpy.median(im)

                thresh = 50
                if median < 5: thresh = 20
                elif median < 10: thresh = 30

                im = thresholding(im, thresh)
        
    return im

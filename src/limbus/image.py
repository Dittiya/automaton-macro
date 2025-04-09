import cv2
from cv2.typing import MatLike

def read_image(dir: str) -> MatLike:
    img = cv2.imread(dir)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img

def blur_image(img: MatLike, kernel: tuple=(3,3)) -> MatLike:
    return cv2.GaussianBlur(img, kernel, 0)

def canny_edge_detection(img: MatLike, low_threshold: int=50, high_threshold: int=150) -> MatLike:
    return cv2.Canny(img, low_threshold, high_threshold)

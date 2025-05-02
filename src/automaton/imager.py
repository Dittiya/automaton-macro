from win32gui import FindWindow, GetWindowRect, SetForegroundWindow, GetClientRect
from typing import NamedTuple
from cv2.typing import MatLike
from mss import mss, tools
from ctypes import windll
import cv2
import time

# Make program aware of DPI scaling
user32 = windll.user32
user32.SetProcessDPIAware()

IMAGE_OUTPUT = "images/capture.png"

class Window(NamedTuple):
    hwnd: int
    left: int
    top: int
    width: int
    height: int

def get_window_data(name: str) -> Window:
    try:
        hwnd = FindWindow(None, name)
        left, top, right, bottom = GetWindowRect(hwnd)
        window = Window(hwnd, left, top, right-left, bottom-top)
    except:
        raise TypeError("Window not found")

    return window

def grab_window(window: Window) -> None:
    sct = mss()

    SetForegroundWindow(window.hwnd)
    time.sleep(0.01)

    sct_img = sct.grab(window._asdict())
    tools.to_png(sct_img.rgb, sct_img.size, output=IMAGE_OUTPUT)

def set_window_top(window: Window) -> None:
    SetForegroundWindow(window.hwnd)

def grab_region(window: Window, output: str) -> None:
    if [x for x in [window, output] if x is None]:
        return TypeError("Type must not be None")

    sct = mss()
    sct_img = sct.grab(window._asdict())
    tools.to_png(sct_img.rgb, sct_img.size, output=output)

def read_image(dir: str, option: str="") -> MatLike:
    img = cv2.imread(dir)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if option in ["gray", "grey"]:
        img = gray_image(img)

    return img

def gray_image(img: MatLike) -> MatLike:
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def match_pixel(img: MatLike, location: tuple, color: str) -> bool:
    x, y = location
    hex = to_hex(img[y,x])

    if hex == color:
        return True
    return False

def to_hex(rgb: tuple|list) -> str:
    mapper = [str(x) for x in range(10)] + [chr(x) for x in range(65, 71)]
    hex = "0x"
    
    for channel in rgb:
        c1 = floor(channel/16)
        c2 = channel%16

        hex += mapper[c1] + mapper[c2]

    return hex

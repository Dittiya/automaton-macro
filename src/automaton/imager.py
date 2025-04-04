from win32gui import FindWindow, GetWindowRect, SetForegroundWindow, GetClientRect
from typing import NamedTuple
from mss import mss, tools
import time
from ctypes import windll

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
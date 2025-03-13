from win32gui import FindWindow, GetWindowRect, SetForegroundWindow
from typing import NamedTuple
from mss import mss, tools
import time

IMAGE_OUTPUT = "images/capture.png"

class Window(NamedTuple):
    id: int
    top: int
    left: int
    width: int
    height: int

def GetWindowData(name: str) -> Window:
    try:
        window_id = FindWindow(None, name)
        window_rect = GetWindowRect(window_id)
        window = Window(window_id, window_rect[0], window_rect[1], window_rect[2], window_rect[3])
    except:
        raise TypeError("Window not found")

    return window

def GrabWindow(window: Window) -> None:
    sct = mss()

    SetForegroundWindow(window.id)
    time.sleep(0.01)

    sct_img = sct.grab(window._asdict())

    tools.to_png(sct_img.rgb, sct_img.size, output=IMAGE_OUTPUT)
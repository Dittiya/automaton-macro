import pyautogui 

ZOOM_MESSAGE = "Zoom on"
CLICK_MESSAGE = "Click on"
ERROR_EMPTY_MESSAGE = "Value must not be empty"

def zoom(x: int, y: int, clicks: int) -> str:
    if None in [x, y, clicks]:
        return TypeError(ERROR_EMPTY_MESSAGE)

    pyautogui.scroll(x=x, y=y, clicks=clicks)

    return ZOOM_MESSAGE + f"({x}, {y}) {clicks} clicks."

def click(x: int, y: int, clicks: int) -> str:
    if None in [x, y, clicks]:
        return TypeError(ERROR_EMPTY_MESSAGE)
    
    pyautogui.click(x, y, clicks, 0.25)
    
    return CLICK_MESSAGE + f"({x}, {y}) {clicks} clicks."
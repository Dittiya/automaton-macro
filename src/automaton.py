from imager import Window, get_window_data, grab_window, set_window_top, grab_region
import os
import pyautogui 
import time

class Automaton:
    def __init__(self, name: str, state: bool=False):
        self.name = name
        self.state = state
        self.vision = None
        self.window = get_window_data(self.name)
        self.delay = 0
        self._roi_coordinate = None

    def get_cursor_position(self) -> None:
        return pyautogui.position()

    def set_delay(self, delay: int):
        self.delay = delay
    
    def start(self):
        if self.state is not True:
            print(f"Starting {self.name}")
            self.state = True

    def stop(self):
        if self.state is True:
            print(f"Stopping {self.name}")
            self.state = False

    def grab(self):
        if not self.state:
            return
        
        pyautogui.moveTo(self.window.width+100, self.window.height+100)
        grab_window(self.window)
        print(f"Looking at {self.window}")

    def zoom(self, clicks: int):
        if not self.state:
            return
        
        set_window_top(self.window)
        self.centerize_cursor()

        for _ in range(abs(clicks)):
            pyautogui.scroll(clicks)
            time.sleep(self.delay)

    def centerize_cursor(self):
        center_x = int(self.window.width * 0.5)
        center_y = int(self.window.height * 0.5)

        pyautogui.moveTo(center_x, center_y)

    def drag(self, x: int, y: int, btn: str='left') -> None:
        if not self.state:
            return
            
        pyautogui.drag(x, y, 0.25, button=btn)

    def grab_roi(self):
        x, y = self.get_cursor_position()

        if self._roi_coordinate is not None:
            print(f"Ending position ({x},{y})")
            region_window = Window(hwnd=self.window.hwnd, 
                                   left=self._roi_coordinate[0], 
                                   top=self._roi_coordinate[1], 
                                   width=x-self._roi_coordinate[0], 
                                   height=y-self._roi_coordinate[1])
            
            print(region_window)
            grab_region(region_window, "test_region.png")
            self._roi_coordinate = None
        else:
            print(f"Starting position ({x},{y})")
            self._roi_coordinate = [x,y]

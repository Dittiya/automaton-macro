from automaton.imager import Window, get_window_data, set_window_top, grab_region, read_image, match_pixel
from cvision.feature_detection import detect_feature, detect_object
from pathlib import Path
import os
import pyautogui 
import time

class Automaton:
    def __init__(self, name: str):
        self.name = name
        self.state = False
        self.vision = None
        self.window = get_window_data(self.name)
        self.delay = 0.05
        self.img_storage = f"{Path().absolute().resolve()}\images"
        self._roi_coordinate = None

    def __normalize_XY(self, x: int|list|tuple, y: int|None) -> tuple[int, int]:

        if type(x) is not int:
            if y is None:
                x, y = x
    
        x += self.window.left
        y += self.window.top

        return x, y
    
    def __relative_XY(self, x: int|list|tuple, y: int=None) -> tuple[int, int]:

        if type(x) is not int:
            if y is None:
                x, y = x
    
        x -= self.window.left
        y -= self.window.top

        return x, y

    def get_cursor_position(self) -> None:
        x, y = pyautogui.position()
        point = self.__relative_XY(x, y)
        print(f"Absolute: ({x}, {y}), Relative: {point}")
        return pyautogui.position()
    
    def start(self):
        if self.state is False:
            print(f"Starting {self.name}")
            self.state = True

    def stop(self):
        if self.state is True:
            print(f"Stopping {self.name}")
            self.state = False

    def click(self, x: int|list|tuple, y: int|None=None, clicks: int=1) -> None:
        x, y = self.__normalize_XY(x, y)

        pyautogui.moveTo(x, y)
        pyautogui.click(x, y, clicks=clicks, interval=self.delay)
        return
    
    def on_screen(self, target: str, minimum: int=10) -> bool:
        target_img = read_image(target, "gray")
        train_img = read_image(f"{self.img_storage}\capture.png", "gray")

        _, target_desc = detect_feature(target_img, 10)
        _, train_desc = detect_feature(train_img, 10)

        return detect_object(target_desc, train_desc, min=minimum)

    def press(self, key: str, clicks: int=1) -> None:
        pyautogui.press(key, clicks, self.delay)

    def grab(self, mouse: bool=True) -> None:
        if not self.state:
            return
        
        if mouse is False:
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
        x = int(self.window.width * 0.5)
        y = int(self.window.height * 0.5)

        x, y = self.__normalize_XY(x, y)

        pyautogui.moveTo(x, y)

    def drag(self, x: int, y: int, btn: str='left') -> None:
        if not self.state:
            return
            
        pyautogui.drag(x, y, 0.25, button=btn)

    def grab_roi(self, name: str) -> None:
        x, y = self.get_cursor_position()

        try:
            os.makedirs(self.img_storage)
        except FileExistsError:
            pass

        # Janky might fix later
        output = f"{self.img_storage}\{name}.png"
        existing_img = [img for img in os.listdir(self.img_storage) if f"{name}_" in img]
        if not existing_img:
            output = output.replace(name, f"{name}_1")
        else:
            index = existing_img[-1].split(".")[0]
            index = int(index.split("_")[-1]) + 1

            output = output.replace(name, f"{name}_{index}")

        if self._roi_coordinate is not None:
            print(f"Ending position ({x},{y})")
            region_window = Window(hwnd=self.window.hwnd, 
                                   left=self._roi_coordinate[0], 
                                   top=self._roi_coordinate[1], 
                                   width=x-self._roi_coordinate[0], 
                                   height=y-self._roi_coordinate[1])
            
            print(region_window)
            grab_region(region_window, output)
            self._roi_coordinate = None
        else:
            print(f"Starting position ({x},{y})")
            self._roi_coordinate = [x,y]

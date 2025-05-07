from automaton.automaton import Automaton
from limbus.dungeon import Dungeon
from limbus.data import Config
from time import sleep, time
from pathlib import Path
import cv2
import keyboard as kb

def wait_anchor(automaton: Automaton, anchor: str, threshold: int=15):
    while True:
        sleep(0.75)
        print("Waiting...")
        automaton.grab(mouse=True)
        if automaton.on_screen(anchor, threshold):
            break

def wait_pixel(automaton: Automaton, location: tuple, color: str):
    x, y = location
    while True:
        sleep(0.75)
        print("Waiting...")
        automaton.grab(True)
        if automaton.pixel_search(x, y, color):
            break

def pix_search(automaton: Automaton):
    automaton.pixel_context = "Screen"
    loc = automaton.pixel_search(708, 149, "0x970A09")
    automaton.pixel_context = "Window"
    print(loc)
    return loc

def reposition(automaton: Automaton):
    automaton.zoom(-6)
    automaton.drag(-500, 300)

def Toggle(automaton: Automaton):
    if automaton.state:
        automaton.stop()
    else:
        automaton.start()

def grabber(automaton: Automaton):
    if automaton.state is False:
        return
    
    automaton.pixel_context = "Screen"

    start_time = time()
    PARENT_DIR = Path().absolute().resolve()

    reposition(automaton)

    sleep(0.5)
    automaton.grab(mouse=False)

    encounters = f"{PARENT_DIR}\images\encounter"
    img = cv2.imread(f"{PARENT_DIR}\images\LimbusCompany.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    md = Dungeon(img, config=Config(x_start=210), encounters_dir=encounters)

    path = md.crawl()

    print(f"Shortest/Most rewarding path: {path}")

    nodes = md.nodes
    for id in path:
        node = next(node for node in nodes if node.id == id)

        reposition(automaton)

        x, y = node.get_center()
        print(f"Clicking ({x},{y})")
        automaton.click(x, y)
        sleep(1)
        automaton.press("enter")
        sleep(0.75)
        automaton.press("enter")
        automaton.centerize_cursor()

        # wait_anchor(automaton, anchor)
        wait_pixel(automaton, (708, 149), "0x970A09")

        sleep(0.5)
    
    reposition(automaton)
    shop = (883, 543)
    automaton.click(shop)
    sleep(1)
    automaton.press("enter")
    automaton.centerize_cursor()
    wait_pixel(automaton, (708, 149), "0x970A09")

    boss = (915, 395)
    automaton.click(boss)
    sleep(1)
    automaton.press("enter")
    sleep(0.75)
    automaton.press("enter")
    automaton.centerize_cursor()

    print("FLOOR FINISHED!")
    print(f"ENDED IN: {time() - start_time} seconds")

    
def log(automaton: Automaton):
    print(automaton.get_cursor_position())

def region(automaton: Automaton):
    automaton.grab(False)

def main():
    atom = Automaton("LimbusCompany")
    kb.add_hotkey("ctrl+e", Toggle, [atom])
    kb.add_hotkey("ctrl+d", region, [atom])
    kb.add_hotkey("ctrl+t", grabber, [atom])
    kb.add_hotkey("ctrl+g", log, [atom])
    kb.add_hotkey("ctrl+b", pix_search, [atom])

    while True:
        try:
            # Run(atom)
            sleep(0.1)
        except KeyboardInterrupt:
            return 0
        
main()
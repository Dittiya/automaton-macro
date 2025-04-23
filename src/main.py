from automaton.automaton import Automaton
from limbus.dungeon import Dungeon
from limbus.data import Config
from time import sleep
from pathlib import Path
import cv2
import keyboard as kb

def Toggle(automaton: Automaton):
    if automaton.state:
        automaton.stop()
    else:
        automaton.start()

def grabber(automaton: Automaton):
    if automaton.state is False:
        return

    PARENT_DIR = Path().absolute().resolve()

    automaton.zoom(-6)
    automaton.drag(-500, 300)

    sleep(0.5)
    automaton.grab(mouse=False)

    encounters = f"{PARENT_DIR}\images\encounter"
    img = cv2.imread(f"{PARENT_DIR}\images\capture.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    md = Dungeon(img, config=Config(x_start=210), encounters_dir=encounters)

    md.map()
    md.find_lines()
    md.map_connections()
    path = md.crawl()

    print(f"Shortest/Most rewarding path: {path}")

    nodes = md.nodes
    for id in path:
        node = next(node for node in nodes if node.id == id)

        automaton.zoom(-6)
        automaton.drag(-500, 300)
        
        x, y = node.get_center()
        print(f"Clicking ({x},{y})")
        automaton.click(x, y)
        sleep(1)
        automaton.press("enter")
        sleep(0.5)
        automaton.press("enter")
        automaton.centerize_cursor()

        while True:
            sleep(0.75)
            print("Waiting...")
            automaton.grab(mouse=True)
            if automaton.on_screen("D:\Repository\python-limbus\images\\anchor.png", 20):
                break

        sleep(1)
    
    print("FLOOR FINISHED!")

    
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

    while True:
        try:
            # Run(atom)
            sleep(0.05)
        except KeyboardInterrupt:
            return 0
        
main()
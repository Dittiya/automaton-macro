from automaton.automaton import Automaton
from limbus.dungeon import Dungeon
from limbus.data import Config
from time import sleep
import cv2
import keyboard as kb

def Toggle(automaton: Automaton):
    if automaton.state:
        automaton.stop()
    else:
        automaton.start()

def Run(automaton: Automaton):
    if automaton.state:
        print(f"{automaton.name} is currently running...")

def vision(automaton: Automaton):
    automaton.grab()

def zoom(automaton: Automaton):
    automaton.zoom(-200)

def grabber(automaton: Automaton):
    automaton.zoom(-6)
    automaton.drag(400, 300)
    automaton.grab()

    encounters = "D:\Repository\python-limbus\images\encounter"
    img = cv2.imread("D:\Repository\python-limbus\images\capture.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    md = Dungeon(img, config=Config(), encounters_dir=encounters)

    md.map()
    md.find_lines()
    md.map_connections()
    path = md.crawl()

    print(f"Shortest/Most rewarding path: {path}")
    
def log(automaton: Automaton):
    print(automaton.dir)

def region(automaton: Automaton):
    automaton.grab_roi("node")

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
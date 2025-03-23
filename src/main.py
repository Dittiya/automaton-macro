import keyboard as kb
from automaton import Automaton
from time import sleep

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
    
def log(automaton: Automaton):
    x, y = automaton.get_cursor_position()
    print(f"Window {automaton.window}")
    print(f"Cursor Screen position ({x}, {y})")
    print(f"Cursor Window position ({x - automaton.window.left}, {y - automaton.window.top})")

def region(automaton: Automaton):
    automaton.grab_roi()

def main():
    atom = Automaton("LimbusCompany")
    kb.add_hotkey("ctrl+r", Toggle, [atom])
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
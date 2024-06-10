# tui.py
import os ,time, threading, keyboard


# Dictionary to hold key states and pulse timers
key_states = {}
pulse_duration = 0.1  # Pulse duration in seconds

def handle_key_event(event):
    current_time = time.time()
    key = event.name
    if event.event_type == 'down':
        if key not in key_states or not key_states[key]['held']:
            key_states[key] = {'held': True, 'pulse': True, 'time': current_time}
        elif current_time - key_states[key]['time'] > pulse_duration:
            key_states[key]['pulse'] = False
    elif event.event_type == 'up':
        if key in key_states:
            key_states[key]['held'] = False
            key_states[key]['pulse'] = False

def update_key_states():
    while True:
        current_time = time.time()
        for key, state in key_states.items():
            if state['held'] and state['pulse'] and current_time - state['time'] > pulse_duration:
                key_states[key]['pulse'] = False
        time.sleep(0.01)

def key_pulsed(key):
    return key_states.get(key, {}).get('pulse', False)

# Start a separate thread to update key states
threading.Thread(target=update_key_states, daemon=True).start()

# Hook the keyboard events
keyboard.hook(handle_key_event)


#-----------------------------------------New file as import is dum-------------------------------------------#

# Classes
class Menu:
    def __init__(self, header, rows_list):
        self.items = rows_list
        self.select_row = 0
        self.header = header
        self.select_row_not_modified = str()
        self.footer = ""

    def select(self):
        # Clear previous selection
        self.clear_selection()
        # Highlight current selection
        self.select_row_not_modified = self.items[self.select_row]
        self.items[self.select_row] = f"\33[7;49;39m{self.items[self.select_row]}\33[0m"

    def clear_selection(self):
        # Remove highlighting from all items
        for i in range(len(self.items)):
            self.items[i] = self.items[i].replace("\33[7;49;39m", "").replace("\33[0m", "")

    def draw_self(self):
        print(str(self.header))
        for row in self.items:
            print(row)
        if self.footer != "":
            print("Slected:")
            print(self.footer)

    def event_down_select(self):
        self.clear_selection()
        self.select_row += 1
        if self.select_row >= len(self.items):
            self.select_row = 0
        self.select()

    def event_up_select(self):
        self.clear_selection()
        self.select_row -= 1
        if self.select_row < 0:
            self.select_row = len(self.items) - 1
        self.select()

    def set_header(self, anystr: str):
        self.header = anystr
    
    def set_Menu_table(self, lst: list[str, str, str]):
        self.items = lst

    def set_footer(self, footer : str):
        self.footer = footer

    def IsGoKeyPressedOnObj(self, key):
        return keyboard.is_pressed(key)

    def CurrentSlectedItem(self):
        return self.select_row_not_modified




def displayflip():
    os.system("cls")





# Initialize menu
my_menu = Menu(
    "Food               : Price",  # Header
    [
        "HotDog             :   10$",  # Menu
        "Burger (ham)       :   20$",
        "Burger (cheez)     :   20$",
        "Burger (beef)      :   27$",
        "Burger (Ham cheez) :   45$"
    ]
)

# Initial selection
my_menu.select()

while True:
    my_menu.draw_self()
    print(
    "is arrow up key is pressed:   " + str(keyboard.is_pressed("up arrow")),
    "\nis arrow down key is pressed: " + str(keyboard.is_pressed("down arrow")),
    "\nis key enter is pressed:      " + str(keyboard.is_pressed("enter"))
    )
    if key_pulsed("up"):
        my_menu.event_up_select()
    elif key_pulsed("down"):
        my_menu.event_down_select()
    if my_menu.IsGoKeyPressedOnObj("enter"):
        my_menu.set_footer(my_menu.CurrentSlectedItem())
    else:
        my_menu.set_footer("")
    time.sleep(0.1)  # Small delay to prevent rapid switching
    
    displayflip()



# this code is under cc-by-ss

import os
import time
import threading
from typing import List, Dict, Any
import keyboard

# Dictionary to hold key states and pulse timers
key_states: Dict[str, Dict[str, Any]] = {}
pulse_duration: float = 0.1  # Pulse duration in seconds

def handle_key_event(event: keyboard.KeyboardEvent) -> None:
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

def update_key_states() -> None:
    while True:
        current_time = time.time()
        for key, state in key_states.items():
            if state['held'] and state['pulse'] and current_time - state['time'] > pulse_duration:
                key_states[key]['pulse'] = False
        time.sleep(0.01)

def key_pulsed(key: str) -> bool:
    return key_states.get(key, {}).get('pulse', False)

# Start a separate thread to update key states
threading.Thread(target=update_key_states, daemon=True).start()

# Hook the keyboard events
keyboard.hook(handle_key_event)

class ListKeyMenu:
    def __init__(self, header: str, rows_list: List[str]) -> None:
        self.items: List[str] = rows_list
        self.select_row: int = 0
        self.header: str = header
        self.select_row_not_modified: str = ""
        self.footer: str = ""
        self.menu_footer_line: bool = False
        self.menu_footer_line_char: str = "-"
        self.hedder_menu_line: bool = False
        self.hedder_menu_line_char: str = "-"
        self.draw_border: bool = False
        self.border_chars: List[str] = ["-", "|"]

    def select(self) -> None:
        # Clear previous selection
        self.clear_selection()
        # Highlight current selection
        self.select_row_not_modified = self.items[self.select_row]
        self.items[self.select_row] = f"\33[7;49;39m{self.items[self.select_row]}\33[0m"

    def clear_selection(self) -> None:
        # Remove highlighting from all items
        for i in range(len(self.items)):
            self.items[i] = self.items[i].replace("\33[7;49;39m", "").replace("\33[0m", "")

    def draw_self(self) -> None:
        print(str(self.header))
        if self.hedder_menu_line and not self.draw_border:
            print(f"{self.hedder_menu_line_char}" * (len(max(self.items, key=len)) + 4))
        for row in self.items:
            print(row)

        if self.footer != "":
            print(self.footer)
        
    def event_down_select(self) -> None:
        self.clear_selection()
        self.select_row += 1
        if self.select_row >= len(self.items):
            self.select_row = 0
        self.select()

    def event_up_select(self) -> None:
        self.clear_selection()
        self.select_row -= 1
        if self.select_row < 0:
            self.select_row = len(self.items) - 1
        self.select()

    def set_header(self, anystr: str) -> None:
        self.header = anystr
    
    def set_Menu_table(self, lst: List[str]) -> None:
        self.items = lst

    def set_footer(self, footer: str) -> None:
        self.footer = footer

    def IsGoKeyPressedOnObj(self, key: str) -> bool:
        return keyboard.is_pressed(key)

    def CurrentSlectedItem(self) -> str:
        return self.select_row_not_modified
    
    def style(self, *args: int) -> None:
        for style in args:
            if style == 1:
                self.hedder_menu_line = True
            elif 1 not in args:
                self.hedder_menu_line = False
            if style == 2:
                self.menu_footer_line = True
            elif 2 not in args:
                self.menu_footer_line = False
            if style == 3:
                self.draw_border = True
            elif 3 not in args:
                self.draw_border = False

    def ConfigStyles(self, stylelook: int, CharUse: Any) -> None:
        if stylelook == 1:
            self.hedder_menu_line_char = CharUse
        elif stylelook == 2:
            self.menu_footer_line_char = CharUse
       

import curses
from typing import List

class ListKeyMenu:
    def __init__(self, header: str, rows_list: List[str]) -> None:
        self.items: List[str] = rows_list
        self.select_row: int = 0
        self.header: str = header
        self.footer: str = ""
        self.menu_footer_line: bool = False
        self.menu_footer_line_char: str = "-"
        self.hedder_menu_line: bool = False
        self.hedder_menu_line_char: str = "-"
        self.draw_border: bool = False
        self.border_chars: List[str] = ["-", "|"]
        self.debug_info: str = ""
        self.debug_mode: bool = False

    def draw_self(self, stdscr) -> None:
        stdscr.clear()
        stdscr.addstr(0, 0, self.header)
        if self.hedder_menu_line and not self.draw_border:
            stdscr.addstr(1, 0, f"{self.hedder_menu_line_char}" * (len(max(self.items, key=len)) + 4))
        
        for idx, row in enumerate(self.items):
            if idx == self.select_row:
                stdscr.addstr(idx + 2, 0, row, curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 2, 0, row)
        
        if self.footer != "":
            stdscr.addstr(len(self.items) + 3, 0, self.footer)
        
        # Debug info
        if self.debug_mode:
            stdscr.addstr(len(self.items) + 4, 0, "Debug Info: " + self.debug_info)
        
        stdscr.refresh()

    def event_down_select(self) -> None:
        self.select_row += 1
        if self.select_row >= len(self.items):
            self.select_row = 0

    def event_up_select(self) -> None:
        self.select_row -= 1
        if self.select_row < 0:
            self.select_row = len(self.items) - 1

    def set_header(self, anystr: str) -> None:
        self.header = anystr
    
    def set_Menu_table(self, lst: List[str]) -> None:
        self.items = lst

    def set_footer(self, footer: str) -> None:
        self.footer = footer

    def CurrentSlectedItem(self) -> str:
        return self.items[self.select_row]
    
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

    def ConfigStyles(self, stylelook: int, CharUse: str) -> None:
        if stylelook == 1:
            self.hedder_menu_line_char = CharUse
        elif stylelook == 2:
            self.menu_footer_line_char = CharUse
        if stylelook == 3:
            self.border_chars = CharUse

    def set_debug_info(self, info: str) -> None:
        self.debug_info = info

    def toggle_debug_mode(self) -> None:
        self.debug_mode = not self.debug_mode
        self.set_debug_info(f"Debug mode {'enabled' if self.debug_mode else 'disabled'}")

def main(stdscr):
    menu = ListKeyMenu(header='Menu Header || for example: Item menu', rows_list=["Item 1", "Item 2", "Item 3", "Item 4"])
    menu.set_footer('Menu Footer \nfor example: press "q" to quit')
    menu.style(1)
    
    while True:
        menu.draw_self(stdscr)
        key = stdscr.getch()
        
        if key == curses.KEY_DOWN:
            menu.event_down_select()
            menu.set_debug_info(f"Key Down pressed. Current selection: {menu.CurrentSlectedItem()}")
        elif key == curses.KEY_UP:
            menu.event_up_select()
            menu.set_debug_info(f"Key Up pressed. Current selection: {menu.CurrentSlectedItem()}")
        elif key == ord('`'):
            menu.toggle_debug_mode()
        elif key == ord('q'):
            menu.set_debug_info("Quit key pressed.")
            break
        else:
            menu.set_debug_info(f"Other key pressed: {key}")

if __name__ == "__main__":
    curses.wrapper(main)

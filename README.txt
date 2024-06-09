This is a python based import for Tui it is very new also it requires keyboard for keydection
doc's
how to make a new menu 
MyMenu = Menu(hedder, [
str(row0)
str(row1)
str(row2)
str(row3)
str(row4)
str(row5)
])

now u can change row hedder and a fotter (we get more on that later) but none f"" string are live so yea 
MyMenu.set_hedder(str)
MyMenu.set_Menu(lst)
MyMenu.set_footer(str)

also ever loop this shoulid be called
MyMenu.draw()
display.flip()

the go key stand fo the slect key to actualy slect soom u can test if a key is pressed via
MyMenu.IsGoKeyPressedOnObj(strkey)

and MyMenu.CurrentSlectedItem() to get slected item
also if the footer is "" it does not draw it so keep it ( ) it is a alt+2+5+5 char
ADD A time.sleep(0.1) so u dont get flashi text 

also the event_up_select() justs mkae it slect the upeer one and oops dof rdown

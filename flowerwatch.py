from datetime import date
import os
import pickle
import curses
import time

a = ""
class plant:
  def __init__(self, name, watered):
    self.name = name
    self.watered = watered

  def diff (self):
     if self.watered == "Null":
         self.watered = date.today()

     tdy = date.today()
     dif = tdy - self.watered
     return dif.days


allplants = []
allplants = pickle.load(open("plants.pkl", "rb"))


def menu(win, current_row):

    h, w = win.getmaxyx()
    for ind, opt in enumerate(allplants):
        if opt.watered == "Null":
            a = opt.watered
        else:
            a= str(opt.watered)

        ime = opt.name+ " "+a
        y = h//2 + ind - len(allplants)//2
        x = w//2 - len(ime)//2
        if current_row == ind:

            win.attron(curses.color_pair(1) | curses.A_BOLD)
            win.addstr(y, x, ime)

            win.attroff(curses.color_pair(1))
        else:
            win.addstr(y, x, ime)
    win.refresh()

def menubottom(win, current_row, current_column):


    mod1 = ["Add", "Else"]
    h, w = win.getmaxyx()
    mode = False;
    if mode == False:
        for ind, opt in enumerate(mod1):
            y = h-1
            x = w//9
            if ind==1:
                x=w//2
            if current_row == len(allplants) and current_column==ind:

                win.attron(curses.color_pair(1) | curses.A_BOLD)
                win.addstr(y, x, opt)

                win.attroff(curses.color_pair(1))
            else:
                win.addstr(y, x, opt)
    win.refresh()


def usrinput(win,):
    win.clear()

    record = ''
    current_row = len(allplants)
    current_column = 0
    h, w = win.getmaxyx()
    y = h-1
    x = w//2-11
    win.attron(curses.color_pair(2) | curses.A_BOLD)
    win.addstr(y, x, "Plant Name: ")
    win.attroff(curses.color_pair(2))
    menu(win, current_row)
    win.refresh()
    v= x+12
    while True:

        key = win.getkey()


        if ord(key) == 10:
            if record != "":
                allplants.append(plant(record, "Null"))
            win.clear()
            menu(win, current_row)
            menubottom(win, current_row, current_column)
            win.refresh()
            break
        elif ord(key) == 127:
            record = record[:-1]
            win.clear()
            menu(win, current_row)
            win.attron(curses.color_pair(2) | curses.A_BOLD)
            win.addstr(y, x, "Plant Name: "+record)
            win.attroff(curses.color_pair(2))
        else:
            win.attron(curses.color_pair(2) | curses.A_BOLD)
            record += str(key)
            win.addstr(y, x, "Plant Name: "+record)
            win.attroff(curses.color_pair(2))
def main(win):
    curses.use_default_colors()
    curses.init_pair(4, curses.COLOR_GREEN, -1)
    win.bkgd(' ', curses.color_pair(4) | curses.A_BOLD)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE )
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN )
    curses.curs_set(0)
    current_row = 0
    current_column = 0

    menubottom(win, current_row, current_column)
    menu(win, current_row)

    while True:
        key = win.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1

        elif key == curses.KEY_DOWN and current_row < len(allplants):
            current_row += 1

        elif key == curses.KEY_RIGHT and current_row == len(allplants) and current_column<1:
            current_column += 1

        elif key == curses.KEY_LEFT and current_row == len(allplants) and current_column>0:
            current_column -= 1

        elif key == curses.KEY_ENTER or key in [10,13] and current_row == len(allplants) and current_column == 0:
            usrinput(win)



        menu(win, current_row)
        menubottom(win, current_row, current_column)

curses.wrapper(main)










#allplants.append(plant(plname, "Null"))
#prtable()
#pickle.dump(allplants, open("plants.pkl", "wb"))

#print("")
#print(p1.name,":","Watered ",Plant.diff(p1)," Days ago")
#print("")


#str = "Your number is " + str(nm)
#print(str.center(os.get_terminal_size().columns))

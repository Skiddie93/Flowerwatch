from datetime import date
import os
import pickle
import curses
import time

mn = 1
a = ""


class plant:
  def __init__(self, name, watered, days):
    self.name = name
    self.watered = watered
    self.days = days

  def diff (self):
     if self.watered == "Null":
         self.watered = date.today()

     tdy = date.today()
     self.days = tdy - self.watered
     return self.days


allplants = []
allplants = pickle.load(open("plants.pkl", "rb"))


def menu(win, current_row):

    h, w = win.getmaxyx()
    for ind, opt in enumerate(allplants):
        if opt.watered == "Null":
            a = opt.watered
        else:
            opt.diff()
            a = opt.days.days
            a = str(a)


        ime = opt.name+ " "+a
        y = h//2 + ind - len(allplants)//2
        x = w//2 - len(ime)//2
        if current_row == ind or mn==2 and prev_row == ind:

            win.attron(curses.color_pair(1) | curses.A_BOLD)
            win.addstr(y, x, ime)

            win.attroff(curses.color_pair(1))
        else:
            win.addstr(y, x, ime)

            if ind==prev_row and mn==2:
                win.attron(curses.color_pair(1) | curses.A_BOLD)
                win.addstr(y, x, ime)

                win.attroff(curses.color_pair(1))


    win.refresh()

def menubottom(win, current_row, current_column, mn):
    global usedlen

    mod1 = ["Add"]
    mod2 = ["Water", "Delete", "Back"]
    h, w = win.getmaxyx()
    if mn == 1:
        usedlen= len(mod1)
        win.clear()
        menu(win, current_row)
        for ind, opt in enumerate(mod1):
            y = h-2
            x = w//3//2-len(mod1)+1
            if current_row == len(allplants) and current_column==ind:

                win.attron(curses.color_pair(1) | curses.A_BOLD)
                win.addstr(y, x, opt)

                win.attroff(curses.color_pair(1))
            else:
                win.addstr(y, x, opt)

    elif mn == 2:

        usedlen=len(mod2)
        win.clear()
        menu(win, current_row)
        for ind, opt in enumerate(mod2):
            multi= ind+1
            y = h-2
            t = w//3
            x = (t*multi)-t//2-len(mod2)

            if current_row == len(allplants) and current_column==ind:

                win.attron(curses.color_pair(1) | curses.A_BOLD)
                win.addstr(y, x, opt)

                win.attroff(curses.color_pair(1))

            else:


                win.addstr(y, x, opt)
        menu(win, current_row)

    win.refresh()
    return usedlen

def usrinput(win):
    win.clear()
    tittle(win)
    record = ''
    current_row = len(allplants)
    current_column = 0
    h, w = win.getmaxyx()
    y = h-2
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
                allplants.append(plant(record, "Null", "null"))
                pickle.dump(allplants, open("plants.pkl", "wb"))
            win.clear()
            menu(win, current_row)
            menubottom(win, current_row, current_column, mn)

            win.refresh()
            break
        elif ord(key) == 127:
            record = record[:-1]
            win.clear()
            menu(win, current_row)
            tittle(win)
            win.attron(curses.color_pair(2) | curses.A_BOLD)
            win.addstr(y, x, "Plant Name: "+record)
            win.attroff(curses.color_pair(2))
        else:
            win.attron(curses.color_pair(2) | curses.A_BOLD)
            record += str(key)
            win.addstr(y, x, "Plant Name: "+record)
            win.attroff(curses.color_pair(2))

def tittle(win):
    h, w = win.getmaxyx()
    y = 1
    x = w//2-5

    win.addstr(y, x, "Flowerwatch")
    win.refresh()

def main(win):
    curses.use_default_colors()
    curses.init_pair(4, curses.COLOR_GREEN, -1)
    win.bkgd(' ', curses.color_pair(4) | curses.A_BOLD)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN )
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN )
    curses.curs_set(0)
    current_row = 0
    current_column = 0
    global mn
    global prev_row
    prev_row= 1
    mn = 1


    menubottom(win, current_row, current_column, mn)
    menu(win, current_row)
    tittle(win)

    while True:
        key = win.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1

        elif key == curses.KEY_DOWN and current_row < len(allplants):
            current_row += 1

        elif key == curses.KEY_RIGHT and current_row == len(allplants) and current_column<usedlen-1:
            current_column += 1

        elif key == curses.KEY_LEFT and current_row == len(allplants) and current_column>0:
            current_column -= 1

        elif key == curses.KEY_ENTER or key in [10,13] and current_row == len(allplants) and current_column == 0 and mn==1:
            usrinput(win)


        elif key == curses.KEY_ENTER or key in [10,13] and current_row == len(allplants) and current_column == 2 and mn==2:
            mn=1
            current_row = prev_row
            current_column=0

        elif key == curses.KEY_ENTER or key in [10,13] and current_row == len(allplants) and current_column == 1 and mn==2:
            allplants.remove(allplants[prev_row])
            pickle.dump(allplants, open("plants.pkl", "wb"))
            mn=1
            current_row = prev_row
            current_column=0

        elif key == curses.KEY_ENTER or key in [10,13] and current_row == len(allplants) and current_column == 0 and mn==2:
            allplants[prev_row].watered=date.today()
            pickle.dump(allplants, open("plants.pkl", "wb"))

            mn=1
            current_row = prev_row
            current_column=0


        elif key == curses.KEY_ENTER or key in [10,13] and current_row < len(allplants):
            prev_row = current_row
            mn = 2
            menubottom(win, current_row, current_column, mn)
            current_row = len(allplants)



        if mn== 2 and key == curses.KEY_UP:
            current_row += 1






        menu(win, current_row)
        menubottom(win, current_row, current_column, mn)
        tittle(win)
curses.wrapper(main)










#allplants.append(plant(plname, "Null"))
#prtable()
#pickle.dump(allplants, open("plants.pkl", "wb"))

#print("")
#print(p1.name,":","Watered ",Plant.diff(p1)," Days ago")
#print("")


#str = "Your number is " + str(nm)
#print(str.center(os.get_terminal_size().columns))

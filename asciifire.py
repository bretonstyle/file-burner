#!/usr/bin/env python
# All credit to https://github.com/mhearse/asciifire/blob/master/asciifire.py


"""

Release under the terms of the GPL licence
You can get a copy of the license at http://www.gnu.org

Ported by: Matt Hersant (matt_hersant[at]yahoo[dot]com)

Description: An animated ascii art fire.
To force no color: shell> TERM=vt100 ./asciifire.py

This algorithm was ported from javascript written by: Thiemo Mattig
http://maettig.com/code/javascript/asciifire.html

"""

try:
    import curses
    import argparse
    from sys import exit
    from random import randint
    from time import time, sleep
    from signal import signal, SIGINT
except ImportError as err:
    print("Error Importing module. %s" % (err))
    exit(1)



##############################################
def signal_handler(signal, frame):
##############################################
    curses.endwin()
    exit(0)

class Fire:
    def __init__(self, options):
        self.options = options
        self.myscreen = curses.initscr()
        self.info_win = curses.newwin(3, 50, 0, 0)
        self.info_win.addstr(0, 0, "testing")
        self.info_win.refresh()
        curses.noecho()
        curses.cbreak()
        if curses.has_colors():
            curses.curs_set(0)
        self.cursescolor = options.validcolors.get(options.color)
        if curses.has_colors():
            self.init_colors()
        else:
            self.cursescolor = ''
        self.last_cycle_changed = time()
        signal(SIGINT, self.signal_handler)
        self.myscreen.timeout(-1 if options.block else 0)
        self.size = 80 * 25
        self.b = [0 for _ in range(self.size + 81)]
        self.char = [' ', '.', ':', '*', 's', 'S', '#', '$']
        self.paused = False
        self.max_y, self.max_x = None, None

    def init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        for i, color in enumerate([curses.COLOR_RED, curses.COLOR_BLUE, curses.COLOR_GREEN, curses.COLOR_YELLOW, curses.COLOR_WHITE], start=1):
            curses.init_pair(i, color, curses.COLOR_BLACK)

    def signal_handler(self, signal, frame):
        curses.endwin()
        exit(0)

    
    def run(self):
        while True:
            self.process_input()
            self.update_fire()
            self.draw_fire()
            self.handle_color_cycling()
            sleep(self.options.delay/1000000.0)

    def process_input(self):
        event = self.myscreen.getch()
        if event == ord('q'):
            curses.endwin()
            exit(0)
        if event == ord('p'):
            self.paused = not self.paused
            self.myscreen.timeout(-1 if self.paused else 0)
        if event == curses.KEY_RESIZE or self.max_y is None:
            self.check_window_size()

    def check_window_size(self):
        self.max_y, self.max_x = self.myscreen.getmaxyx()
        if self.max_y < 25 or self.max_x < 80:
            curses.endwin()
            print('Screen too small.  Must be at least 80x25')
            exit(2)

    def update_fire(self):
        for i in range(10):
            randval = randint(0, 79)
            self.b[randval + 80 * 24] = 70
        a = []
        tmplist = []
        for i in range(self.size):
            self.b[i] = (self.b[i] + self.b[i + 1] + self.b[i + 80] + self.b[i + 81]) // 4
            tmplist.append(self.char[7] if self.b[i] > 7 else self.char[self.b[i]])
            if i % 80 > 78:
                a.append(tmplist)
                tmplist = []
        self.a = a

    def draw_fire(self):
        self.myscreen.erase()
        y = 0
        for outerrow in self.a:
            #TODO: Center this
            self.myscreen.addstr(10,30, "testing")
            self.myscreen.addstr(5,30, "testing")
            x = 0
            for innerrow in outerrow:
                # if (y == 10):
                    # offset right
                    # self.myscreen.addstr(y, x+1, "testingjabroni")
                if curses.has_colors():
                    self.myscreen.addstr(y, x, innerrow, curses.color_pair(self.cursescolor))
                else:
                    self.myscreen.addstr(y, x, innerrow)
                x += 1
            y += 1
        self.myscreen.refresh()

    def handle_color_cycling(self):
        if curses.has_colors() and self.options.cycle and (time() - self.last_cycle_changed) > self.options.cycle_time:
            self.last_cycle_changed = time()
            self.cursescolor = 1 if self.cursescolor == len(self.options.validcolors.keys()) else self.cursescolor + 1
    
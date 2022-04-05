#!/usr/bin/env python

import curses, time

def move(win, pos, dir, snake, slen) :
    # overwrite old head with a body cell
    if snake :
        win.addch(snake[0][0], snake[0][1], 'o')

    if win.inch(*pos) != 32 :
        # CRASH!
        win.addch(pos[0], pos[1], '*')
        return None

    # draw new head
    win.addch(pos[0], pos[1], '8')
    snake.insert(0, pos)
    if len(snake) > slen :
        v = snake.pop()
        win.addch(v[0], v[1], ' ')
    win.move(0,0)
    win.refresh()

    return pos[0]+dir[0], pos[1]+dir[1]

def border(win) :
    my,mx = win.getmaxyx()
    for x in xrange(0,mx) :
        win.addch(0, x, '=')
        win.addch(my-2, x, '=')
    for y in xrange(0,my) :
        win.addch(y, 0, '|')
        win.addch(y, mx-2, '|')

# XXX update screensize dynamically?

def game(win) :
    scrsz = win.getmaxyx()
    pos = scrsz[0]/2, scrsz[1]/2
    dir = 0,1

    slen = 3 
    snake = []

    border(win)
    win.refresh()

    done = False
    cnt = 0
    while not done :
        time.sleep(0.13)
        cnt += 1 

        # occasionally increase length
        if cnt % 10 == 0 :
            slen += 1

        win.addstr(scrsz[0]-1, 5, "Score: %d   " % cnt)
        try :
            key = win.getkey()
        except :
            key = None
        #win.addstr(0,5, "key %r       " % key)

        if key == 'KEY_LEFT' :
            dir = (0,-1)
        elif key == 'KEY_RIGHT' :
            dir = (0,1)
        elif key == 'KEY_UP' :
            dir = (-1,0)
        elif key == 'KEY_DOWN' :
            dir = (1,0)
        elif key == 'q' :
            done = 1
        
        pos = move(win, pos, dir, snake, slen)
        if pos is None :
            win.addstr(1,1, "CRASSSSHHHHHHH!!!!!!")
            win.refresh()
            time.sleep(3)
            done = True
    return cnt


score = 0
try :
    win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    win.keypad(1)
    win.nodelay(1)
    score = game(win)
finally :
    curses.endwin()
print "final score", score

# Copyright (c) 2012 Matthew Denson
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import random

def input_entry(prompt, choices):
    entry=raw_input('{0} '.format(prompt)).lower()
    if entry in choices:
        return entry

    promptvalid = '-- What? Valid answers are ({1}) \n{0} '.format(prompt, ', '.join(choices))
    while entry not in choices:
         entry = raw_input(promptvalid).lower()
    return entry
    
def showInstructions():
    inst_ans = input_entry('Would you like to read the instructions? ', ('y', 'n'))
    if inst_ans == 'y':
        print """
Welcome to "Hunt the Wumpus"
============================
   The wumpus lives in a cave of 20 rooms. Each room
has 3 tunnels leading to other rooms. (Look at a
dodecahedron to see how this works. If you don't know
what a dodecahedron is, ask someone.)

Hazards:
--------
   Bottomless pits - Two rooms have bottomless pits in them
       if you go in there, you will fall into the pit (& lose!)
   Super bats - Two other rooms have super bats. If you 
       go there, a bat grabs you and takes you to some other
       room at random. (Which might be troublesome.)

"""
        raw_input('         -- Press Enter or Return to contine --')
        print """
Wumpus:
-------
   The wumpus is not bothered by the hazards. (He has sucker
feet and is too big for a bat to lift.) Usually he is asleep.
Two things wake him up: your entering his room or your shooting
an arrow.
   If the wumpus wakes, he moves (P=.75) one room or stays
still (P=.25). After that, if he is where you are, he eats you
up (& you lose!)

"""
        raw_input('         -- Press Enter or Return to contine --')
        print """
You:
----
Each turn you may move or shoot a crooked arrow.
 - Moving: You can go one room (thru one tunnel.)
 - Arrows: You have 5 arrows. You lose when you run out.
              Each arrow can go from 1 to 5 rooms. You aim 
           by telling  the computer the room #s you want the 
           arrow to go to.
              If the arrow can't go that way (i.e. no tunnel)
           it moves at random to the next room.
         - If the arrow hits the wumpus, you win.
         - If the arrow hits you, you lose.

"""
        raw_input('         -- Press Enter or Return to contine --')
        print """
Warnings:
---------
   When you are one room away from wumpus or a hazard, the
computer says:
- Wumpus "I smell a wumpus!"
- Bat    "Bats nearby!"
- Pit    "I feel a draft!" """

CAVE = ((), 
    ('2','5','8'), ('1','3','10'), ('2','4','12'), ('3','5','14'), ('1','4','6'),
    ('5','7','15'), ('6','8','17'), ('1','7','9'), ('8','10','18'), ('2','9','11'),
    ('10','12','19'), ('3','11','13'), ('12','14','20'), ('4','13','15'), ('6','14','16'),
    ('15','17','20'), ('7','16','18'), ('9','17','19'), ('11','18','20'), ('13','16','19'))
DEAD = 1
ALIVE = 0
WON = 2

class GameState(object):
    def __init__(self):
        bag = range(1, 21)
        random.shuffle(bag)
        # locations holds the player and hazard locations
        #  [player, wumpus, pit, pit, bats, bats]
        self.locations = bag[:6]
        self.saved_locations = list(self.locations)
        self.arrows = 5
    def reset(self):
        self.locations = list(self.saved_locations)
        self.arrows = 5
        
def print_warnings_and_location(locs):
    for i, loc in enumerate(locs[1:]):
        if str(loc) in CAVE[locs[0]]:
            if i == 0:
                print "I smell a wumpus!"
            elif 1 <= i <= 2:
                print "I feel a draft!"
            else:
                print "Bats nearby!"
    print 'You are in room {0}'.format(locs[0])
    print 'Tunnels lead to rooms {0}'.format(', '.join(CAVE[locs[0]])) 

def move_wumpus(locs):
    k = random.randint(0,3)
    if k < 3:
        locs[1] = int(CAVE[locs[1]][k])

def get_arrow_path():
    numrooms = int(input_entry(' How Many Rooms? ', list(str(i) for i in range(1,6))))
    path = []
    i=0
    while i<numrooms:
        room = int(input_entry('  Room #{}? '.format(i+1), list(str(i) for i in range(1,21))))
        if i>1 and path[i-2]==room:
            print "Arrows aren't that crooked. - Try another room."
        else:
            path.append(room)
            i = i + 1
    return path

def check_arrow_path(path, game):
    arrowin = game.locations[0]
    for room in path:
        if str(room) in CAVE[arrowin]:
            arrowin = room
        else:
            arrowin = int(CAVE[arrowin][random.randint(0,2)])
            
        print "{} ".format(arrowin)
        if arrowin==game.locations[1]:
            print "AHA! You got the Wumpus!\n"
            return WON
        elif arrowin==game.locations[0]:
            print "Ouch! The arrow got you!\n"
            return DEAD
    print "Missed!"
    game.arrows = game.arrows - 1
    if game.arrows==0:
        return DEAD
    move_wumpus(game.locations)
    return check_hazards(game.locations)

def check_hazards(locs):
    if locs[0] == locs[1]:
        print "OOPS!  Bumped a wumpus!"
        move_wumpus(locs)
        if locs[0] == locs[1]:
            print "Tsk Tsk Tsk -- Wumpus got you!"
            return DEAD
        else:
            return ALIVE
    if locs[0] in locs[2:4]:
        print "YYYIIIIEEEE . . . Fell in pit."
        return DEAD
    if locs[0] in locs[4:6]:
        print "ZAP--Super Bat Snatch! Elsewhereville for you!"
        locs[0] = random.randint(1, 21)
        return check_hazards(locs)
    return ALIVE

showInstructions()
game = GameState()
print "\nHunt the Wumpus\n==============="

while 1:
    print
    print_warnings_and_location(game.locations)
    print

    moveorshoot = input_entry('Shoot or Move? ', ('s','m'))
    if moveorshoot=='m':
        game.locations[0] = int(input_entry(' Where to? ', CAVE[game.locations[0]]))
        result = check_hazards(game.locations)
    else:
        path = get_arrow_path()
        result = check_arrow_path(path, game)

    if result != ALIVE:
        if result==DEAD:
            print "HA HA HA - You Lose!\n"
        elif result==WON:
            print "Hee Hee Hee - The Wumpus'll getcha next time!!\n"
            
        same = input_entry("Same Setup? ", ('y','n'))
        if same=='y':
            game.reset()
        else:
            game = GameState()

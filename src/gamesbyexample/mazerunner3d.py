"""Maze 3D, by Al Sweigart al@inventwithpython.com

Move around a maze and try to escape... in 3D!
Tags: extra-large, maze, game, artistic"""
__version__ = 0
import copy, sys, os

# Set up the constants:
WALL = '#'
EMPTY = ' '
START = 'S'
EXIT = 'E'
BLOCK = chr(9608)  # Character 9608 is '█'
NORTH = 'NORTH'
SOUTH = 'SOUTH'
EAST = 'EAST'
WEST = 'WEST'


def wallStrToWallDict(wallStr):
    wallDict = {}
    height = 0
    width = 0
    for y, line in enumerate(wallStr.splitlines()):
        if y > height:
            height = y
        for x, character in enumerate(line):
            if x > width:
                width = x
            wallDict[(x, y)] = character
    wallDict['height'] = height + 1
    wallDict['width'] = width + 1
    return wallDict

EXIT_DICT = {(0, 0): 'E', (1, 0): 'X', (2, 0): 'I',
             (3, 0): 'T', 'height': 1, 'width': 4}

ALL_OPEN = wallStrToWallDict(r'''
.................
____.........____
...|\......./|...
...||.......||...
...||__...__||...
...||.|\./|.||...
...||.|.X.|.||...
...||.|/.\|.||...
...||_/...\_||...
...||.......||...
___|/.......\|___
.................
.................'''.strip())

CLOSED = {}
CLOSED['A'] = wallStrToWallDict(r'''
_____
.....
.....
.....
_____'''.strip()) # Paste to 6, 4

CLOSED['B'] = wallStrToWallDict(r'''
.\.
..\
...
...
...
../
./.'''.strip()) # Paste to 4, 3

CLOSED['C'] = wallStrToWallDict(r'''
___________
...........
...........
...........
...........
...........
...........
...........
...........
___________'''.strip()) # Paste to 3, 1

CLOSED['D'] = wallStrToWallDict(r'''
./.
/..
...
...
...
\..
.\.'''.strip()) # Paste to 10, 3

CLOSED['E'] = wallStrToWallDict(r'''
..\..
...\_
....|
....|
....|
....|
....|
....|
....|
....|
....|
.../.
../..'''.strip()) # Paste to 0, 0

CLOSED['F'] = wallStrToWallDict(r'''
../..
_/...
|....
|....
|....
|....
|....
|....
|....
|....
|....
.\...
..\..
'''.strip()) # Paste to 12, 0 TODO note the extra new line

def displayWallDict(wallDict):
    print(BLOCK * (wallDict['width'] + 2))
    for y in range(wallDict['height']):
        print(BLOCK, end='')
        for x in range(wallDict['width']):
            wall = wallDict[(x, y)]
            if wall == '.':
                wall = ' '
            print(wall, end='')
        print(BLOCK)  # Print block with a newline.
    print(BLOCK * (wallDict['width'] + 2))


def pasteWallDict(srcWallDict, dstWallDict, left, top):
    dstWallDict = copy.copy(dstWallDict)
    for x in range(srcWallDict['width']):
        for y in range(srcWallDict['height']):
            dstWallDict[(x + left, y + top)] = srcWallDict[(x, y)]
    return dstWallDict


def makeWallDict(maze, playerx, playery, playerDirection, exitx, exity):
    if playerDirection == NORTH:
        # Map of the sections, relative  A
        # to the player @:              BCD (Player facing north)
        #                               E@F
        offsets = (('A', 0, -2), ('B', -1, -1), ('C', 0, -1),
                   ('D', 1, -1), ('E', -1, 0), ('F', 1, 0))
    if playerDirection == SOUTH:
        # Map of the sections, relative F@E
        # to the player @:              DCB (Player facing south)
        #                                A
        offsets = (('A', 0, 2), ('B', 1, 1), ('C', 0, 1),
                   ('D', -1, 1), ('E', 1, 0), ('F', -1, 0))
    if playerDirection == EAST:
        # Map of the sections, relative EB
        # to the player @:              @CA (Player facing east)
        #                               FD
        offsets = (('A', 2, 0), ('B', 1, -1), ('C', 1, 0),
                   ('D', 1, 1), ('E', 0, -1), ('F', 0, 1))
    if playerDirection == WEST:
        # Map of the sections, relative  DF
        # to the player @:              AC@ (Player facing west)
        #                                BE
        offsets = (('A', -2, 0), ('B', -1, 1), ('C', -1, 0),
                   ('D', -1, -1), ('E', 0, 1), ('F', 0, -1))

    section = {}
    for sec, xOffset, yOffset in offsets:
        section[sec] = maze.get((playerx + xOffset, playery + yOffset), WALL)
        if (playerx + xOffset, playery + yOffset) == (exitx, exity):
            section[sec] = EXIT

    wallDict = copy.copy(ALL_OPEN)
    PASTE_CLOSED_TO = {'A': (6, 4), 'B': (4, 3), 'C': (3, 1),
                       'D': (10, 3), 'E': (0, 0), 'F': (12, 0)}
    for sec in 'ABDCEF':
        if section[sec] == WALL:
            wallDict = pasteWallDict(CLOSED[sec], wallDict, PASTE_CLOSED_TO[sec][0], PASTE_CLOSED_TO[sec][1])

    # Draw the EXIT sign if needed:
    if section['C'] == EXIT:
        wallDict = pasteWallDict(EXIT_DICT, wallDict, 7, 9)
    if section['E'] == EXIT:
        wallDict = pasteWallDict(EXIT_DICT, wallDict, 0, 11)
    if section['F'] == EXIT:
        wallDict = pasteWallDict(EXIT_DICT, wallDict, 13, 11)

    return wallDict


print('''MAZE RUNNER 3D
By Al Sweigart al@inventwithpython.com

(Maze files are generated by mazemakerrec.py)''')

# Get the maze file's filename from the user:
while True:
    print('Enter the filename of the maze (or LIST or QUIT):')
    filename = input()

    # List all the maze files in the current folder:
    if filename.upper() == 'LIST':
        print('Maze files found in', os.getcwd())
        for fileInCurrentFolder in os.listdir():
            if (fileInCurrentFolder.startswith('maze') and
            fileInCurrentFolder.endswith('.txt')):
                print('  ', fileInCurrentFolder)
        continue

    if filename.upper() == 'QUIT':
        sys.exit()

    if os.path.exists(filename):
        break
    print('There is no file named', filename)

# Load the maze from a file:
mazeFile = open(filename)
maze = {}
lines = mazeFile.readlines()
playerx = None
playery = None
exitx = None
exity = None
y = 0
for line in lines:
    WIDTH = len(line.rstrip())
    for x, character in enumerate(line.rstrip()):
        assert character in (WALL, EMPTY, START, EXIT), 'Invalid character at column {}, line {}'.format(x + 1, y + 1)
        if character in (WALL, EMPTY):
            maze[(x, y)] = character
        elif character == START:
            playerx, playery = x, y
            maze[(x, y)] = EMPTY
        elif character == EXIT:
            exitx, exity = x, y
            maze[(x, y)] = EMPTY
    y += 1
HEIGHT = y

assert playerx != None and playery != None, 'No start point in file.'
assert exitx != None and exity != None, 'No exit point in file.'
playerDirection = NORTH


while True: # Main game loop.
    displayWallDict(makeWallDict(maze, playerx, playery, playerDirection, exitx, exity))

    while True: # Get user move.
        print('Location ({}, {})  Compass: {}'.format(playerx, playery, playerDirection))
        print('                            (F)ORWARD           (W)')
        print('Enter direction, or QUIT: (L)EFT (R)IGHT -or- (A) (D)')
        move = input().upper()

        if move == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if move not in ['F', 'L', 'R', 'W', 'A', 'D'] and not move.startswith('T'):
            print('Invalid direction. Enter one of F, L, or R (or W, A, D).')
            continue

        # Move the player according to their intended move:
        if move == 'F' or move == 'W':
            if playerDirection == NORTH and maze[(playerx, playery - 1)] == EMPTY:
                playery -= 1
                break
            if playerDirection == SOUTH and maze[(playerx, playery + 1)] == EMPTY:
                playery += 1
                break
            if playerDirection == EAST and maze[(playerx + 1, playery)] == EMPTY:
                playerx += 1
                break
            if playerDirection == WEST and maze[(playerx - 1, playery)] == EMPTY:
                playerx -= 1
                break
        elif move == 'L' or move == 'A':
            playerDirection = {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH}[playerDirection]
            break
        elif move == 'R' or move == 'D':
            playerDirection = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}[playerDirection]
            break
        elif move.startswith('T'):  # Cheat code: 'T x,y'
            playerx, playery = move.split()[1].split(',')
            playerx = int(playerx)
            playery = int(playery)
            break
        else:
            print('You cannot move in that direction.')

    if (playerx, playery) == (exitx, exity):
        # TODO - display the maze one last time.
        print('You have reached the exit! Good job!')
        print('Thanks for playing!')
        sys.exit()

    # At this point, go back to the start of the main game loop.

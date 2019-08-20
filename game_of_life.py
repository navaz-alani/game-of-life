from random import randint
from time import sleep
from os import system
from sys import argv
from colorama import Back as B


def make_grid(x, y):
    grid = []
    for _ in range(x):
        row = []
        for _ in range(y):
            row.append(0)
        grid.append(row)
    return grid


class Grid(object):
    def __init__(self, x, y):
        self.x = x  # Rows
        self.y = y  # Columns
        self.state = make_grid(x, y)  # Initialize the grid

    def rand_state(self, n):
        '''
        Sets a random state with n initial alive to the current Grid
        '''
        for _ in range(n):
            rand_row = randint(0, self.x-1)
            rand_col = randint(0, self.y-1)
            self.state[rand_row][rand_col] = 1

    def stat(self, point):
        '''
        Returns True indicating cell is alive, False otherwise
        '''
        if point != None:
            i = point[0]
            j = point[1]
            if self.state[i][j]:
                # Cell is alive
                return True
        # Cell is dead
        return False

    def next_state(self):
        '''
        Computes and returns the changes to be made to the current Grid's state to advance to the next cycle.
        '''
        changes = {
            "kill": [],
            "revive": []
        }
        for i in range(self.x):
            for j in range(self.y):
                alive, _ = self.cell_count(i, j)
                if self.stat([i, j]):
                    if alive < 2:
                        changes["kill"].append([i, j])
                    elif alive == (2 or 3):
                        pass
                    elif alive > 3:
                        changes["kill"].append([i, j])
                else:
                    if alive == 3:
                        changes["revive"].append([i, j])
        if len(changes["kill"]) == len(changes["revive"]) == 0:
            return 'still-life'
        self.push_state(changes)

    def push_state(self, changes):
        '''
        Mutates the current object's state as per the changes
        '''
        for i in changes["kill"]:
            self.state[i[0]][i[1]] = 0
        for j in changes["revive"]:
            self.state[j[0]][j[1]] = 1

    def cell_count(self, i, j):
        '''
        Returns alive and dead neighbor counts
        '''
        cells_around = [
            # Cell above
            self.stat([i-1, j] if (i != 0) else None),
            # Cell below
            self.stat([i+1, j] if i != self.x-1 else None),
            # Cell to the left
            self.stat([i, j-1] if j != 0 else None),
            # Cell to the right
            self.stat([i, j+1] if j != self.y-1 else None),
            # Cell at top-right
            self.stat([i-1, j+1] if (
                (i != 0) and (j != self.y-1)
            ) else None),
            # Cell at top-left
            self.stat([i-1, j-1] if (
                (i != 0) and (j != 0)
            ) else None),
            # Cell at bottom-right
            self.stat([i+1, j+1] if (
                (i != self.x-1) and (j != self.y-1)
            ) else None),
            # Cell at bottom-left
            self.stat([i+1, j-1] if (
                (i != self.x-1) and (j != 0)
            ) else None)
        ]
        alive, dead = 0, 0
        for i in cells_around:
            if i:
                alive += 1
            else:
                dead += 1
        return alive, dead

    def __repr__(self):
        '''
        Command line output styling
        '''
        str_repr = B.BLACK+""
        for i in self.state:
            strRow = []
            for j in i:
                if j == 1:
                    strRow.append(B.WHITE+" "+B.BLACK)
                else:
                    strRow.append(" ")
            str_repr += "".join(strRow)+B.RESET+"\n"
        return str_repr[:-1]


def game_of_life(x, y, n, c):
    '''
    x -> rows
    y -> cols
    n -> initial alive 
    c -> state cycles
    '''
    grid = Grid(x, y)
    grid.rand_state(n)
    t = 0.05 if (c > 1000) else 0.1
    for i in range(c):
        if grid.next_state() != 'still-life':
            sleep(t)
            system('clear')
            print("THE GAME OF LIFE")
            print("*"*y)
            print(grid)
            print(f"Cycle {i+1} of {c}\n")
        else:
            print("The Game of Life appears to have found peace in this state.")
            break


def _get_param(param_name):
    if param_name == "rows":
        prompt = "Number of rows    : "
    elif param_name == "cols":
        prompt = "Number of columns : "
    elif param_name == "ia":
        prompt = "Initial alive     : "
    else:
        prompt = "Number of cycles  : "

    stat = True
    while stat:
        tmp = input(prompt)
        if tmp.isdigit():
            return int(tmp)


def main():
    print("Welcome to the Game of Life!\n")
    print("Please enter the following information ✏️ ")
    rows = _get_param("rows")
    cols = _get_param("cols")
    initial_alive = _get_param("ia")
    cycles = _get_param("")
    print("Hope you enjoy! \nPress enter when you're ready.")
    input()
    game_of_life(rows, cols, initial_alive, cycles)
    print("Hope you enjoyed 🙏🏽")


main()

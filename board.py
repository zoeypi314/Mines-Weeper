import numpy as np
from random import randint, Random


class Board:
    def __init__(self, x: int, y: int, n: int, seed: int = None):
        self.x = x
        self.y = y
        self.num_mines = n
        self.is_active = True
        self._is_mine = np.zeros([self.x, self.y], np.bool)
        self.is_open = np.zeros([self.x, self.y], np.bool)
        self._adj_mines = np.zeros([self.x, self.y], np.int8)
        self.flag = np.zeros([self.x, self.y], np.int8)
        self.rnd = Random(seed)


        self._init_mines()
        self._init_adj()

    def _init_mines(self):
        count = 0
        mines = set()
        while count < self.num_mines:
            mine = (self.rnd.randint(0, self.x - 1), self.rnd.randint(0, self.y - 1))
            if mine not in mines:
                count += 1
                mines.add(mine)
        for x, y in mines:
            self._is_mine[x, y] = True

    def _init_adj(self):
        for x in range(self.x):
            for y in range(self.y):
                count = 0
                has_above = y >= 1
                has_below = y < self.y - 1
                has_left = x >=1
                has_right = x < self.x - 1

                if has_above and has_left:
                    if self._is_mine[x-1, y-1]:
                        count +=1
                if has_left:
                    if self._is_mine[x-1, y]:
                        count += 1
                if has_below and has_left:
                    if self._is_mine[x-1, y+1]:
                        count += 1
                if has_below:
                    if self._is_mine[x, y+1]:
                        count += 1
                if has_below and has_right:
                    if self._is_mine[x+1, y+1]:
                        count += 1
                if has_right:
                    if self._is_mine[x+1, y]:
                        count += 1
                if has_above and has_right:
                    if self._is_mine[x+1, y-1]:
                        count += 1
                if has_above:
                    if self._is_mine[x, y-1]:
                        count += 1
                self._adj_mines[x, y] = count

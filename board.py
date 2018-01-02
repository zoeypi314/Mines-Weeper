import numpy as np
from random import Random
from enum import IntEnum


class Marker(IntEnum):
    clear = 0
    flag = 1
    unknown = 2


class Board:
    def __init__(self, x: int, y: int, n: int, seed: int = None):
        self.x = x
        self.y = y
        self.num_mines = n
        self.is_active = True
        self._is_mine = np.zeros([self.x, self.y], np.bool)
        self._is_open = np.zeros([self.x, self.y], np.bool)
        self._adj_mines = np.zeros([self.x, self.y], np.int8)
        self._marker = np.zeros([self.x, self.y], np.int8)
        self._rnd = Random(seed)
        self.remaining_closed = x * y - n

        self._init_mines()
        self._init_adj()

    def _init_mines(self):
        count = 0
        mines = set()
        while count < self.num_mines:
            mine = (self._rnd.randint(0, self.x - 1), self._rnd.randint(0, self.y - 1))
            if mine not in mines:
                count += 1
                mines.add(mine)
        for x, y in mines:
            self._is_mine[x, y] = True

    def _init_adj(self):
        for x in range(self.x):
            for y in range(self.y):
                count = 0
                has_above, has_below, has_left, has_right = self._edginess(x, y)

                if has_above and has_left:
                    if self._is_mine[x-1, y-1]:
                        count += 1
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

    def _edginess(self, x: int, y: int) -> (bool, bool, bool, bool):
        has_above = y >= 1
        has_below = y < self.y - 1
        has_left = x >= 1
        has_right = x < self.x - 1
        return has_above, has_below, has_left, has_right

    def _append_mine(self, x: int, y: int, exposed: list):
        if self._is_mine[x, y]:
            exposed.append((x, y, -1))
        else:
            exposed.append((x, y, self._adj_mines[x, y]))

    def expose(self, x: int, y: int, exposed: list = None) -> list:
        if exposed is None:
            exposed = []
        if self._marker[x, y] == Marker.flag or not self.is_active:
            return exposed
        if self._is_open[x, y]:
            return exposed
        self._is_open[x, y] = True
        # Handling for landing on a mine
        if self._is_mine[x, y]:
            self.is_active = False
            for x1 in range(self.x):
                for y1 in range(self.y):
                    self._append_mine(x1, y1, exposed)
        else:
            self.remaining_closed -= 1
            if self._adj_mines[x, y] == 0:
                has_above, has_below, has_left, has_right = self._edginess(x, y)
                self._append_mine(x, y, exposed)

                if has_above and has_left:
                    self.expose(x-1, y-1, exposed)
                if has_left:
                    self.expose(x - 1, y, exposed)
                if has_below and has_left:
                    self.expose(x - 1, y + 1, exposed)
                if has_below:
                    self.expose(x, y + 1, exposed)
                if has_below and has_right:
                    self.expose(x + 1, y + 1, exposed)
                if has_right:
                    self.expose(x + 1, y, exposed)
                if has_above and has_right:
                    self.expose(x + 1, y - 1, exposed)
                if has_above:
                    self.expose(x, y - 1, exposed)

            else:
                self._append_mine(x, y, exposed)
        if self.remaining_closed == 0:
            self.is_active = False
        return exposed

    def mark(self, x: int, y: int) -> Marker:
        if self._is_open[x, y] or not self.is_active:
            # noinspection PyTypeChecker
            return None
        else:
            self._marker[x, y] = (self._marker[x, y] + 1) % 3
            return self._marker[x, y]

    def reset(self, seed: int = None):
        return Board(self.x, self.y, self.num_mines, seed)


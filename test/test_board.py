from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal
from board import Board


class BoardTest(TestCase):

    A314 = [
        [False, False, True, False, True, False, False, False, False, False],
        [False, True, True, False, False, False, False, True, False, False],
        [False, True, False, False, True, False, False, False, False, False],
        [True, False, True, False, False, True, True, True, False, True],
        [True, True, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, True, False, False, True, True],
        [False, False, False, True, False, False, True, False, True, True],
        [True, False, True, False, False, False, False, False, True, True],
        [True, False, False, False, False, False, False, True, False, False],
        [False, False, False, True, False, True, False, False, False, False]]
    B314 = np.array(A314, np.bool)
    
    J314 = [
        [1, 3, 2, 3, 0, 1, 1, 1, 1, 0],
        [2, 3, 3, 4, 2, 2, 1, 0, 1, 0],
        [3, 4, 4, 3, 1, 3, 4, 3, 3, 1],
        [3, 5, 2, 2, 2, 2, 2, 1, 2, 0],
        [2, 3, 2, 1, 2, 3, 4, 3, 4, 3],
        [2, 2, 2, 1, 2, 1, 2, 3, 3, 3],
        [1, 2, 2, 1, 2, 2, 1, 4, 5, 5],
        [1, 3, 1, 2, 1, 1, 2, 4, 4, 3],
        [1, 3, 2, 2, 2, 1, 2, 1, 3, 2],
        [1, 1, 1, 0, 2, 0, 2, 1, 1, 0]]

    def test_board_init_mines(self):
        mine_count = 30
        b = Board(10, 10, mine_count, 314)
        self.assertEqual(np.count_nonzero(b._is_mine), mine_count)
        assert_array_equal(b._is_mine, self.B314)

    def test_board_init_adj(self):
        mine_count = 30
        b = Board(10, 10, mine_count, 314)
        assert_array_equal(b._adj_mines, np.array(self.J314))

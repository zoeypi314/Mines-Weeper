from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal
from board import Board, Marker
from json.encoder import JSONEncoder
from json.decoder import JSONDecoder


class BoardTest(TestCase):

    # region example board
    SEED = 314
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
    # endregion

    def test_board_init_mines(self):
        mine_count = 30
        b = Board(10, 10, mine_count, self.SEED)
        self.assertEqual(np.count_nonzero(b._is_mine), mine_count)
        assert_array_equal(b._is_mine, np.array(self.A314, np.bool))

    def test_board_init_adj(self):
        mine_count = 30
        b = Board(10, 10, mine_count, self.SEED)
        assert_array_equal(b._adj_mines, np.array(self.J314))

    def test_mark(self):
        mine_count = 30
        b = Board(10, 10, mine_count, self.SEED)
        # case 1 - not mine
        # change mode
        self.assertEqual(b.mark(0, 0), Marker.flag)
        self.assertEqual(b.mark(0, 0), Marker.unknown)
        self.assertEqual(b.mark(0, 0), Marker.clear)
        self.assertEqual(b.mark(0, 0), Marker.flag)
        # check expose locking of flag
        self.assertEqual(len(b.expose(0, 0)), 0)
        # check not expose locking of unknown
        self.assertEqual(b.mark(0, 0), Marker.unknown)
        self.assertEqual(len(b.expose(0, 0)), 1)
        # check can't mark if exposed already
        self.assertIsNone(b.mark(0, 0))

        self.assertEqual(b.mark(1, 1), Marker.flag)
        self.assertEqual(b.mark(1, 1), Marker.unknown)
        self.assertEqual(b.mark(1, 1), Marker.clear)
        self.assertEqual(b.mark(1, 1), Marker.flag)
        self.assertEqual(len(b.expose(1, 1)), 0)
        # check expose locking of flag
        self.assertEqual(len(b.expose(1, 1)), 0)
        # check not expose locking of unknown
        self.assertEqual(b.mark(1, 1), Marker.unknown)
        self.assertEqual(len(b.expose(1, 1)), 100)
        self.assertFalse(b._is_active)
        # check can't mark when game is over
        self.assertIsNone(b.mark(1, 1))
        self.assertIsNone(b.mark(1, 0))

    def test_expose(self):
        mine_count = 30
        # case 1 - single expose
        b = Board(10, 10, mine_count, self.SEED)
        e = b.expose(0, 0)
        self.assertEqual(len(e), 1)
        self.assertTupleEqual(e[0], (0, 0, 1))
        self.assertTrue(b._is_active)
        self.assertEqual(b.remaining_closed, 69)

        # case 2 - expose a mine
        e = b.expose(1, 1)
        self.assertEqual(len(e), 100)
        self.assertTupleEqual(e[11], (1, 1, -1))
        self.assertFalse(b._is_active)
        # Check that the board doesn't respond when game is over
        e = b.expose(1, 0)
        self.assertEqual(len(e), 0)
        # case 3 - expose span
        b = b.reset(self.SEED)
        e = b.expose(0, 9)

        self.assertEqual(len(e), 6)
        self.assertTupleEqual(e[0], (0, 9, 0))
        self.assertTupleEqual(e[1], (1, 9, 0))
        self.assertTupleEqual(e[2], (0, 8, 1))
        self.assertTupleEqual(e[3], (2, 9, 1))
        self.assertTupleEqual(e[4], (2, 8, 3))
        self.assertTupleEqual(e[5], (1, 8, 1))
        self.assertTrue(b.is_active)
        self.assertEqual(b.remaining_closed, 64)

        # case 4 - game won
        b = Board(10, 10, 1, self.SEED)
        e = b.expose(0, 0)
        self.assertEqual(len(e), 99)
        self.assertTupleEqual(e[0], (0, 0, 0))
        self.assertFalse(b._is_active)
        self.assertEqual(b.remaining_closed, 0)

    def test_to_json(self):
        mine_count = 30
        b = Board(10, 10, mine_count, self.SEED)
        b.expose(0, 9)
        json = b.to_json()
        json = JSONDecoder().decode(json)
        self.assertEqual(json['x'], 10)
        self.assertEqual(json['y'], 10)
        self.assertEqual(json['num_mines'], 30)
        self.assertEqual(json['rem_mines'], 30)
        self.assertEqual(json['_is_active'], True)
        self.assertEqual(json['_is_mine'][0][0], False)
        self.assertEqual(json['_is_mine'][0][2], True)
        self.assertEqual(json['_is_open'][0][8], True)
        self.assertEqual(json['_is_open'][0][7], False)
        self.assertEqual(json['_adj_mines'][0][0], 1)
        self.assertEqual(json['_adj_mines'][0][2], 2)
        self.assertEqual(json['_marker'][0][0], 0)
        self.assertEqual(json['remaining_closed'], 64)
        self.assertNotIn('_rnd', json)

    def test_from_json(self):
        mine_count = 30
        b = Board(10, 10, mine_count, self.SEED)
        b.expose(0, 9)
        json = b.to_json()
        board = Board.from_json(json)[0]

        self.assertEqual(board.x, 10)
        self.assertEqual(board.y, 10)
        self.assertEqual(board.num_mines, 30)
        self.assertEqual(board.rem_mines, 30)
        self.assertEqual(board._is_active, True)
        self.assertEqual(board._is_mine[0, 0], False)
        self.assertEqual(board._is_mine[0, 2], True)
        self.assertEqual(board._is_open[0, 8], True)
        self.assertEqual(board._is_open[0, 7], False)
        self.assertEqual(board._adj_mines[0, 0], 1)
        self.assertEqual(board._adj_mines[0, 2], 2)
        self.assertEqual(board._marker[0, 0], 0)
        self.assertEqual(board.remaining_closed, 64)


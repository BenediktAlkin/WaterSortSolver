import unittest
from wss import State, Color, Solver
import numpy as np

class SolverTests(unittest.TestCase):
    def test_solve1(self):
        state = State(
            np.array(
                [
                    [Color.RED, Color.GREEN, Color.GREEN, Color.GREEN],
                    [Color.GREEN, Color.RED, Color.EMPTY, Color.EMPTY],
                    [Color.RED, Color.RED, Color.EMPTY, Color.EMPTY],
                ],
            ),
        )
        move_history = []
        solved = Solver().solve(state, move_history_out=move_history)
        self.assertTrue(solved.is_solved)
        expected_move_history = [
            (1, 2),
            (0, 1),
            (0, 2),
        ]
        self.assertEqual(expected_move_history, move_history)


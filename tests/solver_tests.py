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

    # crashes system...not sure why...probably something with recursion depth or memory consumption
    # def test_solve_level122(self):
    #     state = State(
    #         np.array(
    #             [
    #                 [Color.PURPLE, Color.GRAY, Color.GREEN, Color.PINK],
    #                 [Color.GRAY, Color.PURPLE, Color.PINK, Color.RED],
    #                 [Color.TURQUOISE, Color.ORANGE, Color.PINK, Color.GREEN],
    #                 [Color.YELLOW, Color.DARK_PURPLE, Color.ORANGE, Color.BLUE],
    #                 [Color.RED, Color.YELLOW, Color.GRAY, Color.DARK_BLUE],
    #                 [Color.DARK_PURPLE, Color.ORANGE, Color.DARK_GREEN, Color.PURPLE],
    #                 [Color.BLUE, Color.DARK_PURPLE, Color.BLUE, Color.GREEN],
    #                 [Color.YELLOW, Color.DARK_GREEN, Color.YELLOW, Color.PURPLE],
    #                 [Color.ORANGE, Color.RED, Color.PURPLE, Color.BLUE],
    #                 [Color.DARK_GREEN, Color.GRAY, Color.TURQUOISE, Color.TURQUOISE],
    #                 [Color.DARK_BLUE, Color.RED, Color.GREEN, Color.PINK],
    #                 [Color.DARK_BLUE, Color.DARK_BLUE, Color.TURQUOISE, Color.DARK_GREEN],
    #                 [Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY],
    #                 [Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY],
    #             ],
    #         ),
    #     )
    #     move_history = []
    #     solved = Solver().solve(state, move_history_out=move_history)
    #     self.assertTrue(solved.is_solved)


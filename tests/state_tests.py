import unittest

import numpy as np

from wss import State, Color


class StateTests(unittest.TestCase):
    def test_from_list_invalid(self):
        state = State.from_list(
            [
                [Color.RED, Color.GREEN, Color.GREEN, Color.GREEN],
                [Color.GREEN, Color.RED],
            ],
        )
        expected_state = np.array(
            [
                [Color.RED, Color.GREEN, Color.GREEN, Color.GREEN],
                [Color.GREEN, Color.RED, Color.EMPTY, Color.EMPTY],
            ],
        )
        self.assertEqual((2, 4), state.flask_state.shape)
        self.assertTrue(np.all(state.flask_state == expected_state))
        self.assertFalse(state.is_valid)
        self.assertFalse(state.is_solved)
        self.assertEqual(0, len(state.valid_moves))

    def test_from_list_valid(self):
        state = State.from_list(
            [
                [Color.RED, Color.GREEN, Color.GREEN, Color.GREEN],
                [Color.GREEN, Color.RED],
                [Color.RED, Color.RED],
            ],
        )
        expected_state = np.array(
            [
                [Color.RED, Color.GREEN, Color.GREEN, Color.GREEN],
                [Color.GREEN, Color.RED, Color.EMPTY, Color.EMPTY],
                [Color.RED, Color.RED, Color.EMPTY, Color.EMPTY],
            ],
        )
        self.assertEqual((3, 4), state.flask_state.shape)
        self.assertTrue(np.all(state.flask_state == expected_state))
        self.assertTrue(state.is_valid)
        self.assertFalse(state.is_solved)
        valid_moves = state.valid_moves
        self.assertEqual(2, len(valid_moves))
        self.assertEqual((1, 2), valid_moves[0])
        self.assertEqual((2, 1), valid_moves[1])

    def test_to_string(self):
        state = State.from_list(
            [
                [Color.RED, Color.GREEN, Color.GREEN, Color.GREEN],
                [Color.GREEN, Color.RED],
            ],
        )
        expected = "\n".join(
            [
                "G  ",
                "G  ",
                "G R",
                "R G",
            ],
        )
        self.assertEqual(expected, str(state))

    def test_from_list_solved(self):
        state = State.from_list(
            [
                [Color.RED, Color.RED, Color.RED, Color.RED],
                [Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN],
                [],
            ],
        )
        expected_state = np.array(
            [
                [Color.RED, Color.RED, Color.RED, Color.RED],
                [Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN],
                [Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY],
            ],
        )
        self.assertEqual((3, 4), state.flask_state.shape)
        self.assertTrue(np.all(state.flask_state == expected_state))
        self.assertTrue(state.is_valid)
        self.assertTrue(state.is_solved)
        self.assertEqual(0, len(state.valid_moves))

    def test_step(self):
        state = State(
            np.array(
                [
                    [Color.RED, Color.GREEN, Color.GREEN, Color.GREEN],
                    [Color.GREEN, Color.RED, Color.EMPTY, Color.EMPTY],
                    [Color.RED, Color.RED, Color.EMPTY, Color.EMPTY],
                ],
            ),
        )
        self.assertEqual((3, 4), state.flask_state.shape)
        self.assertTrue(state.is_valid)
        self.assertFalse(state.is_solved)
        # step1
        state = state.step((1, 2))
        expected = np.array(
            [
                [Color.RED, Color.GREEN, Color.GREEN, Color.GREEN],
                [Color.GREEN, Color.EMPTY, Color.EMPTY, Color.EMPTY],
                [Color.RED, Color.RED, Color.RED, Color.EMPTY],
            ],
        )
        self.assertTrue(np.all(state.flask_state == expected))
        self.assertTrue(state.is_valid)
        self.assertFalse(state.is_solved)
        # step2
        state = state.step((0, 1))
        expected = np.array(
            [
                [Color.RED, Color.EMPTY, Color.EMPTY, Color.EMPTY],
                [Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN],
                [Color.RED, Color.RED, Color.RED, Color.EMPTY],
            ],
        )
        self.assertTrue(np.all(state.flask_state == expected))
        self.assertTrue(state.is_valid)
        self.assertFalse(state.is_solved)
        # step3
        state = state.step((0, 2))
        expected = np.array(
            [
                [Color.EMPTY, Color.EMPTY, Color.EMPTY, Color.EMPTY],
                [Color.GREEN, Color.GREEN, Color.GREEN, Color.GREEN],
                [Color.RED, Color.RED, Color.RED, Color.RED],
            ],
        )
        self.assertTrue(np.all(state.flask_state == expected))
        self.assertTrue(state.is_valid)
        self.assertTrue(state.is_solved)

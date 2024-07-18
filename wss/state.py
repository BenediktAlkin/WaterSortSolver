import numpy as np

from .color import Color


class State:
    def __init__(self, flask_state, num_used_moves=None, num_total_moves=None):
        super().__init__()
        self.flask_state = flask_state
        self.num_used_moves = num_used_moves or 0
        self.num_total_moves = num_total_moves or float("inf")

    def __str__(self):
        num_flasks, num_sections = self.flask_state.shape
        rows = []
        for i in range(num_sections):
            values = []
            for j in range(num_flasks):
                value = Color.int_to_char[self.flask_state[j][num_sections - 1 - i]]
                if value == "E":
                    value = " "
                values.append(value)
            rows.append(" ".join(values))
        return "\n".join(rows)

    @staticmethod
    def from_list(src, num_used_moves=None, num_total_moves=None):
        assert isinstance(src, list) and len(src) > 0
        num_flasks = len(src)
        num_sections = max(len(src[i]) for i in range(num_flasks))
        state = np.zeros((num_flasks, num_sections), dtype=np.int)
        for i in range(num_flasks):
            for j in range(len(src[i])):
                if isinstance(src[i][j], int):
                    value = src[i][j]
                elif len(src[i][j]) > 1:
                    value = Color.str_to_int[src[i][j]]
                else:
                    value = Color.char_to_int[src[i][j]]
                state[i, j] = value
        return State(flask_state=state, num_used_moves=num_used_moves, num_total_moves=num_total_moves)

    @property
    def num_sections(self):
        return self.flask_state.shape[1]

    @property
    def num_flasks(self):
        return self.flask_state.shape[0]

    @property
    def is_valid(self):
        # check if all colors are exactly num_sections time in state
        num_sections = self.num_sections
        unique, counts = np.unique(self.flask_state, return_counts=True)
        for i in range(len(unique)):
            if unique[i] == 0:
                continue
            if counts[i] != num_sections:
                return False
        # TODO check if EMPTY is always on top (e.g. [Color.RED, Color.EMPTY, Color.RED, Color.RED] is invalid)
        return True

    @property
    def valid_moves(self):
        moves = []
        for src_flask_idx in range(self.num_flasks):
            # check if flask is finished/empty
            _, counts = np.unique(self.flask_state[src_flask_idx], return_counts=True)
            if len(counts) == 1 and counts[0] == self.num_sections:
                continue

            # determine src_color and required_space
            # TODO theoretically one could also pour a part of the top color of one flask into another flask
            #  (e.g. flask0 has 3xBLUE on top and flask1 has 2xRED BLUE -> one could pour 1 BLUE from flask0 to flask1)
            required_space = 0
            src_color = None
            for src_section_idx in range(self.num_sections):
                cur_color = self.flask_state[src_flask_idx, self.num_sections - 1 - src_section_idx]
                if cur_color == Color.EMPTY:
                    continue
                if src_color is None:
                    src_color = cur_color
                if src_color == cur_color:
                    required_space += 1
                else:
                    break
            assert src_color is not None

            # iterate over flasks to determine valid moves
            for dst_flask_idx in range(self.num_flasks):
                if src_flask_idx == dst_flask_idx:
                    continue
                # determine dst_color and available_space
                dst_color = Color.EMPTY
                available_space = 0
                for dst_section_idx in range(self.num_sections):
                    cur_color = self.flask_state[dst_flask_idx, self.num_sections - 1 - dst_section_idx]
                    if cur_color == Color.EMPTY:
                        available_space += 1
                        continue
                    dst_color = cur_color
                    break
                # checks
                if dst_color != Color.EMPTY:
                    if dst_color != src_color:
                        continue
                    if available_space < required_space:
                        continue

                moves.append((src_flask_idx, dst_flask_idx))
        return moves

    @property
    def is_solved(self):
        # all flasks need to be filled with the same color (also counts for Color.EMPTY)
        for i in range(self.num_flasks):
            _, counts = np.unique(self.flask_state[i], return_counts=True)
            if len(counts) != 1 or counts[0] != self.num_sections:
                return False
        return True

    def clone(self):
        return State(
            flask_state=self.flask_state.copy(),
            num_used_moves=self.num_used_moves,
            num_total_moves=self.num_total_moves,
        )

    def step(self, move):
        src_flask_idx, dst_flask_idx = move
        assert src_flask_idx != dst_flask_idx
        assert src_flask_idx >= 0
        assert dst_flask_idx >= 0
        state = self.clone()

        # determine required_space
        src_color = None
        required_space = 0
        for src_section_idx in range(self.num_sections):
            cur_color = self.flask_state[src_flask_idx, self.num_sections - 1 - src_section_idx]
            if cur_color == Color.EMPTY:
                continue
            if src_color is None:
                src_color = cur_color
            if src_color == cur_color:
                required_space += 1
            else:
                break

        # determine available_space
        dst_color = Color.EMPTY
        available_space = 0
        for dst_section_idx in range(self.num_sections):
            cur_color = self.flask_state[dst_flask_idx, self.num_sections - 1 - dst_section_idx]
            if cur_color == Color.EMPTY:
                available_space += 1
                continue
            dst_color = cur_color
            break

        # sanity check
        assert dst_color == Color.EMPTY or src_color == dst_color
        assert required_space <= available_space

        # remove water from src_flask
        for src_section_idx in range(self.num_sections):
            cur_color = state.flask_state[src_flask_idx, self.num_sections - 1 - src_section_idx]
            if cur_color == Color.EMPTY:
                continue
            if cur_color == src_color:
                # remove top non-empty section
                state.flask_state[src_flask_idx, self.num_sections - 1 - src_section_idx] = Color.EMPTY
            else:
                # finished removing water (top color is different from src_color)
                break

        # add water to dst_flask
        remaining_sections = required_space
        for dst_section_idx in range(self.num_sections):
            cur_color = state.flask_state[dst_flask_idx, dst_section_idx]
            if cur_color != Color.EMPTY:
                # skip other colors on the bottom
                continue
            else:
                # add water
                state.flask_state[dst_flask_idx, dst_section_idx] = src_color
                remaining_sections -= 1
            if remaining_sections == 0:
                break

        return state
from .state import State

class Solver:
    def solve(self, state: State, move_history_out=None) -> State:
        # check if state is solved
        valid_moves = state.valid_moves
        if len(valid_moves) == 0:
            if state.is_solved:
                return state
            return None

        # depth-fist search
        for move in valid_moves:
            next_state = state.step(move)
            final_state = self.solve(next_state, move_history_out=move_history_out)
            if final_state is not None:
                # return move_history if intiail if solve is called via e.g. solver.solve(state, move_history_out=[])
                if move_history_out is not None:
                    move_history_out.insert(0, move)
                return final_state

        return None

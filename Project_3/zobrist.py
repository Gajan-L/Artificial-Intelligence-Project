import numpy as np
import numba as nb


class Zobrist:
    def __init__(self, n):
        self.board_b = np.random.randint(2 ** 64, size=(n, n), dtype=np.uint64)
        self.board_w = np.random.randint(2 ** 64, size=(n, n), dtype=np.uint64)
        self.D = {}

    def __getitem__(self, state):
        _hash = get_hash(state, self.board_b, self.board_w)
        if _hash in self.D:
            return self.D[_hash]
        else:
            return False

    def __setitem__(self, state, value):
        _hash = get_hash(state, self.board_b, self.board_w)
        self.D[_hash] = value


@nb.njit(nb.uint64(nb.int8[:, :], nb.uint64[:, :], nb.uint64[:, :]))
def get_hash(state, board_b, board_w):
    _hash = 0
    n = state.shape[0]
    for y in range(n):
        for x in range(n):
            if state[y, x] == 1:
                _hash ^= board_b[y, x]
            elif state[y, x] == -1:
                _hash ^= board_w[y, x]
    return _hash

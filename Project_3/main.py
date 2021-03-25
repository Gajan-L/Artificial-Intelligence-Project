from eve import Eve
from pve import Pve
from online import Online


class Config:
    N = 12
    M = 6
    DEPTH = 4
    SAVE_PERMISSION = False


def main():
    c = Config()
    mode = int(input('Please choose the game mode of Tic Tac Toe:\n1: EvE\t2: PvE\t3:Online\n'))
    if mode == 1:
        g = Eve(c.N, c.M, c.DEPTH, c.SAVE_PERMISSION)
    elif mode == 2:
        g = Pve(c.N, c.M, c.DEPTH, c.SAVE_PERMISSION)
    elif mode == 3:
        # user_id = input('user id:')
        # team_id = input('team id:')
        game_id = input('game id:')
        fast_list = [[1077, 1271, game_id],[1079, 1272, game_id]]
        ind = int(input('fast list:\n0: 1271\t1: 1272\n'))
        user_id, team_id, game_id = fast_list[ind]
        g = Online(c.N, c.M, c.DEPTH, c.SAVE_PERMISSION, user_id, team_id, game_id)
    g.start_game()
    return g


if __name__ == '__main__':
    G = main()

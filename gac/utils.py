class Best(object):
    def __init__(self, v, r=0, c=0):
        """ Holds the best move"""
        # value of move
        self.val = v
        # row of move
        self.row = r
        # column of move
        self.column = c

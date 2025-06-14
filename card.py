class Card:
    def __init__(self, ID, N, E, S, W, img="default.png", colour=(255, 255, 255), is_hidden=False):
        self.ID = ID
        self.N = N
        self.E = E
        self.S = S
        self.W = W
        self.img = img
        self.colour = colour
        self.is_hidden = is_hidden

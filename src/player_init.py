from random import randint

NAME_FILE="../assets/player_names.txt"

class Player:
    def __init__(self, name, pos, bomb=False):
        if name != "_":
            self.name = name
        else:
            self.name = self.random_name()
        self.pos = pos # position is tuple (x,y)
        self.bomb = bomb # True if player starts with bomb or holds bomb

    def __repr__(self):
        return f"{self.name} is at {self.pos}. Bomb: {self.bomb}"

    def random_name(self):
        choice = randint(0,51)
        file = open(NAME_FILE)
        content = file.readlines()
        return content[choice].strip()

    def has_bomb(self.bomb):
        return self.bomb

    def location(self):
        return self.pos

    def get_bomb(self, other):
        other.bomb = False
        self.bomb = True

    def give_bomb(self, other):
        self.bomb = False
        other.bomb = True

    def move_player(self, x, y):
        pos_x, pos_y = self.pos
        self.pos = (pos_x+x, pos_y+y)

player1 = Player("_",(16,17),False)
print(player1)

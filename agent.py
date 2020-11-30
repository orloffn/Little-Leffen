from keras import Sequential
from gamestate import GameState


class Agent():
    """docstring for Agent"""
    def __init__(self):
        self.model = Sequential()
        self.game = GameState()

    def read_state(self):
        """
        parse the next gamestate to get inputs for the network
        return array representation of melee state
        """
        s = self.game.get_next_state()
        out = [s.distance]
        # for i in s.player:
        """
        return data from bot port before data from oponent port
        """


if __name__ == '__main__':
    test = Agent()
    print(test.read_state())
        
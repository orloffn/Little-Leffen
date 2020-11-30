from melee.enums import Button
from game import Game

class GameState(Game):
    """docstring for GameState"""
    def __init__(self):
        super(GameState, self).__init__()

    def press_a(self):
        self.pad.press_button(Button.BUTTON_A)

    def press_b(self):
        self.pad.press_button(Button.BUTTON_B)

    def press_x(self):
        self.pad.press_button(Button.BUTTON_X)

    def press_l(self):
        self.pad.press_button(Button.BUTTON_L)

    def press_r(self):
        self.pad.press_button(Button.BUTTON_R)

    def press_z(self):
        self.pad.press_button(Button.BUTTON_Z)

    def press_start(self):
        self.pad.press_button(Button.BUTTON_START)

    def clear_buttons(self):
        self.pad.release_all()

    def get_next_state(self):
        return self.con.step()

    def get_actions(self):
        return [self.press_a,
                self.press_b,
                self.press_x,
                self.press_l,
                self.press_r,
                self.press_z,
                self.press_start]


if __name__ == '__main__':
    obj = GameState()
    while True:
        obj.get_next_state()
        obj.clear_buttons()
        obj.get_next_state()
        obj.press_b()

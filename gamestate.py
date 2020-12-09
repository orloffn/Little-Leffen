from melee.enums import Button
from melee import Menu
from game import Game

# TODO: Actions for moving sticks
# TODO: Action for setting analog trigger

class GameState():
    """docstring for GameState"""

    NUM_ACTIONS = 8         # TODO: programmatically get these instead of hardcoding
    NUM_OBSERVATIONS = 41

    def __init__(self, game):
        self.game = game
        self.current_state = None

    def press_a(self):
        self.game.pad.press_button(Button.BUTTON_A)

    def press_b(self):
        self.game.pad.press_button(Button.BUTTON_B)

    def press_x(self):
        self.game.pad.press_button(Button.BUTTON_X)

    def press_r(self):
        self.game.pad.press_button(Button.BUTTON_R)

    def press_z(self):
        self.game.pad.press_button(Button.BUTTON_Z)

    def set_light_shield(self):
        self.game.pad.press_shoulder(Button.BUTTON_L, .1)

    def set_grey_stick(self, coord):
        x, y = coord
        self.game.pad.tilt_analog(Button.BUTTON_MAIN, x, y)

    def set_c_stick(self, val):
        if val == 0:
            x = y = .5
        elif val == 1:
            x, y = 0, .5
        elif val == 2:
            x, y = .5, 1
        elif val == 3:
            x, y = 1, .5
        elif val == 4:
            x, y = .5, 0
        self.game.pad.tilt_analog(Button.BUTTON_C, x, y)

    def clear(self):
        self.game.pad.release_all()

    def step(self):
        s = self.game.con.step()
        self.current_state = s
        if not s.menu_state == Menu.IN_GAME:
            return []
        return s

    def get_state_list(self, s):
        out = [s.distance]
        out += self.get_playerdata(s.player[self.game.port])
        for i in [k for k in s.player.keys() if k != self.game.port]:
            out += self.get_playerdata(s.player[i])
        return out

    def get_actions(self):
        return [self.press_a,
                self.press_b,
                self.press_x,
                self.press_r,
                self.press_z,
                self.set_light_shield,
                self.set_grey_stick,
                self.set_c_stick]

    @staticmethod
    def get_playerdata(p):
        """
        get state of a player for game state function
        """
        return [p.action.value,
                p.action_frame,
                int(p.facing),
                int(p.hitlag),
                p.hitstun_frames_left,
                p.invulnerability_left,
                int(p.invulnerable),
                p.jumps_left,
                int(p.off_stage),
                int(p.on_ground),
                p.percent,
                p.shield_strength,
                p.speed_air_x_self,
                p.speed_ground_x_self,
                p.speed_x_attack,
                p.speed_y_attack,
                p.speed_y_self,
                p.stock,
                p.x,
                p.y]

    def is_done(self, state):
        if self.current_state.menu_state == Menu.IN_GAME:
            for i in self.current_state.player:
                if self.current_state.player[i].stock == 0:
                    return True
            return False
        return True


if __name__ == '__main__':
    game = Game(4)
    test = GameState(game)
    while True:
        test.clear_buttons()
        test.step()
        test.press_b()
        test.step()

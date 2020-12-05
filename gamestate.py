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
                self.press_z]

    @staticmethod
    def get_playerdata(p):
        """
        get state of a player for game state function
        """
        return [p.action.value,
                p.action_frame,
                p.ecb_bottom,
                p.ecb_left,
                p.ecb_right,
                p.ecb_top,
                p.facing,
                p.hitlag,
                p.hitstun_frames_left,
                p.invulnerability_left,
                p.invulnerable,
                p.jumps_left,
                p.off_stage,
                p.on_ground,
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

    def read_state(self):
        """
        parse the next gamestate to get inputs for the network
        return array representation of melee state
        """
        s = self.game.get_next_state()
        out = [s.distance]
        out += self.get_playerdata(s.player[4])
        for i in [k for k in s.player.keys() if k is not 4]:
            out += self.get_playerdata(s.player[i])
        return out

if __name__ == '__main__':
    obj = GameState()
    while True:
        obj.get_next_state()
        obj.clear_buttons()
        obj.get_next_state()
        obj.press_b()

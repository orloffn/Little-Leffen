import keras
from keras.layers import Dense
from keras.models import Sequential
from gamestate import GameState


class Agent():
    """docstring for Agent"""
    def __init__(self):
        self.model = self.build_model()
        self.game = GameState()

    @staticmethod
    def build_model():
        model = Sequential()
        model.add(Dense(47, activation='relu', input_shape=(1,)))
        model.add(Dense(7, activation='softmax'))
        model.compile(optimizer='sgd', loss='categorical_crossentropy')
        return model

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
    test = Agent()
    test.game.get_to_the_fun_part()
    print(test.read_state())
        
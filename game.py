"""
https://libmelee.readthedocs.io/en/latest/
"""
import melee
from time import sleep


GAME_PATH = 'StreamableDolphin'
ISO_PATH = '../../../SSBMv102.iso'


class Game():
    """docstring for Game"""
    def __init__(self, p, partner=False):
        self.port = p
        self.con = melee.Console(path=GAME_PATH)
        self.pad = melee.Controller(console=self.con, port=p)
        self.partner = partner
        if not partner:
            self.con.run(iso_path = ISO_PATH)
        print('console connect: {}'.format(self.con.connect()))
        self.pad.connect()
        print('test port: {}'.format(p))

    def get_to_the_fun_part(self,
                            char=melee.enums.Character.FOX,
                            stage=melee.enums.Stage.RANDOM_STAGE):
        state = self.con.step()
        while state.menu_state is not melee.Menu.IN_GAME:
            melee.MenuHelper.menu_helper_simple(state,
                                                self.pad,
                                                char,
                                                stage,
                                                '',
                                                autostart=True,
                                                swag=False)
            state = self.con.step()
        return state

    def manual_menu(self,
                    state,
                    char=melee.enums.Character.FOX,
                    stage=melee.enums.Stage.RANDOM_STAGE):
        if not self.partner:
            if state.menu_state is not melee.Menu.IN_GAME:
                melee.MenuHelper.menu_helper_simple(state, self.pad, char, stage, '', autostart=True, swag=False)
        elif state.menu_state is melee.Menu.CHARACTER_SELECT:
            melee.MenuHelper.menu_helper_simple(state, self.pad, char, stage, '', autostart=True, swag=False)
        return self.con.step()


if __name__ == '__main__':
    test = Game(4)
    test2 = Game(3, True)
    test.get_to_the_fun_part()
            

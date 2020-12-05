"""
https://libmelee.readthedocs.io/en/latest/
"""
import melee


GAME_PATH = '../FM-Slippi'


class Game():
    """docstring for Game"""
    def __init__(self):
        self.con = melee.Console(path=GAME_PATH)
        self.pad = melee.Controller(console=self.con, port=4)
        self.con.run()
        self.con.connect()
        self.pad.connect()

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


if __name__ == '__main__':
    test = Game()
    test.get_to_the_fun_part()
            

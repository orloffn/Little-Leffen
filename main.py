"""
https://github.com/altf4/libmelee

https://libmelee.readthedocs.io/en/latest/

https://towardsdatascience.com/how-to-teach-an-ai-to-play-games-deep-reinforcement-learning-28f9b920440a
https://medium.com/acing-ai/how-i-build-an-ai-to-play-dino-run-e37f37bdf153
"""

import melee
import os
import keras

SLIPPI_DIR = '../Slippi'


def main():
    file = '{}/{}'.format(SLIPPI_DIR, os.listdir(SLIPPI_DIR)[0])
    console = melee.Console(is_dolphin=False, path=file)
    console.connect()

    while True:
        gamestate = console.step()
        # step() returns None when the file ends
        if gamestate is None:
            break
        print(gamestate.player[1].x, gamestate.player[1].y)


if __name__ == '__main__':
    main()

"""
Package a folder of Slippi files into a dataframe and save it to disk
"""

import pandas as pd
import melee
from melee.enums import Character, Button
import argparse
import os


CHARACTER = Character.FOX
DIR = 'C:/Users/ameof/Documents/Slippi'
EXPORT_FILE = 'training_data.csv'
BATCH_SIZE = 10


def get_playerdata(p):
    return [p.percent,
            p.x,
            p.y,
            int(p.hitlag_left),
            int(p.invulnerable),
            int(p.off_stage)]


def get_obs(state, port):
    out = [state.distance]
    out += get_playerdata(state.player[port])
    for i in [k for k in state.player.keys() if k != port]:
        out += get_playerdata(state.player[i])
    return out


def get_light_shield(pad):
    return int(.1 <= pad.l_shoulder <= .9 or .1 <= pad.r_shoulder <= .9)


def get_buttons(pad):
    return [int(pad.button[Button.BUTTON_A]),
            int(pad.button[Button.BUTTON_B]),
            int(pad.button[Button.BUTTON_X]),
            int(pad.button[Button.BUTTON_R]),
            int(pad.button[Button.BUTTON_Z]),
            get_light_shield(pad)]


def get_c_stick(coords):
    if coords[0] < .25: return [1]
    if coords[0] > .75: return [3]
    if coords[1] < .25: return [2]
    if coords[1] > .75: return [4]
    return [0]


def get_action(state, port):
    pad_state = state.player[port].controller_state
    return [get_buttons(pad_state) + \
           list(pad_state.main_stick) + \
           get_c_stick(pad_state.c_stick)]


def get_row(state, ports):
    return [get_obs(state, i) + get_action(state, i) for i in ports]


def find_ports_for_char(state, char):
    return [p for p in state.player if state.player[p].character == char]


def read_file(fname):
    try:
        console = melee.Console(is_dolphin=False, path=fname)
        console.connect()
    except Exception:
        return pd.DataFrame()
    state = console.step()
    ports = find_ports_for_char(state, CHARACTER)
    state_list = []
    if ports is not [] and len(state.players) == 2:
        while state is not None:
            try:
                state_list += get_row(state, ports)    
            except Exception:
                pass
            state = console.step()
    return pd.DataFrame(state_list)


def batchify(files):
    return [files[i:i+BATCH_SIZE] for i in range(0, len(files), BATCH_SIZE)]


def main():
    if os.path.exists(EXPORT_FILE):
        os.remove(EXPORT_FILE)
    for i, batch in enumerate(batchify(os.listdir(DIR))):
        print('Batch {}: {} to {}'.format(i+1, i*BATCH_SIZE, (i+1)*BATCH_SIZE))
        df = pd.concat([read_file(DIR + '/' + file) for file in batch])
        df.to_csv(EXPORT_FILE, index=False, mode='a', header=False)


if __name__ == '__main__':
    main()

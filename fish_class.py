import random
import sys

import pyasge
from gamedata import GameData


class Fish(pyasge.ASGEGame):

    def __init__(self):
        self.sprite: pyasge.Sprite

    def spawn(self, fish_amount, fish_list) -> None:
        # Two lines below determine the texture of the fish

        fish_list.append(pyasge.Sprite())
        fish_list[fish_amount].z_order = 1
        fish_list[fish_amount].scale = 1

        fish_random = random.randint(1, 7)
        fish_list[fish_amount].loadTexture("/data/images/Fishes/fishTile_0" + str(fish_random) + ".png", )

        # generate random {x,y} but don't let the fish spawn on edges
        x = random.randint(0, self.data.game_res[0] - fish_list[fish_amount].width)
        y = random.randint(0, self.data.game_res[1] - fish_list[fish_amount].height)

        fish_list[fish_amount].x = x
        fish_list[fish_amount].y = y


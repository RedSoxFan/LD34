import os

import pygame
from utils import Settings


class Sound:
    sounds = {}

    @staticmethod
    def init():
        pygame.mixer.init()
        for s in os.listdir('snd'):
            Sound.sounds[s[:s.rindex('.')]] = pygame.mixer.Sound('snd/' + s)

    @staticmethod
    def play(name):
        if name in Sound.sounds:
            if Settings.AUDIO == 1:
                Sound.sounds[name].play()
        else:
            print('ERROR: Sound "{}" not found'.format(name))

    @staticmethod
    def stop(name, fade):
        if name in Sound.sounds:
            if fade and Settings.AUDIO == 1:
                Sound.sounds[name].fadeout()
            else:
                Sound.sounds[name].stop()
        else:
            print('ERROR: Sound "{}" not found'.format(name))

    @staticmethod
    def stop_all(fade):
        map(lambda name: Sound.stop(name, fade), Sound.sounds.keys())
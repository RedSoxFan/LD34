import os

import pygame


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
            Sound.sounds[name].play()
        else:
            print('ERROR: Sound "{}" not found'.format(name))

    @staticmethod
    def stop(name, fade):
        if name in Sound.sounds:
            if fade:
                Sound.sounds[name].fadeout()
            else:
                Sound.sounds[name].stop()
        else:
            print('ERROR: Sound "{}" not found'.format(name))

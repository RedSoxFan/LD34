import os

import pygame
from utils import Settings
from random import shuffle

SONG_END = pygame.USEREVENT + 1


class Sound:
    sounds = {}
    music = []

    # music = {}

    @staticmethod
    def init():
        pygame.mixer.init()
        for s in os.listdir('snd'):
            Sound.sounds[s[:s.rindex('.')]] = pygame.mixer.Sound('snd/' + s)

    @staticmethod
    def reloadMusic():
        Sound.music = ['music/' + s for s in os.listdir('music')]
        shuffle(Sound.music)

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
        pygame.mixer.music.stop()

    @staticmethod
    def cycleMusic():
        if Settings.AUDIO == 1:
            if len(Sound.music) == 0:
                Sound.reloadMusic()
            if len(Sound.music) > 0:
                pygame.mixer.music.load(Sound.music.pop(0))
                pygame.mixer.music.set_endevent(SONG_END)
                pygame.mixer.music.play()

#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import pygame


class Arithmetic:
    @staticmethod
    def lerp(val1, val2, percent):
        return round(val1 + (val2 - val1) * percent)


class Constants:
    EXIT_SCREEN = 0
    FPS = 60
    GAME_SCREEN = 1
    GRAVITY = 9.8
    GROW_KEY = pygame.K_UP
    HEIGHT = 700
    MAX_PLAYER_HEIGHT = 250
    MAX_PLAYER_WIDTH = 250
    MIN_PLAYER_HEIGHT = 10
    MIN_PLAYER_WIDTH = 10
    SHRINK_KEY = pygame.K_DOWN
    SIZE_INTERVAL = 2
    TITLE = "Ludum Dare 34"
    WIDTH = 600


class Resources:
    @staticmethod
    def load_image(name, size=None):
        image = pygame.image.load(os.path.join("images", name)).convert()
        if size is not None:
            image = pygame.transform.scale(image, size).convert()
        return image
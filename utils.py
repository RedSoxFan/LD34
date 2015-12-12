#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import pygame


class Arithmetic:
    @staticmethod
    def lerp(val1, val2, percent):
        return round(val1 + (val2 - val1) * percent)


class Constants:
    FPS = 60
    GRAVITY = 9.8
    HEIGHT = 600
    TITLE = "Ludum Dare 34"
    WIDTH = 600


class Resources:
    @staticmethod
    def load_image(name, size=None):
        image = pygame.image.load(os.path.join("images", name)).convert()
        if size is not None:
            image = pygame.transform.scale(image, size).convert()
        return image
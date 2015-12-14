#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import pygame


class Arithmetic:
    @staticmethod
    def lerp(val1, val2, percent):
        return round(val1 + (val2 - val1) * percent)

    @staticmethod
    def lerpf(val1, val2, percent):
        return val1 + (val2 - val1) * percent

    @staticmethod
    def clamp(vmin, vmax, val):
        return min(vmax, max(val, vmin))


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


class Graphics:
    @staticmethod
    def hue_shift(color, hueShift):
        col = color if isinstance(color, pygame.color.Color) else pygame.color.Color(color)
        col.hsva = ((col.hsva[0] + hueShift) % 360, min(col.hsva[1], 100), min(col.hsva[2], 100), min(col.hsva[3], 255))
        return col


class Resources:
    @staticmethod
    def load_image(name, size=None):
        image = pygame.image.load(os.path.join("resources", name)).convert_alpha()
        if size is not None:
            image = pygame.transform.scale(image, size).convert_alpha()
        return image

    @staticmethod
    def load_colorized_image(name, hueShift, size=None):
        image = Resources.load_image(name, size=size)

        try:
            from pygame import PixelArray
            pxls = pygame.PixelArray(image)
            for x, y in ((x, y) for x in xrange(image.get_width()) for y in xrange(image.get_height())):
                pxls[x, y] = Graphics.hue_shift(image.unmap_rgb(pxls[x, y]), hueShift)
        except ImportError:
            col = pygame.color.Color(0)
            col.hsva = (hueShift, 50, 50, 255)
            image.fill(col, None, pygame.BLEND_RGBA_ADD)

        return image

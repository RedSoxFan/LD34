#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pygame


class Message(object):
    def __init__(self, msg, xloc, yloc, msgstate="neutral"):
        self.message = msg
        self.x = xloc
        self.y = yloc
        self._lasth = 0
        self.state = msgstate if msgstate in ("good", "bad", "neutral") else "neutral"

    @property
    def alive(self):
        return (self.y + self._lasth) > 0

    def tick(self, surface, delta, fontmap, colormap):
        yoff = 0
        for i, line in enumerate(self.message.split("\n")):
            mtype = ("msgtitle", "msgtitle") if i == 0 else ("msgbody", "msg%s" % self.state)
            (w, h) = fontmap[mtype[0]].size(line)
            surface.blit(fontmap[mtype[0]].render(line, True, colormap[mtype[1]]),
                         (self.x - w // 2, int(self.y) + yoff))
            yoff += h + 5
        self._lasth = yoff
        self.y -= delta / 20.0
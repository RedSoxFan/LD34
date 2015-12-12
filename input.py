import pygame


class Mouse:
    pos = (0, 0)
    oldstate = (0, 0, 0)
    state = (0, 0, 0)

    @staticmethod
    def update():
        Mouse.oldstate = Mouse.state
        Mouse.state = pygame.mouse.get_pressed()
        Mouse.pos = pygame.mouse.get_pos()

    @staticmethod
    def getX():
        return Mouse.pos[0]

    @staticmethod
    def getY():
        return Mouse.pos[1]

    @staticmethod
    def left():
        Mouse.update()
        return Mouse.state[0] == 1

    @staticmethod
    def middle():
        Mouse.update()
        return Mouse.state[1] == 1

    @staticmethod
    def right():
        Mouse.update()
        return Mouse.state[2] == 1

    @staticmethod
    def pressed(ind):
        Mouse.update()
        return Mouse.oldstate[ind] == 0 and Mouse.state[ind] == 1

    @staticmethod
    def released(ind):
        Mouse.update()
        return Mouse.oldstate[ind] == 1 and Mouse.state[ind] == 0

    @staticmethod
    def leftPressed():
        return Mouse.pressed(0)

    @staticmethod
    def leftReleased():
        return Mouse.released(0)

    @staticmethod
    def middlePressed():
        return Mouse.pressed(1)

    @staticmethod
    def middleReleased():
        return Mouse.released(1)

    @staticmethod
    def rightPressed():
        return Mouse.pressed(2)

    @staticmethod
    def rightReleased():
        return Mouse.released(2)


class Keyboard:
    oldkeys = [False for i in range(256)]
    keys = oldkeys

    @staticmethod
    def update():
        Keyboard.oldkeys = Keyboard.keys
        Keyboard.keys = pygame.key.get_pressed()

    @staticmethod
    def down(k, kmap=None):
        Keyboard.update()
        if kmap is None:
            kmap = Keyboard.keys
        return kmap[k if type(k) is int else ord(k)]

    @staticmethod
    def up(k, kmap=None):
        if kmap is None:
            kmap = Keyboard.keys
        return not Keyboard.down(k, kmap)

    @staticmethod
    def pressed(k):
        return not Keyboard.down(k, Keyboard.oldkeys) and Keyboard.down(k)

    @staticmethod
    def released(k):
        return not Keyboard.up(k, Keyboard.oldkeys) and Keyboard.up(k)

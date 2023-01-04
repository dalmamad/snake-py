import sys
from screen import screen, pygame
from setting import *

font = pygame.font.SysFont('Hack', 32)


def key_act(key):
    if key == ENTER_KEY:
        Pause.select()
    if key == DOWN_ARROW or key == S_KEY:
        Pause.change_select(DOWN)
    if key == UP_ARROW or key == W_KEY:
        Pause.change_select(UP)


class Pause:
    pause = True
    selector = 0
    end = RESUME
    options = []
    frcolor = PAUSE_FRCOLOR
    frlen = PAUSE_FRLEN
    frpos = PAUSE_FRPOS

    def __init__(self, index, text, bgcolor, select_color, txtcolor, bglen, bgpos, bggap):
        self.index = index
        self.text = text
        self.bgcolor = bgcolor
        self.txtcolor = txtcolor
        self.bglen = bglen
        self.bgpos = bgpos
        self.bggap = bggap
        self.select_color = select_color

    def draw(self):
        bgcolor = self.bgcolor
        if self.index == self.__class__.selector:
            bgcolor = self.select_color
        pygame.draw.rect(screen, bgcolor, pygame.Rect(
            self.bgpos[0], self.bgpos[1] + self.index*(self.bglen[1]+self.bggap), self.bglen[0], self.bglen[1]))

    def txtdraw(self):
        txt = font.render(self.text, True, self.txtcolor)
        txt_width = txt.get_width()
        txt_height = txt.get_height()
        screen.blit(txt, (self.bgpos[0]+(self.bglen[0]-txt_width)/2, self.bgpos[1] +
                    self.index*(self.bglen[1]+self.bggap)+(self.bglen[1]-txt_height)/2))

    @classmethod
    def draw_frame(cls):
        pygame.draw.rect(screen, cls.frcolor, pygame.Rect(
            cls.frpos[0], cls.frpos[1], cls.frlen[0], cls.frlen[1]))

    @classmethod
    def change_select(cls, dir):
        cls.options[cls.selector].selected = False
        if dir == DOWN:
            if cls.selector == len(cls.options) - 1:
                cls.selector = 0
            else:
                cls.selector += 1
        if dir == UP:
            if cls.selector == 0:
                cls.selector = len(cls.options) - 1
            else:
                cls.selector -= 1
        cls.options[cls.selector].selected = True

    @classmethod
    def select(cls):
        cls.pause = False
        if cls.selector == 0:  # resume
            cls.end = RESUME
        if cls.selector == 1:  # menu
            cls.end = MENU


Pause.options.append(Pause(0, 'Resume', PAUSE_OPCOLOR, PAUSE_SELECT_COLOR,
                     PAUSE_TXTCOLOR, PAUSE_OPLEN, PAUSE_OPPOS, PAUSE_OPGAP))
Pause.options.append(Pause(1, 'menu', PAUSE_OPCOLOR, PAUSE_SELECT_COLOR,
                     PAUSE_TXTCOLOR, PAUSE_OPLEN, PAUSE_OPPOS, PAUSE_OPGAP))


def pause_game():

    Pause.pause = True
    Pause.selector = 0
    Pause.draw_frame()

    while Pause.pause:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                key_act(event.key)

        for option in Pause.options:
            option.draw()
            option.txtdraw()

        pygame.display.update()
    return Pause.end

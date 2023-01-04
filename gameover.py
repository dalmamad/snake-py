import sys
from screen import screen, pygame
from setting import *

font = pygame.font.Font(FONT, FONT_SIZE_PAUSE)


def key_act(key):
    if key == ENTER_KEY:
        Gameover.select()
    if key == DOWN_ARROW or key == S_KEY:
        Gameover.change_select(DOWN)
    if key == UP_ARROW or key == W_KEY:
        Gameover.change_select(UP)


class Gameover:
    menu = True
    selector = 0
    end = RESUME
    options = []
    frcolor = GO_FRCOLOR
    txtcolor = GO_TXTCOLOR
    frlen = GO_FRLEN
    frpos = GO_FRPOS
    game_info = {}

    def __init__(
        self, index, text, bgcolor, select_color, txtcolor, bglen, bgpos, bggap
    ):
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
        pygame.draw.rect(
            screen,
            bgcolor,
            pygame.Rect(
                self.bgpos[0],
                self.bgpos[1] + self.index * (self.bglen[1] + self.bggap),
                self.bglen[0],
                self.bglen[1],
            ),
        )

    def txtdraw(self):
        txt = font.render(self.text, True, self.txtcolor)
        txt_width = txt.get_width()
        txt_height = txt.get_height()
        screen.blit(
            txt,
            (
                self.bgpos[0] + (self.bglen[0] - txt_width) / 2,
                self.bgpos[1]
                + self.index * (self.bglen[1] + self.bggap)
                + (self.bglen[1] - txt_height) / 2,
            ),
        )

    @classmethod
    def draw_frame(cls):
        pygame.draw.rect(
            screen,
            cls.frcolor,
            pygame.Rect(cls.frpos[0], cls.frpos[1], cls.frlen[0], cls.frlen[1]),
        )

    @classmethod
    def draw_txt(cls):
        for index in range(int(cls.game_info["players"])):
            snake_color = cls.game_info["snake" + str(index + 1) + "_color"]
            txt = font.render(
                "Score : " + str(cls.game_info["score_" + str(index + 1)]),
                True,
                snake_color,
            )
            txt_width = txt.get_width()
            txt_height = txt.get_height()
            screen.blit(
                txt,
                (
                    cls.frpos[0] + (cls.frlen[0] - txt_width) / 2,
                    cls.frpos[1] * 1.3 + index * txt_height * 1.3,
                ),
            )
        if (cls.game_info["players"]) > 1 and cls.game_info["winner"] != 0:
            winner_color = cls.game_info[
                "snake" + str(cls.game_info["winner"]) + "_color"
            ]
            # txt = font.render(
            #     "snake" + str(cls.game_info["winner"]) + " won", True, winner_color
            # )
            txt = font.render("ThisColorWon", True, winner_color)
            txt_width = txt.get_width()
            txt_height = txt.get_height()
            screen.blit(
                txt,
                (
                    cls.frpos[0] + (cls.frlen[0] - txt_width) / 2,
                    cls.frpos[1] * 1.3
                    + int(cls.game_info["players"]) * txt_height * 1.5,
                ),
            )

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
        cls.menu = False
        if cls.selector == 0:  # play-again
            cls.end = PLAY_AGAIN
        if cls.selector == 1:  # menu
            cls.end = MENU


Gameover.options.append(
    Gameover(
        0,
        "PlayAgain",
        GO_OPCOLOR,
        GO_SELECT_COLOR,
        GO_TXTCOLOR,
        GO_OPLEN,
        GO_OPPOS,
        GO_OPGAP,
    )
)
Gameover.options.append(
    Gameover(
        1,
        "Menu",
        GO_OPCOLOR,
        GO_SELECT_COLOR,
        GO_TXTCOLOR,
        GO_OPLEN,
        GO_OPPOS,
        GO_OPGAP,
    )
)


def game_over(game_info):
    Gameover.game_info = game_info
    Gameover.menu = True
    screen.fill(MENU_BGCOLOR)
    # Gameover.draw_frame()
    Gameover.selector = 0
    Gameover.draw_txt()

    while Gameover.menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                key_act(event.key)
        for option in Gameover.options:
            option.draw()
            option.txtdraw()
        pygame.display.update()
    return Gameover.end

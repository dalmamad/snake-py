import sys
from screen import screen, pygame
from setting import *
from game import the_game

screen.fill(MENU_BGCOLOR)
font = pygame.font.SysFont("Hack", 32)
text = font.render("PRESS ENTER", True, TEXT_COLOR)
screen.blit(text, (20, 20))
pygame.display.update()


def key_act(key):
    if key == ENTER_KEY:
        Option.select()
    if key == DOWN_ARROW or key == S_KEY:
        Option.change_select(DOWN)
    if key == UP_ARROW or key == W_KEY:
        Option.change_select(UP)


class Option:
    selector = 0
    options = []
    txtcolor = TEXT_COLOR

    def __init__(
        self, index, text, bgcolor, select_color, txtcolor, players, bglen, bgpos, bggap
    ):
        self.index = index
        self.text = text
        self.bgcolor = bgcolor
        self.txtcolor = txtcolor
        self.players = players
        self.bglen = bglen
        self.bgpos = bgpos
        self.bggap = bggap
        self.select_color = select_color

    def bgdraw(self):
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
    def draw_txt(cls):
        keys = ["w,a,s,d", "arrows"]
        lines = [
            "in 2 player the loser is a snake",
            "that collides with itself or another snake",
        ]
        for index in range(2):
            txt = font.render(
                "snake" + str(index + 1) + " keys : " + keys[index], True, cls.txtcolor
            )
            txt_width = txt.get_width()
            txt_height = txt.get_height()
            screen.blit(
                txt,
                (
                    (WIN_WIDTH - txt_width) / 2,
                    0.2 * WIN_HEIGHT + index * txt_height * 1.3,
                ),
            )
        for index in range(len(lines)):
            txt = font.render(lines[index], True, cls.txtcolor)
            txt_width = txt.get_width()
            txt_height = txt.get_height()
            screen.blit(
                txt,
                (
                    (WIN_WIDTH - txt_width) / 2,
                    0.2 * WIN_HEIGHT + 2 * txt_height * 1.5 + index * txt_height * 1.3,
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
        if cls.selector == 2:
            sys.exit()
        else:
            players = cls.options[cls.selector].players
            res = the_game(players)
            while res == PLAY_AGAIN:
                res = the_game(players)


Option.options.append(
    Option(
        0,
        "1-player",
        OPTION_BGCOLOR,
        OPTION_SELECT_COLOR,
        OPTION_TXTCOLOR,
        1,
        OPTION_BGLEN,
        OPTION_BGPOS,
        OPTION_BGGAP,
    )
)
Option.options.append(
    Option(
        1,
        "2-player",
        OPTION_BGCOLOR,
        OPTION_SELECT_COLOR,
        OPTION_TXTCOLOR,
        2,
        OPTION_BGLEN,
        OPTION_BGPOS,
        OPTION_BGGAP,
    )
)
Option.options.append(
    Option(
        2,
        "exit",
        OPTION_BGCOLOR,
        OPTION_SELECT_COLOR,
        OPTION_TXTCOLOR,
        0,
        OPTION_BGLEN,
        OPTION_BGPOS,
        OPTION_BGGAP,
    )
)


def main():
    on_menu = True
    while on_menu:
        screen.fill(MENU_BGCOLOR)
        Option.draw_txt()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                key_act(event.key)
        for option in Option.options:
            option.bgdraw()
            option.txtdraw()
        pygame.display.update()


if __name__ == "__main__":
    main()

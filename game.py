import sys
import random
from setting import *
from screen import screen, pygame
from pause import pause_game
from gameover import game_over


clock = pygame.time.Clock()
PLAY = True
RETURN = 0
GRID = {}


def ADD_GRID(x, y, snake_index):
    if str(x) + ":" + str(y) not in GRID:
        GRID[str(x) + ":" + str(y)] = EMPTY
    if GRID[str(x) + ":" + str(y)] != EMPTY:
        if GRID[str(x) + ":" + str(y)] == str(snake_index):
            GRID[str(x) + ":" + str(y)] = SELF_OVERLAP
        else:
            GRID[str(x) + ":" + str(y)] = OVERLAP
    else:
        GRID[str(x) + ":" + str(y)] = str(snake_index)


def REMOVE_GRID(x, y):
    GRID[str(x) + ":" + str(y)] = EMPTY


def GET_GRID(x, y):
    return GRID[str(x) + ":" + str(y)]


def CLEAN_GRID():
    for i in range(GRID_COUNT):
        for j in range(GRID_COUNT):
            GRID[str(i) + ":" + str(j)] = EMPTY


class Snake:
    snakes = []
    snakes_count = 0

    def __init__(self, color, init_len, init_dir, init_grid, counter, keys, index):
        self.init_grid = init_grid
        self.parts = []
        self.color = color
        self.keys = keys
        self.len = init_len
        self.turn_to = init_dir
        self.dir = init_dir
        self.tail_dir = init_dir
        self.max_counter = counter
        self.counter = 0
        self.screen_exit = False
        self.eat = False
        self.eat_index = 0
        self.index = index
        self.score = 0
        self.init_draw = True
        self.add_init_parts()

    def add_init_parts(self):
        dx = 0
        dy = 0

        if self.dir == UP:
            dy = 1
        if self.dir == DOWN:
            dy = -1
        if self.dir == LEFT:
            dx = 1
        if self.dir == RIGHT:
            dx = -1
        for index in range(0, self.len):
            x = self.init_grid[0] + index * dx
            y = self.init_grid[1] + index * dy
            ADD_GRID(x, y, self.index)
            self.parts.append((x, y))

    def turn(self, key):
        if key == self.keys[LEFT] and self.dir != RIGHT:
            self.turn_to = LEFT
        if key == self.keys[RIGHT] and self.dir != LEFT:
            self.turn_to = RIGHT
        if key == self.keys[UP] and self.dir != DOWN:
            self.turn_to = UP
        if key == self.keys[DOWN] and self.dir != UP:
            self.turn_to = DOWN

    def move(self):
        dy = 0
        dx = 0
        if self.dir == UP:
            dy = -1
        if self.dir == DOWN:
            dy = 1
        if self.dir == LEFT:
            dx = -1
        if self.dir == RIGHT:
            dx = 1
        tailx = self.parts[len(self.parts) - 1][0]
        taily = self.parts[len(self.parts) - 1][1]
        REMOVE_GRID(tailx, taily)
        self.parts.pop()
        self.screen_exit = self.check_screen_exit(dx, dy)
        if self.screen_exit == False:
            ADD_GRID(self.parts[0][0] + dx, self.parts[0][1] + dy, self.index)
            self.parts.insert(0, (self.parts[0][0] + dx, self.parts[0][1] + dy))

    def check_screen_exit(self, dx, dy):
        head = self.parts[0]
        if head[0] + dx == GRID_COUNT:
            ADD_GRID(0, self.parts[0][1], self.index)
            self.parts.insert(0, (0, self.parts[0][1]))
            return True
        if head[0] + dx == -1:
            ADD_GRID(GRID_COUNT - 1, self.parts[0][1], self.index)
            self.parts.insert(0, (GRID_COUNT - 1, self.parts[0][1]))
            return True
        if head[1] + dy == GRID_COUNT:
            ADD_GRID(self.parts[0][0], 0, self.index)
            self.parts.insert(0, (self.parts[0][0], 0))
            return True
        if head[1] + dy == -1:
            ADD_GRID(self.parts[0][0], GRID_COUNT - 1, self.index)
            self.parts.insert(0, (self.parts[0][0], GRID_COUNT - 1))
            return True
        return False

    def check_eat(self, foods):
        for food in foods:
            if food.pos[0] == self.parts[0][0] and food.pos[1] == self.parts[0][1]:
                self.eat = True
                self.len += 1
                self.score += 1
                food.eated = True
                last_index = len(self.parts) - 1
                last_part = self.parts[last_index]

                if self.tail_dir == LEFT:
                    self.parts.append((last_part[0] + 1, last_part[1]))
                if self.tail_dir == RIGHT:
                    self.parts.append((last_part[0] - 1, last_part[1]))
                if self.tail_dir == UP:
                    self.parts.append((last_part[0], last_part[1] + 1))
                if self.tail_dir == DOWN:
                    self.parts.append((last_part[0], last_part[1] - 1))

    def update_tail_dir(self):
        last_index = len(self.parts) - 1
        last_part = self.parts[last_index]
        nextto_last = self.parts[last_index - 1]
        dx = last_part[0] - nextto_last[0]
        dy = last_part[1] - nextto_last[1]
        if dx == 1 or dx == -(GRID_COUNT - 1):
            self.tail_dir = LEFT
        if dx == -1 or dx == (GRID_COUNT - 1):
            self.tail_dir = RIGHT
        if dy == 1 or dy == -(GRID_COUNT - 1):
            self.tail_dir = UP
        if dy == -1 or dy == (GRID_COUNT - 1):
            self.tail_dir = DOWN

    def check_collision(self):
        global PLAY
        global RETURN
        head = self.parts[0]
        target_grid = GET_GRID(head[0], head[1])

        if target_grid == SELF_OVERLAP or target_grid == OVERLAP:

            game_info = {
                "players": self.__class__.snakes_count,
            }
            for index in range(self.__class__.snakes_count):
                game_info["score_" + str(index + 1)] = self.__class__.snakes[
                    index
                ].score
                game_info["snake" + str(index + 1) + "_color"] = self.__class__.snakes[
                    index
                ].color
                if index != self.index:
                    game_info["winner"] = index + 1
            if target_grid == OVERLAP:

                for index, snake in enumerate(Snake.snakes):
                    if (
                        index != self.index
                        and head[0] == snake.parts[0][0]
                        and head[1] == snake.parts[0][1]
                    ):
                        print("hed")
                        if self.score > snake.score:
                            game_info["winner"] = self.index + 1
                        elif self.score < snake.score:
                            game_info["winner"] = snake.index + 1
                        else:
                            game_info["winner"] = 0

            RETURN = game_over(game_info)
            PLAY = False

    def mid_part_draw(self):
        last_index = len(self.parts) - 1
        for index, part in enumerate(self.parts):
            if index != last_index and index != 0:
                pygame.draw.rect(
                    screen,
                    self.color,
                    pygame.Rect(
                        part[0] * GRID_SIZE, part[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE
                    ),
                )

    def smooth_draw(self):
        layer = self.counter / self.max_counter * GRID_SIZE
        last_index = len(self.parts) - 1
        head = self.parts[0]
        tail = self.parts[last_index]

        if self.init_draw:
            self.init_draw = False
            self.mid_part_draw()

        if self.eat == False:
            pygame.draw.rect(
                screen,
                GAME_BGCOLOR,
                pygame.Rect(
                    tail[0] * GRID_SIZE, tail[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE
                ),
            )
            if self.tail_dir == UP:
                pygame.draw.rect(
                    screen,
                    self.color,
                    pygame.Rect(
                        tail[0] * GRID_SIZE,
                        tail[1] * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE - layer,
                    ),
                )
            if self.tail_dir == DOWN:
                pygame.draw.rect(
                    screen,
                    self.color,
                    pygame.Rect(
                        tail[0] * GRID_SIZE,
                        tail[1] * GRID_SIZE + layer,
                        GRID_SIZE,
                        GRID_SIZE,
                    ),
                )
            if self.tail_dir == LEFT:
                pygame.draw.rect(
                    screen,
                    self.color,
                    pygame.Rect(
                        tail[0] * GRID_SIZE,
                        tail[1] * GRID_SIZE,
                        GRID_SIZE - layer,
                        GRID_SIZE,
                    ),
                )
            if self.tail_dir == RIGHT:
                pygame.draw.rect(
                    screen,
                    self.color,
                    pygame.Rect(
                        tail[0] * GRID_SIZE + layer,
                        tail[1] * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE,
                    ),
                )

        if self.dir == UP:
            pygame.draw.rect(
                screen,
                self.color,
                pygame.Rect(
                    head[0] * GRID_SIZE,
                    (head[1] + 1) * GRID_SIZE - layer,
                    GRID_SIZE,
                    layer * 1.5,
                ),
            )
        if self.dir == DOWN:
            pygame.draw.rect(
                screen,
                self.color,
                pygame.Rect(head[0] * GRID_SIZE, head[1] * GRID_SIZE, GRID_SIZE, layer),
            )
        if self.dir == LEFT:
            pygame.draw.rect(
                screen,
                self.color,
                pygame.Rect(
                    (head[0] + 1) * GRID_SIZE - layer,
                    head[1] * GRID_SIZE,
                    layer * 1.5,
                    GRID_SIZE,
                ),
            )
        if self.dir == RIGHT:
            pygame.draw.rect(
                screen,
                self.color,
                pygame.Rect(head[0] * GRID_SIZE, head[1] * GRID_SIZE, layer, GRID_SIZE),
            )


class Food:
    def __init__(self, color, snakes):
        self.color = color
        self.pos = (0, 0)
        self.create(snakes)
        self.eated = False

    def create(self, snakes):
        index = 0
        xrandom = random.randrange(0, GRID_COUNT)
        yrandom = random.randrange(0, GRID_COUNT)
        while index != len(snakes):
            broke = False
            for part in snakes[index].parts:
                if part[0] == xrandom and part[1] == yrandom:
                    xrandom = random.randrange(0, GRID_COUNT)
                    yrandom = random.randrange(0, GRID_COUNT)
                    broke = True
                    index = 0
                    break
            if broke == False:
                index += 1
        self.pos = (xrandom, yrandom)

    def check_eated(self, snakes):
        if self.eated:
            self.eated = False
            self.create(snakes)

    def draw(self):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(
                self.pos[0] * GRID_SIZE, self.pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE
            ),
        )


def the_game(players):
    screen.fill(GAME_BGCOLOR)
    global PLAYERS
    global PLAY
    global RETURN
    PLAY = True
    RETURN = 0
    CLEAN_GRID()
    Snake.snakes_count = int(players)
    Snake.snakes = []
    foods = []
    for index in range(players):
        Snake.snakes.append(
            Snake(
                SNAKES_COLOR[index],
                SNAKES_INIT_LEN[index],
                SNAKES_INIT_DIR[index],
                SNAKES_INIT_GRID[index],
                SNAKES_MAX_COUNTER[index],
                SNAKES_KEYS[index],
                index,
            )
        )
        foods.append(Food(FOOD_COLOR, Snake.snakes))

    while PLAY:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == ESC_KEY:
                    res = pause_game()
                    screen.fill(GAME_BGCOLOR)
                    for snake in Snake.snakes:
                        snake.init_draw = True
                    if res == MENU:
                        PLAY = False
                for snake in Snake.snakes:
                    snake.turn(event.key)

        for snake in Snake.snakes:
            if snake.counter == snake.max_counter + 1:
                snake.counter = 0
                snake.eat = False
                snake.dir = snake.turn_to
                snake.move()
                snake.check_collision()
                snake.check_eat(foods)
                snake.update_tail_dir()
            snake.smooth_draw()
            snake.counter += 1

        for food in foods:
            food.check_eated(Snake.snakes)
            if RETURN == 0:
                food.draw()

        pygame.display.flip()

    return RETURN

import pygame
import random


colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


# Game class
class Tetris:
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figure = None
        self.next_figure = None
        self.paused = False

        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = self.next_figure if self.next_figure else Figure(3, 0)
        self.next_figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection


    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += (lines + 1) ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


pygame.init()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (600, 600)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")



def show_start_screen():
    font = pygame.font.SysFont('Transformers Movie', 50, True, False)
    text_title = font.render("TETRIS", True, (0, 0, 0))
    text_start = font.render("Click to Start", True, (0, 0, 0))

    screen.fill(WHITE)
    screen.blit(text_title, (200, 150))
    screen.blit(text_start, (150, 250))

    pygame.display.flip()



def show_pause_screen():
    font = pygame.font.SysFont('Transformers Movie', 50, True, False)
    text_pause = font.render("PAUSED", True, (0, 0, 0))

    screen.fill(WHITE)
    screen.blit(text_pause, (230, 250))

    pygame.display.flip()



def draw_next_figure():
    if game.next_figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.next_figure.image():
                    pygame.draw.rect(screen, colors[game.next_figure.color],
                                     [450 + j * game.zoom, 150 + i * game.zoom, game.zoom - 2, game.zoom - 2])



done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0

pressing_down = False
game_started = False

while not done:
    if not game_started:
        show_start_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started:
                game_started = True
                game.state = "start"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)
            if event.key == pygame.K_p:
                game.paused = not game.paused

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    if not game.paused:
        if game_started:
            if game.figure is None:
                game.new_figure()
            counter += 1
            if counter > 100000:
                counter = 0

            if counter % (fps // game.level // 2) == 0 or pressing_down:
                if game.state == "start":
                    game.go_down()

            screen.fill(WHITE)

            for i in range(game.height):
                for j in range(game.width):
                    pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                    if game.field[i][j] > 0:
                        pygame.draw.rect(screen, colors[game.field[i][j]],
                                         [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

            if game.figure is not None:
                for i in range(4):
                    for j in range(4):
                        p = i * 4 + j
                        if p in game.figure.image():
                            pygame.draw.rect(screen, colors[game.figure.color],
                                             [game.x + game.zoom * (j + game.figure.x) + 1,
                                              game.y + game.zoom * (i + game.figure.y) + 1,
                                              game.zoom - 2, game.zoom - 2])

            font = pygame.font.SysFont('Transformers Movie', 25, True, False)
            font1 = pygame.font.SysFont('Transformers Movie', 50, True, False)
            text = font.render("Score: " + str(game.score), True, BLACK)
            text_next = font1.render("next:", True, (0, 0, 0))
            screen.blit(text_next, [320, 155])
            text_game_over = font1.render("Game Over", True, (0, 0, 0))
            text_game_over1 = font1.render("Press ESC", True, (0, 0, 0))

            screen.blit(text, [0, 0])
            if game.state == "gameover":
                screen.blit(text_game_over, [320, 300])
                screen.blit(text_game_over1, [320, 365])

            draw_next_figure()

            pygame.display.flip()

    else:
        show_pause_screen()

    clock.tick(fps)

pygame.quit()
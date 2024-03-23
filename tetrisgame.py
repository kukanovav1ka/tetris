#!/usr/bin/python3

import pygame
import pygame_menu
import logging
import numpy as np
import random

SCREEN_COLOR = (255, 0, 255)
WHITE = (255, 255, 255)
HEAD_COLOR = (204, 0, 204)
PINK = (255, 204, 229)
RED = (255, 105, 122)
BLUE = (87, 220, 220)
YELLOW = (255, 255, 51)
GREEN = (153, 255, 51)
ORANGE = (255, 153, 51)
PURPLE = (178, 102, 255)
SIZE_BLOCK = 20
COUNT_COLUMNS = 21
COUNT_ROWS = 30
HEAD_MARGIN = 80
MAP = {1: [[-1, 0], [0, -1], [0, 0], [0, 1]],
       2: [[-1, 0], [0, 0], [1, 0], [2, 0]],
       3: [[-1, 0], [0, 0], [0, 1], [1, 1]],
       4: [[-1, 0], [0, -1], [0, 0], [1, -1]],
       5: [[0, 0], [0, 1], [1, 0], [1, 1]],
       6: [[0, 0], [0, 1], [1, 0], [2, 0]],
       7: [[0, -1], [0, 0], [1, 0], [2, 0]],
       }
COLOR_BLOCKS = [BLUE, RED, YELLOW, GREEN, ORANGE, PURPLE]
logging.basicConfig(level=logging.DEBUG)

pygame.init()

bg_image = pygame.image.load("bg.jpg")

size = [SIZE_BLOCK * COUNT_COLUMNS + 2 * SIZE_BLOCK,
        SIZE_BLOCK * COUNT_ROWS + 2 * SIZE_BLOCK + HEAD_MARGIN]

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tetris game')
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 36)


class Arena:
    def __init__(self, m, n):
        self.arena = [[0] * n for _ in range(m)]

    def add_block(self, block):
        count = 100
        mul = 1
        for i in block.get_cells():
            self.arena[i[0]][i[1]] = 1
        for i in range(len(self.arena)):
            if self.clear_line(i):
                count += 1000 * mul
                mul += 1
        return count

    def are_collisions(self, block, direction):
        for i in block.get_cells():
            if i[1] + direction[1] >= 21 or i[1] + direction[1] < 0:
                logging.info("Collision")
                return True
            if i[0] + direction[0] >= 30 or self.arena[i[0] + direction[0]][i[1] + direction[1]] == 1:
                logging.info("Collision")
                return True
        return False

    def draw_arena(self):
        for row in range(0, len(self.arena)):
            for column in range(0, len(self.arena[0])):
                if self.arena[row][column] == 1:
                    color = RED
                    draw_block(color, row, column, True)
                elif (row + column) % 2 == 0:
                    color = PINK
                    draw_block(color, row, column, False)
                else:
                    color = WHITE
                    draw_block(color, row, column, False)

    def clear_line(self, num):
        for i in range(len(self.arena[0])):
            if self.arena[num][i] == 0:
                return False
        self.arena.pop(num)
        self.arena.insert(0, [0] * len(self.arena[0]))
        return True


class Block:
    def __init__(self, block, color):
        self.block = block.copy()
        self.color = color
        self.x = 1
        self.y = 10

    def get_cells(self):
        return [[self.x + self.block[column][0], self.y + self.block[column][1]]
                for column in range(0, 4)]

    def draw_blocks(self, color):
        for i in range(0, 4):
            draw_block(color, self.get_cells()[
                       i][0], self.get_cells()[i][1], True)

    def rotate_block(self):
        a = np.array([[0, 1], [-1, 0]])
        for i in range(4):
            b = np.array([self.block[i][0], self.block[i][1]])
            self.block[i][0] = np.matmul(a, b)[0]
            self.block[i][1] = np.matmul(a, b)[1]


def draw_block(color, row, column, line):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK,
                                     HEAD_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK,
                                     SIZE_BLOCK,
                                     SIZE_BLOCK])
    if line == True:
        pygame.draw.rect(screen, (0, 0, 0), [SIZE_BLOCK + column * SIZE_BLOCK,
                                             HEAD_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK,
                                             SIZE_BLOCK,
                                             SIZE_BLOCK], 1)


def game_over():
    main_theme1 = pygame_menu.themes.THEME_DARK.copy()
    main_theme1.set_background_color_opacity(0.3)

    exit_menu = False

    def close_menu():
        nonlocal exit_menu
        exit_menu = True

    menu = pygame_menu.Menu('', 250, 300, theme=main_theme1)

    menu.add.button('Выход в меню', close_menu)
    while not exit_menu:

        screen.blit(bg_image, (0, 0))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)

        pygame.display.update()


def start_the_game():
    arena = Arena(COUNT_ROWS, COUNT_COLUMNS)
    num = random.randint(1, 7)
    my_block = Block(MAP[num], (255, 255, 255))
    num = random.randint(1, 7)
    next_block = Block(MAP[num], (255, 255, 255))
    next_block.x = -4
    next_block.y = 17
    num = random.randint(1, 7)
    elapsed_time = 0.0
    total = 0
    direction = [0, 0]
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    direction[1] = 1
                    # my_block.y += 1
                if event.key == pygame.K_LEFT:
                    direction[1] = -1
                    # my_block.y -= 1
                if event.key == pygame.K_SPACE and not arena.are_collisions(my_block, [0, 1]) and not arena.are_collisions(my_block, [0, -1]):
                    my_block.rotate_block()
                if event.key == pygame.K_DOWN:
                    direction[0] = 1
                    # my_block.x += 1
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    direction[1] = 0
                elif event.key == pygame.K_DOWN:
                    direction[0] = 0

        if not arena.are_collisions(my_block, direction):
            my_block.y += direction[1]
            my_block.x += direction[0]
        elif not arena.are_collisions(my_block, [direction[0], 0]):
            my_block.x += direction[0]
        elif not arena.are_collisions(my_block, [0, direction[1]]):
            my_block.y += direction[1]

        screen.fill(SCREEN_COLOR)
        pygame.draw.rect(screen, HEAD_COLOR, [0, 0, size[0], HEAD_MARGIN])
        text_total = courier.render(
            f'Total: {total}', 0, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))

        arena.draw_arena()

        next_block.draw_blocks(BLUE)
        my_block.draw_blocks(BLUE)

        pygame.display.flip()
        elapsed_time += timer.tick(10)
        logging.info(f"Time {elapsed_time}")
        if elapsed_time > 500:
            elapsed_time = 0.0
            if not arena.are_collisions(my_block, [1, 0]):
                my_block.x += 1
            else:
                total += arena.add_block(my_block)
                my_block = Block(MAP[num], (255, 255, 255))
                if arena.are_collisions(my_block, [0, 0]):
                    print("GAME OVER...")
                    game_over()
                    break
                num = random.randint(1, 7)
                next_block.block = MAP[num]
                logging.info(f"Num {num}")


main_theme = pygame_menu.themes.THEME_DARK.copy()
main_theme.set_background_color_opacity(0.3)

# менюшка
menu = pygame_menu.Menu('', 250, 300,
                        theme=main_theme)

menu.add.text_input('Игрок: ', default='Игрок 1')
menu.add.button('Играть', start_the_game)
menu.add.button('Выход', pygame_menu.events.EXIT)

while True:

    screen.blit(bg_image, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()


# def main(argv):


# if __name__ == "__main__":
#    main(sys.argv)

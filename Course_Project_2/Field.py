import pygame
import random

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (114, 114, 114)
dark_grey = (72, 72, 72)
# predicted_walls = [[[21, 41], [103, 123], [162, 182], [261], [323, 343, 363]]]
# block_is_choosen = False
cannot_place_apple = [3]
sectors_walls = [[40, 41, 42],
                 [102, 122],
                 [161, 181],
                 [280, 281],
                 [342],
                 [364, 365],
                 [284, 264],
                 [166, 167],
                 [107],
                 [110, 130, 150],
                 [210, 211],
                 [269, 289],
                 [368, 388],
                 [393, 394, 395],
                 [356, 336],
                 [297],
                 [294, 293],
                 [214, 194, 174],
                 [177, 178],
                 [116],
                 [94, 93],
                 [36, 37],
                 [10, 30],
                 [45, 46]]
sectors_entrance_exit = [[3, 80],
                         [80, 160],
                         [160, 240],
                         [240, 320],
                         [320, 384],
                         [384, 304],
                         [304, 224],
                         [224, 144],
                         [144, 88],
                         [88, 171],
                         [171, 251],
                         [251, 331],
                         [331, 392],
                         [392, 376],
                         [376, 319],
                         [319, 255],
                         [255, 232],
                         [232, 176],
                         [176, 159],
                         [159, 95],
                         [95, 72],
                         [72, 11],
                         [11, 7],
                         [7, 3]]

def define_sector(block):
    if block <= 79:
        if block % 20 <= 3:
            return 0
        elif block % 20 <= 7:
            return 23
        elif block % 20 <= 11:
            return 22
        else:
            return 21
    elif block <= 159:
        if block % 20 <= 3:
            return 1
        elif block % 20 <= 7:
            return 8
        elif block % 20 <= 11:
            return 9
        elif block % 20 <= 15:
            return 20
        else:
            return 19
    elif block <= 239:
        if block % 20 <= 3:
            return 2
        elif block % 20 <= 7:
            return 7
        elif block % 20 <= 11:
            return 10
        elif block % 20 <= 15:
            return 17
        else:
            return 18
    elif block <= 319:
        if block % 20 <= 3:
            return 3
        elif block % 20 <= 7:
            return 6
        elif block % 20 <= 11:
            return 11
        elif block % 20 <= 15:
            return 16
        else:
            return 15
    else:
        if block % 20 <= 3:
            return 4
        elif block % 20 <= 7:
            return 5
        elif block % 20 <= 11:
            return 12
        elif block % 20 <= 15:
            return 13
        else:
            return 14

class Field:

    def __init__(self, field, block_array):
        self.field = field
        self.block_array = block_array
        self.apple_count = 0
        self.apple = 0
        self.walls = 0
        self.path_to_apple = []
        self.path = []
        self.graph = []
        self.current_block_of_walls = []
        self.sectors_status = ['disactivated' for i in range(24)]
        for i in range(400):
            self.graph.append([])
            if i // 20 != 0:
                if self.field[i // 20][i % 20] == 'empty':
                    self.graph[-1].append(i - 20)
            if i // 20 != 19:
                if self.field[i // 20][i % 20] == 'empty':
                    self.graph[-1].append(i + 20)
            if i % 20 != 19:
                if self.field[i // 20][i % 20] == 'empty':
                    self.graph[-1].append(i + 1)
            if i % 20 != 0:
                if self.field[i // 20][i % 20] == 'empty':
                    self.graph[-1].append(i - 1)

    def reset_graph(self, snake_head):
        self.graph = []
        for i in range(400):
            self.graph.append([])
            if self.field[i % 20][i // 20] == 'empty' or self.field[i % 20][i // 20] == 'apple':
                if i // 20 != 0:
                    if self.field[(i - 20) % 20][(i - 20) // 20] == 'empty' or self.field[(i - 20) % 20][(i - 20) // 20] == 'apple':
                        self.graph[-1].append(i - 20)
                if i // 20 != 19:
                    if self.field[(i + 20) % 20][(i + 20) // 20] == 'empty' or self.field[(i + 20) % 20][(i + 20) // 20] == 'apple':
                        self.graph[-1].append(i + 20)
                if i % 20 != 19:
                    if self.field[(i + 1) % 20][(i + 1) // 20] == 'empty' or self.field[(i + 1) % 20][(i + 1) // 20] == 'apple':
                        self.graph[-1].append(i + 1)
                if i % 20 != 0:
                    if self.field[(i - 1) % 20][(i - 1) // 20] == 'empty' or self.field[(i - 1) % 20][(i - 1) // 20] == 'apple':
                        self.graph[-1].append(i - 1)

        if snake_head // 20 != 0:
            if self.field[(snake_head - 20) % 20][(snake_head - 20) // 20] == 'empty' or self.field[(snake_head - 20) % 20][(snake_head - 20) // 20] == 'apple':
                self.graph[snake_head].append(snake_head - 20)
                self.graph[snake_head - 20].append(snake_head)
        if snake_head // 20 != 19:
            if self.field[(snake_head + 20) % 20][(snake_head + 20) // 20] == 'empty' or self.field[(snake_head + 20) % 20][(snake_head + 20) // 20] == 'apple':
                self.graph[snake_head].append(snake_head + 20)
                self.graph[snake_head + 20].append(snake_head)
        if snake_head % 20 != 19:
            if self.field[(snake_head + 1) % 20][(snake_head + 1) // 20] == 'empty' or self.field[(snake_head + 1) % 20][(snake_head + 1) // 20] == 'apple':
                self.graph[snake_head].append(snake_head + 1)
                self.graph[snake_head + 1].append(snake_head)
        if snake_head % 20 != 0:
            if self.field[(snake_head - 1) % 20][(snake_head - 1) // 20] == 'empty' or self.field[(snake_head - 1) % 20][(snake_head - 1) // 20] == 'apple':
                self.graph[snake_head].append(snake_head - 1)
                self.graph[snake_head - 1].append(snake_head)

    def create_apple(self):
        self.apple_count += 1
        flag = True
        new_block_array = list(range(400))
        while flag:
            random_index = random.randrange(len(new_block_array))
            random_block = new_block_array[random_index]
            if self.sectors_status[define_sector(random_block)] == 'disactivated':
                if self.field[random_block % 20][random_block // 20] == 'empty':
                    if random_block % 20 != 0 and random_block % 20 != 3 and random_block % 20 != 4 and random_block % 20 != 7 and random_block % 20 != 8 and random_block % 20 != 11 and random_block % 20 != 12 and random_block % 20 != 15 and random_block % 20 != 16 and random_block % 20 != 19:
                        if random_block // 20 != 0 and random_block // 20 != 3 and random_block // 20 != 4 and random_block // 20 != 7 and random_block // 20 != 8 and random_block // 20 != 11 and random_block // 20 != 12 and random_block // 20 != 15 and random_block // 20 != 16 and random_block // 20 != 19:
                            self.field[random_block % 20][random_block // 20] = 'apple'
                            self.apple = random_block
                            flag = False
                        else:
                            new_block_array.pop(random_index)
                            if len(new_block_array) == 0:
                                running = False
                    else:
                        new_block_array.pop(random_index)
                        if len(new_block_array) == 0:
                            running = False
                else:
                    new_block_array.pop(random_index)
                    if len(new_block_array) == 0:
                        running = False
            else:
                if self.field[random_block % 20][random_block // 20] == 'empty':
                    self.field[random_block % 20][random_block // 20] = 'apple'
                    self.apple = random_block
                    flag = False
                else:
                    new_block_array.pop(random_index)
                    if len(new_block_array) == 0:
                        running = False

    def create_wall(self, snake_head):
        disactivated_sectors = []
        for i in range(24):
            if self.sectors_status[i] == 'disactivated' and i != define_sector(snake_head):
                disactivated_sectors.append(i)
        if disactivated_sectors != []:
            random_sector_index = random.randrange(len(disactivated_sectors))
            random_sector = disactivated_sectors[random_sector_index]
            self.sectors_status[random_sector] = 'activated'
            for block in sectors_walls[random_sector]:
                self.field[block % 20][block // 20] = 'wall'





    def draw_field(self, screen, game):
        pygame.draw.rect(screen, black, (270, 0, 900, 900))
        if self.apple_count == 0:
            self.create_apple()
        for i in range(20):
            for j in range(20):
                if self.field[i][j] == 'empty':
                    if (i + j) % 2 == 0:
                        pygame.draw.rect(screen, grey, (270 + 45 * i, 45 * j, 45, 45))
                    else:
                        pygame.draw.rect(screen, dark_grey, (270 + 45 * i, 45 * j, 45, 45))
                elif self.field[i][j] == 'snake':
                    pygame.draw.rect(screen, green, (270 + 45 * i + 3, 45 * j + 3, 39, 39))
                elif self.field[i][j] == 'apple':
                    pygame.draw.rect(screen, red, (270 + 45 * i + 3, 45 * j + 3, 39, 39))
                elif self.field[i][j] == 'wall':
                    pygame.draw.rect(screen, black, (270 + 45 * i + 3, 45 * j + 3, 39, 39))
        press_q_font = pygame.font.Font(None, 25)
        press_q_text = press_q_font.render('Press Q to quit.', 1, black)
        screen.blit(press_q_text, (40, 85))
        if game == 'over':
            game_over_font = pygame.font.Font(None, 50)
            game_over_text = game_over_font.render('Game over', 1, red)
            screen.blit(game_over_text, (40, 50))

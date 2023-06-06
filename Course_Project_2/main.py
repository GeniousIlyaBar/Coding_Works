import pygame
from Field import Field

width = 1440
height = 900
fps = 5
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (114, 114, 114)
dark_grey = (72, 72, 72)
start_block = 3
direction = 'none'
game = 'running'
gamer = 'human'
stage = 0
# sectors_entrance_exit = [[3, 60, 80],
#                          [80, 140, 160],
#                          [160, 220, 240],
#                          [240, 300, 320],
#                          [320, 383, 384],
#                          [384, 324, 304],
#                          [304, 244, 224],
#                          [224, 164, 144],
#                          [144, 87, 88],
#                          [88, 151, 171],
#                          [171, 231, 251],
#                          [251, 311, 331],
#                          [331, 391, 392],
#                          [392, 375, 376],
#                          [376, 339, 319],
#                          [319, 256, 255],
#                          [255, 252, 232],
#                          [232, 175, 176],
#                          [176, 179, 159],
#                          [159, 96, 95],
#                          [95, 92, 72],
#                          [72, 12, 11],
#                          [11, 7],
#                          [7, 3]]

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

activated_sectors_paths = [[3, 2, 1, 0, 20, 21, 22, 23, 43, 63, 62, 61, 60, 80],
                           [80, 81, 82, 83, 103, 123, 143, 142, 141, 121, 101, 100, 120, 140, 160],
                           [160, 180, 200, 201, 202, 182, 162, 163, 183, 203, 223, 222, 221, 220, 240],
                           [240, 260, 261, 241, 242, 243, 263, 262, 282, 283, 303, 302, 301, 300, 320],
                           [320, 321, 322, 323, 343, 363, 362, 361, 341, 340, 360, 380, 381, 382, 383, 384],
                           [384, 385, 386, 387, 367, 366, 346, 347, 327, 326, 325, 345, 344, 324, 304],
                           [304, 305, 306, 307, 287, 286, 285, 265, 266, 267, 247, 246, 245, 244, 224],
                           [224, 225, 226, 227, 207, 187, 186, 206, 205, 204, 184, 185, 165, 164, 144],
                           [144, 145, 146, 147, 127, 126, 125, 124, 104, 84, 85, 105, 106, 86, 87, 88],
                           [88, 108, 128, 148, 149, 129, 109, 89, 90, 91, 111, 131, 151, 171],
                           [171, 191, 190, 170, 169, 168, 188, 189, 209, 208, 228, 229, 230, 231, 251],
                           [251, 250, 249, 248, 268, 288, 308, 309, 310, 290, 270, 271, 291, 311, 331],
                           [331, 330, 329, 328, 348, 349, 350, 351, 371, 370, 369, 389, 390, 391, 392],
                           [392, 372, 352, 332, 333, 353, 373, 374, 354, 334, 335, 355, 375, 376],
                           [376, 396, 397, 377, 357, 337, 338, 358, 378, 398, 399, 379, 359, 339, 319],
                           [319, 318, 317, 316, 296, 276, 277, 278, 298, 299, 279, 259, 258, 257, 256, 255],
                           [255, 275, 295, 315, 314, 313, 312, 292, 272, 273, 274, 254, 253, 252, 232],
                           [232, 212, 192, 172, 173, 193, 213, 233, 234, 235, 215, 195, 175, 176],
                           [176, 196, 216, 236, 237, 217, 197, 198, 218, 238, 239, 219, 199, 179, 159],
                           [159, 158, 157, 156, 136, 137, 138, 139, 119, 99, 98, 118, 117, 97, 96, 95],
                           [95, 115, 135, 155, 154, 134, 114, 113, 133, 153, 152, 132, 112, 92, 72],
                           [72, 52, 53, 73, 74, 54, 55, 75, 76, 56, 57, 77, 78, 79, 59, 58, 38, 39, 19, 18, 17, 16, 15, 35, 34, 14, 13, 33, 32, 12, 11],
                           [11, 31, 51, 71, 70, 50, 49, 69, 68, 48, 28, 29, 9, 8, 7],
                           [7, 27, 47, 67, 66, 65, 64, 44, 24, 25, 26, 6, 5, 4, 3]]

pygame.init()
pygame.mixer.init()  #sound
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Ultimate Snake Bot")
clock = pygame.time.Clock()
h, w = screen.get_size()

table = [['empty'] * 20 for i in range(20)]
blocks = list(range(0,400))
field = Field(table, blocks)
snake = []
snake.append(start_block)
field.field[start_block % 20][start_block // 20] = 'snake'

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

def follow_path(path):
    current_block = path[0]
    next_block = path[1]
    if next_block - current_block == 1:
        return 'right'
    elif next_block - current_block == -1:
        return 'left'
    elif next_block - current_block == 20:
        return 'down'
    elif next_block - current_block == -20:
        return 'up'
    field.path_to_apple.pop(0)

def build_path(graph, snake_head, apple):
    found_flag = False
    queue = []
    pred = list(range(400))
    dist = list(range(400))

    visited = [False for i in range(400)]

    for i in range(400):
        dist[i] = 1000000
        pred[i] = -1

    visited[snake_head] = True
    dist[snake_head] = 0
    current_sector = define_sector(snake_head)
    queue.append(snake_head)

    while (len(queue) != 0):
        u = queue[0]
        queue.pop(0)
        for i in range(len(graph[u])):
            if (visited[graph[u][i]] == False and (define_sector(graph[u][i]) == current_sector or graph[u][i] == apple)):
                visited[graph[u][i]] = True
                dist[graph[u][i]] = dist[u] + 1
                pred[graph[u][i]] = u
                queue.append(graph[u][i])

                if (graph[u][i] == apple):
                    found_flag = True
                    break

        if found_flag == True:
            break

    if found_flag == True:
        path = []
        crawl = apple
        path.append(crawl)

        while (pred[crawl] != -1):
            path.append(pred[crawl])
            crawl = pred[crawl]
        return list(reversed(path))
    else:
        return []

running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.QUIT:
                direction = 'none'
                running = False
            if game == 'running':
                if event.key == pygame.K_LEFT:
                    if direction != 'right':
                        direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    if direction != 'left':
                        direction = 'right'
                elif event.key == pygame.K_UP:
                    if direction != 'down':
                        direction = 'up'
                elif event.key == pygame.K_DOWN:
                    if direction != 'up':
                        direction = 'down'
                elif event.key == pygame.K_q:
                    pygame.quit()
                elif event.key == pygame.K_h:
                    gamer = 'hamilton'
                elif event.key == pygame.K_b:
                    gamer = 'bot'
                elif event.key == pygame.K_w:
                    gamer = 'winner'
                elif event.key == pygame.K_f:
                    fps += 5
                elif event.key == pygame.K_s:
                    fps -= 5
                elif event.key == pygame.K_r:
                    field.restart()
                    snake = []
                    snake.append(start_block)
                    field.field[start_block % 20][start_block // 20] = 'snake'
                    game = 'running'
                    direction = 'none'
            if game == 'over':
                if event.key == pygame.K_r:
                    field.restart()
                    snake = []
                    snake.append(start_block)
                    field.field[start_block % 20][start_block // 20] = 'snake'
                    game = 'running'

    # Обновление

    if gamer == 'winner':
        head_sector = define_sector(snake[0])
        apple_sector = define_sector(field.apple)
        if field.sectors_status[head_sector] == 'disactivated':
            if head_sector == apple_sector:
                field.path = build_path(field.graph, snake[0], field.apple)
                field.path += build_path(field.graph, field.apple, sectors_entrance_exit[head_sector][1])
                direction = follow_path(field.path)
            else:
                field.path = build_path(field.graph, snake[0], sectors_entrance_exit[head_sector][1])
                direction = follow_path(field.path)
        else:
            start = 0
            for i in range(len(activated_sectors_paths[define_sector(snake[0])])):
                if activated_sectors_paths[define_sector(snake[0])][i] == snake[0]:
                    start = i
                    break
            field.path = activated_sectors_paths[define_sector(snake[0])][start:]
            direction = follow_path(field.path)




    if gamer == 'bot':
        field.path_to_apple = build_path(field.graph, snake[0], field.apple)
        current_block = field.path_to_apple[0]
        next_block = 0
        next_block = field.path_to_apple[1]
        if next_block - current_block == 1:
            direction = 'right'
        elif next_block - current_block == -1:
            direction = 'left'
        elif next_block - current_block == 20:
            direction = 'down'
        elif next_block - current_block == -20:
            direction = 'up'
        field.path_to_apple.pop(0)

    if gamer == 'hamilton':


        if stage == 3:
            if snake[0] % 20 != 0:
                direction = 'left'
            else:
                direction = 'down'
                stage = 2

        if stage == 2:
            if snake[0] // 20 != 19 and direction == 'down':
                direction = 'down'
            if snake[0] // 20 == 19 and direction == 'down':
                direction = 'right'
            elif snake[0] // 20 == 19 and direction == 'right':
                direction = 'up'

            if snake[0] // 20 != 1 and direction == 'up':
                direction = 'up'
            if snake[0] // 20 == 1 and direction == 'up':
                direction = 'right'
            elif snake[0] // 20 == 1 and direction == 'right':
                direction = 'down'

            if snake[0] // 20 == 1 and snake[0] % 20 == 19 and direction == 'right':
                direction = 'up'
                stage = 3

    if direction == 'up':
        if snake[0] // 20 == 0 or field.field[snake[0] % 20][snake[0] // 20 - 1] == 'snake' or field.field[snake[0] % 20][snake[0] // 20 - 1] == 'wall':
            direction = 'none'
            game = 'over'
        else:
            snake.insert(0, snake[0] - 20)
            if field.field[snake[0] % 20][snake[0] // 20] == 'apple':
                field.field[snake[0] % 20][snake[0] // 20] = 'snake'
                field.create_apple()
                field.create_wall(snake[0])
                field.reset_graph(snake[0])
            else:
                field.field[snake[-1] % 20][snake[-1] // 20] = 'empty'
                field.field[snake[0] % 20][snake[0] // 20] = 'snake'
                snake.pop()
    elif direction == 'down':
        if snake[0] // 20 == 19 or field.field[snake[0] % 20][snake[0] // 20 + 1] == 'snake' or field.field[snake[0] % 20][snake[0] // 20 + 1] == 'wall':
            direction = 'none'
            game = 'over'
        else:
            snake.insert(0, snake[0] + 20)
            if field.field[snake[0] % 20][snake[0] // 20] == 'apple':
                field.field[snake[0] % 20][snake[0] // 20] = 'snake'
                field.create_apple()
                field.create_wall(snake[0])
                field.reset_graph(snake[0])
            else:
                field.field[snake[-1] % 20][snake[-1] // 20] = 'empty'
                field.field[snake[0] % 20][snake[0] // 20] = 'snake'
                snake.pop()
    elif direction == 'right':
        if snake[0] % 20 == 19 or field.field[snake[0] % 20 + 1][snake[0] // 20] == 'snake' or field.field[snake[0] % 20 + 1][snake[0] // 20] == 'wall':
            direction = 'none'
            game = 'over'
        else:
            snake.insert(0, snake[0] + 1)
            if field.field[snake[0] % 20][snake[0] // 20] == 'apple':
                field.field[snake[0] % 20][snake[0] // 20] = 'snake'
                field.create_apple()
                field.create_wall(snake[0])
                field.reset_graph(snake[0])
            else:
                field.field[snake[-1] % 20][snake[-1] // 20] = 'empty'
                field.field[snake[0] % 20][snake[0] // 20] = 'snake'
                snake.pop()
    elif direction == 'left':
        if snake[0] % 20 == 0 or field.field[snake[0] % 20 - 1][snake[0] // 20] == 'snake' or field.field[snake[0] % 20 - 1][snake[0] // 20] == 'wall':
            direction = 'none'
            game = 'over'
        else:
            snake.insert(0, snake[0] - 1)
            if field.field[snake[0] % 20][snake[0] // 20] == 'apple':
                field.field[snake[0] % 20][snake[0] // 20] = 'snake'
                field.create_apple()
                field.create_wall(snake[0])
                field.reset_graph(snake[0])
            else:
                field.field[snake[-1] % 20][snake[-1] // 20] = 'empty'
                field.field[snake[0] % 20][snake[0] // 20] = 'snake'
                snake.pop()


    # Рендеринг
    screen.fill(white)
    field.draw_field(screen, game)

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
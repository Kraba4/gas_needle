import pygame
import blocks
import generation
import motion

pygame.init()
blocks.init()
import entities
import palette

l = [[1, 1, 1], [1, blocks.block['empty'].id, blocks.block['empty'].id], [1, blocks.block['brain'].id, 1],
     [1, blocks.block['empty'].id, 1], [1, 1, 1]]

entity_group = []


def draw():
    global y_border
    global left_border
    screen.fill((0, 0, 0))
    for i in range(0, 600, 10):
        for j in range(0, 960, 10):
            screen.blit(blocks.block[blocks.name_from_id[field[i // 10 + 1][j // 10 + 1]]].image,
                        (left_border + j, y_border + i))
    for e in entities.entity:
        screen.blit(e.image, ((e.draw_pos[0] - 1) * 10 - 1 + 20, (e.draw_pos[1] - 1) * 10 - 1 + 60))
    for b in generation.buildings:
        screen.blit(blocks.block[b].image,
                    (generation.buildings[b][0] * 10 + left_border, y_border + generation.buildings[b][1] * 10))

    palette.draw(screen)


field = generation.create_new_world()
motion.init(62, 98)
motion.update_field(field, (1, 1), (96, 60))
y_border = 60
x_border = 180
left_border = 20
screen = pygame.display.set_mode((960 + left_border + x_border, 600 + 2 * y_border))  # pygame.resize
palette.init(960 + left_border, 0, 180, 600 + 2 * y_border, 'player')
pygame.display.set_caption('Gas needle')
screen.fill((0, 0, 0))
#entities.entity.append(entities.EntityObject(l, (40, 20), (0, 0, 0), field))
#entities.entity.append(entities.EntityObject([[7, 1], [1, 1]], (45, 30), (0, 0, 0), field))
endGame = False

pos = pygame.mouse.get_pos()
highlight = [(0, 0), (0, 0)]
hold_pos = (-1, -1)
start_pos = (1, 1)
end_pos = (1, 1)
c = 0
time_last_click_1 = 0
time_last_click_2 = 0
start_time = pygame.time.Clock()
mouse = 0


def check_group(pos1, pos2):
    g = []
    pos1 = ((pos1[0]) // 10, (pos1[1]) // 10)
    pos2 = ((pos2[0]) // 10, (pos2[1]) // 10)

    for e in entities.entity:

        if pos1[0] + 1 <= e.pos[0] - 1 + e.size_x + 2 and pos1[1] + 1 <= e.pos[1] - 1 + e.size_y + 6:
            if e.pos[0] - 1 + 2 <= pos2[0] - 1 and e.pos[1] - 1 + 6 <= pos2[1] - 1:
                g.append(e)
    return g


while not endGame:
    start_time.tick(60)
    c += 1
    for e in entities.entity:
        e.update_move()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endGame = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                field = generation.create_new_world()
                motion.update_field(field, (1, 1), (96, 60))

                entities.field = field.copy()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            posX = event.pos[0] // 10 * 10
            posY = event.pos[1] // 10 * 10
            hold_pos = (posX, posY)
            start_pos = (posX // 10 - 2 + 1, posY // 10 - 6 + 1)
            if mouse == 0:
                mouse = 1
            if c - time_last_click_1 < 10:
                palette.check_mouse_down((event.pos[0], (event.pos[1])), 6)

            time_last_click_1 = c
            palette.check_mouse_down((event.pos[0], (event.pos[1])), 1)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            posX = event.pos[0] // 10 * 10
            posY = event.pos[1] // 10 * 10
            end_pos = (posX // 10 - 2 + 1, posY // 10 - 6 + 1)
            for e in entity_group:
                entities.entity_commands[e] = end_pos
                e.finish = True
                e.finish_end = False
                e.move_set = motion.make_path((e.size_x, e.size_y), e.pos, entities.entity_commands[e])
                e.end_pos = e.move_set[0]
                for i in range(e.size_y):
                    e.saved_bg.append([])
                    for j in range(e.size_x):
                        e.saved_bg[i].append(field[e.pos[1] + i][e.pos[0] + j])

            if mouse == 0:
                mouse = 3
        elif event.type == pygame.MOUSEBUTTONDOWN and (event.button == 4 or event.button == 5):
            palette.check_mouse_down((event.pos[0], (event.pos[1])), event.button)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:

            time_last_click_2 = c
            palette.check_mouse_down((event.pos[0], (event.pos[1])), 2)

            if mouse == 0:
                mouse = 2
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            entity_group = check_group((min(pos[0], hold_pos[0]), min(pos[1], hold_pos[1])),
                                       (max(pos[0], hold_pos[0]), max(pos[1], hold_pos[1])))

            hold_pos = (-1, -1)
            mouse = 0
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            mouse = 0
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:
            mouse = 0
            palette.check_mouse_up(event.pos, 2, field)

    new_pos = pygame.mouse.get_pos()
    if new_pos != pos:
        pos = new_pos
    draw()
    if mouse != 0:
        palette.check_mouse_down_hold((pos[0], (pos[1])), mouse)

    palette.update(((pos[0] // 10 * 10), pos[1] // 10 * 10), field)
    if hold_pos[0] > 960 + left_border:
        hold_pos = (960 + left_border, hold_pos[1])
    if pos[0] > 960 + left_border:
        pos = (960 + left_border, pos[1])
    if hold_pos != (-1, -1):
        highlight[0] = (min(hold_pos[0], pos[0] // 10 * 10), min(hold_pos[1], pos[1] // 10 * 10))
        highlight[1] = (max(hold_pos[0], pos[0] // 10 * 10), max(hold_pos[1], pos[1] // 10 * 10))
        highlightSurf = pygame.Surface((abs(hold_pos[0] - pos[0] // 10 * 10), abs(hold_pos[1] - pos[1] // 10 * 10)))
        highlightSurf.fill((0, 0, 0))
        highlightSurf.set_alpha(100)
        screen.blit(highlightSurf, highlight[0])
    pygame.display.flip()

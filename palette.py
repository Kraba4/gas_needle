import pygame
import entities
import blocks
import numpy
import motion
import json
import client_tool


class Player:
    def __init__(self, name):
        self.name = name
        a = 0
        b = 0
        c = 0
        for i in name:
            a += ord(i)
            b += ord(i.encode('koi8-r'))
            c += ord(i.encode('cp1252'))
        self.color = (a % 256, (b + 50) % 256, (c + 100) % 256)
        self.image = font2.render(self.name, True, self.color)

    def draw(self):
        palette.blit(self.image, (20, 20))


draw_picture = None
palette = None
start_x, start_y = None, None
font = pygame.font.SysFont('arial', 12)
font2 = pygame.font.SysFont('arial', 20)
res_info = {}
arrow_up = None
arrow_down = None

picture_collection = None
picked_block = blocks.block['empty']
erase_button = None
buttons = []
id_empty = blocks.block['empty'].id
holded = None
hold = False
player = None


class NoneBlock:
    def __init__(self, block):
        self.image = block.image.copy()
        self.image.set_alpha(100)
        self.id = block.id
        self.color = block.color


def update(pos, field):
    global picked_block
    if hold:
        holded.set_pos(pos)
        holded.check_pos((pos[0], pos[1]), field, False)


def arrow_up_func():
    picture_collection.add_offset(-1)


def arrow_down_func():
    picture_collection.add_offset(1)


def erase_button_func():
    draw_picture.fill(blocks.block['empty'])


def fill_button_func():
    for i in range(12):
        for j in range(12):
            if draw_picture.data[i][j] != blocks.block['empty']:
                if draw_picture.data_webber[i][j] == 0 and res_info[draw_picture.data[i][j].id].amount > 0:
                    draw_picture.data_webber[i][j] = 1
                    res_info[draw_picture.data[i][j].id].add(-1)
                    draw_picture.image.blit(draw_picture.data[i][j].image, (j * 10 + 10, i * 10 + 10))


def add_button_func():
    l = []
    for i in range(12):
        l.append([])
        for j in range(12):
            l[i].append(draw_picture.data[i][j].id)

    picture_collection.append(Picture((0, 0), l))


def draw(surface):
    palette.fill((50, 50, 50))
    for r in res_info:
        res_info[r].draw()
    draw_picture.draw()
    picture_collection.draw()
    player.draw()
    for b in buttons:
        b.draw()
    if picked_block != blocks.block['empty']:
        pygame.draw.rect(palette, picked_block.color,
                         ((res_info[picked_block.id].x - 4, res_info[picked_block.id].y - 4), (28, 28)), 1)
    surface.blit(palette, (start_x, start_y))
    if hold:
        holded.draw(surface)


def init(x, y, width, height, name):
    global palette
    global start_x
    global start_y
    global draw_picture, picture_collection, arrow_up, arrow_down, erase_button, player
    start_x = x
    start_y = y
    palette = pygame.Surface((width, height))
    palette.fill((50, 50, 50))
    player = Player(name)
    DOWN = 100
    RIGHT = 15
    ResInfo(blocks.block['obsidian'], 10, (20 + RIGHT, 20 + DOWN))
    ResInfo(blocks.block['dirt'], 1, (100 + RIGHT, 20 + DOWN))
    ResInfo(blocks.block['grass'], 1, (20 + RIGHT, 60 + DOWN))
    ResInfo(blocks.block['hard_stone'], 2, (100 + RIGHT, 60 + DOWN))
    ResInfo(blocks.block['wood'], 4, (20 + RIGHT, 100 + DOWN))
    ResInfo(blocks.block['gas'], 8, (100 + RIGHT, 100 + DOWN))
    ResInfo(blocks.block['fire'], 6, (20 + RIGHT, 140 + DOWN))
    ResInfo(blocks.block['water'], 2, (100 + RIGHT, 140 + DOWN))
    ResInfo(blocks.block['leaves'], 2, (20 + RIGHT, 180 + DOWN))
    ResInfo(blocks.block['brain'], 20, (100 + RIGHT, 180 + DOWN))
    ResInfo(blocks.block['philosof'], 1, (20 + RIGHT, -20 + DOWN))

    l = [[-1] * 12] * 12
    draw_picture = Picture((20, 320), l)
    picture_collection = Collection((20, 480))
    Button((20, 465), (140, 10), blocks.block['button_up'], arrow_up_func)
    Button((20, 695), (140, 10), blocks.block['button_down'], arrow_down_func)
    Button((165, 320), (10, 10), blocks.block['button_erase'], erase_button_func)
    Button((165, 430), (10, 10), blocks.block['button_fill'], fill_button_func)
    Button((165, 450), (10, 10), blocks.block['button_add'], add_button_func)
    res_info[blocks.block['dirt'].id].add(2)


def check_mouse_down_hold(pos, mouse):
    if pos[0] - 980 >= 0:
        if pos[1] <= 320:
            pass
        else:
            if mouse != 2:
                draw_picture.check_hold((pos[0] - 980, pos[1]), mouse)


def check_mouse_up(pos, mouse, field):
    if mouse == 2 and holded is not None:
        holded.check_pos((pos[0], pos[1]), field, True)


def check_mouse_down(pos, mouse):
    if pos[0] - 980 >= 0:
        if pos[1] <= 320:
            for r in res_info:
                res_info[r].check_mouse_pick((pos[0] - 980, pos[1]))
        else:
            draw_picture.check_click((pos[0] - 980, pos[1]), mouse)
            picture_collection.check_click((pos[0] - 980, pos[1]), mouse)
            for b in buttons:
                b.check_click((pos[0] - 980, pos[1]), mouse)


class ResInfo:
    def __init__(self, block, price, pos):
        self.block = block
        self.price = price
        self.amount = 26
        self.image = pygame.Surface((60, 40), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 0))
        a = pygame.transform.scale(self.block.image, (20, 20))
        self.image.blit(a, (0, 0))
        text = font.render(str(self.amount), False, (255, 255, 255))
        self.image.blit(text, (30, 0))
        self.x = pos[0]
        self.y = pos[1]
        res_info[self.block.id] = self

    def add(self, x):
        self.amount += x
        if self.amount < 0:
            self.amount = 0
        text = font.render(str(self.amount), False, (255, 255, 255))
        a = pygame.Surface((30, 40))
        a.fill((50, 50, 50, 255))
        self.image.blit(a, (30, 0))
        self.image.blit(text, (30, 0))

    def draw(self):
        global palette
        palette.blit(self.image, (self.x, self.y))

    def check_mouse_pick(self, pos):
        global picked_block
        width = 20
        height = 20
        if self.x <= pos[0] <= self.x + width and self.y <= pos[1] <= self.y + height:
            picked_block = self.block


class HoldedPicture:
    def __init__(self, data, pos, offset):
        self.x = pos[0]
        self.y = pos[1]
        self.data = data
        self.size_x = len(data[0])
        self.size_y = len(data)
        self.offset_x = offset[0]
        self.offset_y = offset[1]
        self.image = pygame.Surface((self.size_x * 10, self.size_y * 10), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 0))
        for i in range(self.size_y):
            for j in range(self.size_x):
                if data[i][j] != id_empty:
                    self.image.blit(blocks.block[blocks.name_from_id[data[i][j]]].image, (j * 10, i * 10))

    def draw(self, surface):
        surface.blit(self.image, (self.x - self.offset_x, self.y - self.offset_y))

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def check_pos(self, pos, field, drop):
        global hold
        if hold:
            if pos[0] < 980:
                if pos[0] - self.offset_x > 20 and pos[0] - self.offset_x + self.size_x * 10 <= 980 and pos[
                    1] - self.offset_y > 60 and pos[1] - self.offset_y + self.size_y * 10 <= 660:
                    x = (pos[0] - self.offset_x - 20) // 10 + 1
                    y = (pos[1] - self.offset_y - 60) // 10 + 1
                    flag = True
                    if drop:
                        e = entities.EntityObject(self.data, (x, y), player.color, field)
                        new_data, eq = e.update_body()

                        for i in range(self.size_y):
                            for j in range(self.size_x):
                                if new_data[i][j] != id_empty:
                                    field[y + i][x + j] = new_data[i][j]

                        motion.update_field(field, (x, y), (x + self.size_x, y + self.size_y))
                        #client_tool.trade_with_server((field, 'give_field', player.name))
                        entities.entity.extend(eq)
                        #client_tool.trade_with_server((eq, 'give_entities', player.name))
                        hold = False
                    else:
                        flag = True
                        for i in range(self.size_y):
                            for j in range(self.size_x):
                                if motion.field_x[y + i][x + j] == 0 and self.data[i][j] != id_empty:
                                    flag = False
                        if flag:
                            self.image.set_alpha(255)
                        else:
                            self.image.set_alpha(100)
            else:
                if drop:
                    if pos[1] >= 480:
                        picture_collection.append(Picture((0, 0), self.data))
                    for i in range(self.size_y):
                        for j in range(self.size_x):
                            if self.data[i][j] != id_empty:
                                res_info[self.data[i][j]].add(1)

        if drop:
            hold = False


class Picture:
    def __init__(self, pos, field):
        self.data = [[], [], [], [],
                     [], [], [], [],
                     [], [], [], []]
        self.data_webber = [[], [], [], [],
                            [], [], [], [],
                            [], [], [], []]

        if field is not None:
            for i in range(12):
                for j in range(12):
                    if i < len(field) and j < len(field[0]):
                        if field[i][j] == -1:
                            self.data[i].append(blocks.block['empty'])
                        else:
                            self.data[i].append(blocks.block[blocks.name_from_id[field[i][j]]])
                    else:
                        self.data[i].append(blocks.block['empty'])
        else:
            for i in range(12):
                for j in range(12):
                    self.data[i].append(blocks.block['empty'])
        for i in range(12):
            for j in range(12):
                self.data_webber[i].append(0)

        self.x = pos[0]
        self.y = pos[1]
        self.size_x = 10 * 12 + 20
        self.size_y = 10 * 12 + 20
        self.width = 12
        self.height = 12
        self.image = pygame.Surface((10 * 12 + 20, 10 * 12 + 20), pygame.SRCALPHA)
        self.image.fill((0, 0, 0))
        for i in range(12):
            for j in range(12):
                self.image.blit(self.data[i][j].image, (j * 10 + 10, i * 10 + 10))

    def fill(self, new_block):
        for i in range(12):
            for j in range(12):
                if self.data_webber[i][j] == 1:
                    res_info[self.data[i][j].id].add(1)
                    self.data_webber[i][j] = 0
                self.data[i][j] = new_block
                self.image.blit(self.data[i][j].image, (j * 10 + 10, i * 10 + 10))

    def copy_image(self, pic):
        for i in range(12):
            for j in range(12):
                if self.data[i][j].id != id_empty and self.data_webber[i][j] == 1:
                    res_info[self.data[i][j].id].add(1)
                self.data[i][j] = pic.data[i][j]
                self.data_webber[i][j] = 0

        for i in range(12):
            for j in range(12):
                self.image.blit(blocks.block['empty'].image, (j * 10 + 10, i * 10 + 10))
                a = NoneBlock(pic.data[i][j])
                self.image.blit(a.image, (j * 10 + 10, i * 10 + 10))

    def draw(self):
        palette.blit(self.image, (self.x, self.y))

    def check_hold(self, pos, mouse):
        global picked_block, holded
        if self.x + 10 <= pos[0] < self.x + self.size_x - 10 and self.y + 10 <= pos[1] < self.y + self.size_y - 10:
            x = (pos[0] - (self.x + 10)) // 10
            y = (pos[1] - (self.y + 10)) // 10
            if mouse == 1:
                if picked_block.id == blocks.block['philosof'].id:
                    if self.data[y][x].id != id_empty and self.data_webber[y][x] == 0 and res_info[
                        picked_block.id].amount > 0:
                        self.data_webber[y][x] = 1
                        res_info[picked_block.id].add(-1)
                        self.image.blit(self.data[y][x].image, (x * 10 + 10, y * 10 + 10))
                elif picked_block.id != id_empty and self.data[y][x].id != picked_block.id:
                    if self.data_webber[y][x] == 1:
                        res_info[self.data[y][x].id].add(1)
                    self.data[y][x] = picked_block
                    p_b = picked_block
                    if res_info[picked_block.id].amount == 0:
                        self.data_webber[y][x] = 0
                        p_b = NoneBlock(picked_block)
                    else:
                        self.data_webber[y][x] = 1
                        res_info[picked_block.id].add(-1)
                    self.image.blit(blocks.block['empty'].image, (x * 10 + 10, y * 10 + 10))
                    self.image.blit(p_b.image, (x * 10 + 10, y * 10 + 10))
            elif mouse == 3:
                if self.data[y][x] != blocks.block['empty']:
                    if self.data_webber[y][x] == 1:
                        res_info[self.data[y][x].id].add(1)
                    self.data_webber[y][x] = 0
                    self.data[y][x] = blocks.block['empty']
                    self.image.blit(blocks.block['empty'].image, (x * 10 + 10, y * 10 + 10))

    def check_click(self, pos, mouse):
        global picked_block, holded, hold
        if self.x + 10 <= pos[0] < self.x + self.size_x - 10 and self.y + 10 <= pos[1] < self.y + self.size_y - 10:
            x = (pos[0] - (self.x + 10)) // 10
            y = (pos[1] - (self.y + 10)) // 10
            if mouse == 2:
                if self.data[y][x] != blocks.block['empty']:
                    picked_block = self.data[y][x]
                    if not hold and self.data_webber[y][x] == 1:
                        elems = self.bfs(y, x, False)
                        body, pos1 = self.create_new_body(elems)

                        hold = True
                        holded = HoldedPicture(body, (pos[0] + 980, pos[1]), ((x - pos1[0]) * 10, (y - pos1[1]) * 10))
                else:
                    if not hold:
                        elems = self.bfs(y, x, True)
                        body, pos1 = self.create_new_body(elems)

                        hold = True
                        holded = HoldedPicture(body, (pos[0] + 980, pos[1]), ((x - pos1[0]) * 10, (y - pos1[1]) * 10))
            elif mouse == 6:
                if self.data[y][x] != blocks.block['empty'] and (
                        self.data[y][x].id == picked_block.id or picked_block.id == blocks.block['philosof'].id):
                    block = self.data[y][x]
                    for i in range(12):
                        for j in range(12):
                            if self.data[i][j] == block and self.data_webber[i][j] == 0 and res_info[
                                picked_block.id].amount > 0:
                                self.data_webber[i][j] = 1

                                self.image.blit(block.image, (j * 10 + 10, i * 10 + 10))
                                res_info[picked_block.id].add(-1)

    def create_new_body(self, elems):
        min_j = min_i = 1123456789
        max_j = max_i = -1
        for e in elems:
            max_j = max(max_j, e[1])
            max_i = max(max_i, e[0])
            min_j = min(min_j, e[1])
            min_i = min(min_i, e[0])
        new_i = max_i - min_i + 1
        new_j = max_j - min_j + 1
        new_body = numpy.ndarray((new_i, new_j), 'int')
        for i in range(new_i):
            for j in range(new_j):
                new_body[i][j] = id_empty
        for e in elems:
            if self.data_webber[e[0]][e[1]] == 1:
                new_body[e[0] - min_i][e[1] - min_j] = self.data[e[0]][e[1]].id
                self.data_webber[e[0]][e[1]] = 0
                self.image.blit(blocks.block['empty'].image, (e[1] * 10 + 10, e[0] * 10 + 10))
                a = NoneBlock(self.data[e[0]][e[1]])
                self.image.blit(a.image, (e[1] * 10 + 10, e[0] * 10 + 10))
        return new_body, (min_j, min_i)

    def bfs(self, i, j, isEmpty):
        que = []
        elems = []
        elems_bfs = numpy.ndarray((len(self.data[0]), len(self.data)), 'int')
        if isEmpty:
            for i1 in range(self.height):
                for j1 in range(self.width):
                    elems.append((i1, j1))
            return elems
        for i1 in range(self.height):
            for j1 in range(self.width):
                elems_bfs[i1][j1] = 0
        que.append((i, j))
        elems.append((i, j))
        elems_bfs[i][j] = 1
        while len(que) > 0:
            i, j = que.pop(0)
            if j + 1 < self.width and self.data[i][j + 1].id != id_empty and elems_bfs[i][j + 1] == 0:
                que.append((i, j + 1))
                elems.append((i, j + 1))
                elems_bfs[i][j + 1] = 1
            if j - 1 >= 0 and self.data[i][j - 1].id != id_empty and elems_bfs[i][j - 1] == 0:
                que.append((i, j - 1))
                elems.append((i, j - 1))
                elems_bfs[i][j - 1] = 1
            if i + 1 < self.height and self.data[i + 1][j].id != id_empty and elems_bfs[i + 1][j] == 0:
                que.append((i + 1, j))
                elems.append((i + 1, j))
                elems_bfs[i + 1][j] = 1
            if i - 1 >= 0 and self.data[i - 1][j].id != id_empty and elems_bfs[i - 1][j] == 0:
                que.append((i - 1, j))
                elems.append((i - 1, j))
                elems_bfs[i - 1][j] = 1

        return elems


class Button:
    def __init__(self, pos, size, block, func):
        global buttons
        self.x = pos[0]
        self.y = pos[1]
        self.size_x = size[0]
        self.size_y = size[1]
        self.image = pygame.transform.scale(block.image, size)
        self.func = func
        buttons.append(self)

    def draw(self):
        palette.blit(self.image, (self.x, self.y))

    def check_click(self, pos, mouse):
        if mouse == 1 and self.x <= pos[0] <= self.x + self.size_x and self.y <= pos[1] <= self.y + self.size_y:
            self.func()


class Collection:
    def __init__(self, pos):
        with open("collection.json", "r") as read_file:
            self.data_info = json.load(read_file)
        self.data = []
        for d in self.data_info:
            self.data.append(Picture((0, 0), d))
        self.image = pygame.Surface((10 * 12 + 20, (10 * 12 + 20) // 2 * 3), pygame.SRCALPHA)
        self.image.fill((0, 0, 0))
        self.x = pos[0]
        self.y = pos[1]
        self.picture_offset = 0
        self.update()

    def draw(self):
        palette.blit(self.image, (self.x, self.y))

    def check_click(self, pos, mouse):
        global draw_picture
        if mouse == 1:
            if self.x <= pos[0] <= self.x + 70 and self.y <= pos[
                1] <= self.y + 70 and self.picture_offset * 2 + 0 < len(self.data):
                draw_picture.copy_image(self.data[self.picture_offset * 2 + 0])
            elif self.x + 70 <= pos[0] <= self.x + 140 and self.y <= pos[
                1] <= self.y + 70 and self.picture_offset * 2 + 1 < len(self.data):
                draw_picture.copy_image(self.data[self.picture_offset * 2 + 1])
            elif self.x <= pos[0] <= self.x + 70 and self.y + 70 <= pos[
                1] <= self.y + 140 and self.picture_offset * 2 + 2 < len(self.data):
                draw_picture.copy_image(self.data[self.picture_offset * 2 + 2])
            elif self.x + 70 <= pos[0] <= self.x + 140 and self.y + 70 <= pos[
                1] <= self.y + 140 and self.picture_offset * 2 + 3 < len(self.data):
                draw_picture.copy_image(self.data[self.picture_offset * 2 + 3])
            elif self.x <= pos[0] <= self.x + 70 and self.y + 140 <= pos[
                1] <= self.y + 210 and self.picture_offset * 2 + 4 < len(self.data):
                draw_picture.copy_image(self.data[self.picture_offset * 2 + 4])
            elif self.x + 70 <= pos[0] <= self.x + 140 and self.y + 140 <= pos[
                1] <= self.y + 210 and self.picture_offset * 2 + 5 < len(self.data):
                draw_picture.copy_image(self.data[self.picture_offset * 2 + 5])
        elif mouse == 4:
            if self.x <= pos[0] <= self.x + 140 and self.y <= pos[1] <= self.y + 210:
                self.add_offset(-1)
        elif mouse == 5:
            if self.x <= pos[0] <= self.x + 140 and self.y <= pos[1] <= self.y + 210:
                self.add_offset(1)

    def append(self, new_picture):
        self.data.append(new_picture)
        l = []
        for i in range(12):
            l.append([])
            for j in range(12):
                l[i].append(new_picture.data[i][j].id)

        self.data_info.append(l)
        self.update()
        with open("collection.json", "w") as write_file:
            json.dump(self.data_info, write_file)

    def add_offset(self, offset):
        if offset != 0:
            if 0 <= self.picture_offset + offset < len(self.data) // 2:
                self.picture_offset += offset
                self.update()

    def update(self):
        for i in range(6):
            index = i + (self.picture_offset * 2)
            if index < len(self.data):
                a = pygame.transform.scale(self.data[index].image, (70, 70))
                self.image.blit(a, (70 * (i % 2), 70 * (i // 2)))
            else:
                pygame.draw.rect(self.image, (0, 0, 0), ((70 * (i % 2), 70 * (i // 2)), (70, 70)))

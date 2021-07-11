import random
import numpy
import blocks

field = numpy.ndarray((62, 98), 'int')
max_h = -1
x_gen = -8  # random.randrange(-20,10)
y_gen = 25  # random.randrange(-10,30)

buildings = dict()


def average(arr):
    sum = 0
    global max_h
    for i in arr:
        sum += i
    global x_gen
    global y_gen
    sum = sum / len(arr) + random.randrange(min(x_gen, y_gen), max(x_gen, y_gen) + 1)
    max_h = max(max_h, sum)
    return sum

size_r = 0
def direct_river(x, y):
    global size_r
    size_r += 1
    if size_r > 1000:
        return
    g = [blocks.block['grass'].id,blocks.block['grass2'].id, blocks.block['grass3'].id ]
    if field[y][x] in g:
        field[y][x] = blocks.block['water'].id
        direct = random.randrange(0, 4)
        if direct == 0:
            if x + 1 < 96:
                direct_river(x + 1, y)
            if y + 1 < 60:
                direct_river(x, y + 1)
            if x - 1 > 0:
                direct_river(x - 1, y)
            if y - 1 > 0:
                direct_river(x, y - 1)
        elif direct == 1:
            if y + 1 < 60:
                direct_river(x, y + 1)
            if x - 1 > 0:
                direct_river(x - 1, y)
            if y - 1 > 0:
                direct_river(x, y - 1)
            if x + 1 < 96:
                direct_river(x + 1, y)
        elif direct == 2:
            if x - 1 > 0:
                direct_river(x - 1, y)
            if y - 1 > 0:
                direct_river(x, y - 1)
            if x + 1 < 96:
                direct_river(x + 1, y)
            if y + 1 < 60:
                direct_river(x, y + 1)
        elif direct == 3:
            if y - 1 > 0:
                direct_river(x, y - 1)
            if x + 1 < 96:
                direct_river(x + 1, y)
            if y + 1 < 60:
                direct_river(x, y + 1)
            if x - 1 > 0:
                direct_river(x - 1, y)
    else:
        return


def gen_river():
    global size_r
    while size_r < 10:
        direct_river(random.randrange(1, 96), random.randrange(1, 58))
    size_r = 0


def gen_deep_dirt():
    find = blocks.block['dirt'].id
    g = [blocks.block['dirt'].id, blocks.block['deep_dirt'].id, blocks.block['obsidian'].id]
    rep = blocks.block['deep_dirt'].id
    for i in range(1, 61):
        for j in range(1, 97):
            if field[i][j] == find:
                count = 0
                if field[i][j + 1] in g:
                    count += 1
                if field[i][j - 1] in g:
                    count += 1
                if field[i + 1][j] in g:
                    count += 1
                if field[i - 1][j] in g:
                    count += 1

                if count >= 3:
                    field[i][j] = rep


def find_and_rep(i, j, find, group, rep):
    if field[i][j] == find:
        if field[i][j + 1] in group:
            field[i][j + 1] = rep
        elif field[i + 1][j] in group:
            field[i + 1][j] = rep
        elif field[i][j - 1] in group:
            field[i + 1][j - 1] = rep
        elif field[i - 1][j] in group:
            field[i - 1][j] = rep
        elif field[i - 1][j + 1] in group:
            field[i - 1][j + 1] = rep
        elif field[i - 1][j - 1] in group:
            field[i - 1][j - 1] = rep
        elif field[i + 1][j + 1] in group:
            field[i + 1][j + 1] = rep
        elif field[i + 1][j - 1] in group:
            field[i + 1][j - 1] = rep


def gen_add():
    g1 = [blocks.block['grass'].id, blocks.block['grass2'].id]
    rep1 = blocks.block['sand'].id
    g2 = [blocks.block['grass'].id, blocks.block['grass2'].id, blocks.block['grass3'].id]
    rep2 = blocks.block['wall'].id
    find1 = blocks.block['water'].id
    find2 = blocks.block['dirt'].id
    find4 = blocks.block['water'].id
    g4 = [blocks.block['water'].id, blocks.block['deep_water'].id]
    rep4 = blocks.block['deep_water'].id
    for i in range(1, 61):
        for j in range(1, 97):
            find_and_rep(i, j, find1, g1, rep1)
            find_and_rep(i, j, find2, g2, rep2)
            if field[i][j] == find4:
                if field[i][j + 1] in g4 and field[i][j - 1] in g4 and field[i + 1][j] in g4 and field[i - 1][j] in g4:
                    field[i][j] = rep4
    find4 = blocks.block['deep_water'].id
    g4 = [blocks.block['deep_water'].id, blocks.block['deep_water2'].id]
    rep4 = blocks.block['deep_water2'].id
    for i in range(1, 61):
        for j in range(1, 97):
            if field[i][j] == find4:
                count = 0
                if field[i][j + 1] in g4:
                    count += 1
                if field[i][j - 1] in g4:
                    count += 1
                if field[i + 1][j] in g4:
                    count += 1
                if field[i - 1][j] in g4:
                    count += 1

                if count >= 3:
                    field[i][j] = rep4


def gen_wall():
    find3 = blocks.block['hard_stone'].id
    g3 = [blocks.block['grass'].id, blocks.block['grass2'].id, blocks.block['grass3'].id]
    rep3 = blocks.block['wall'].id
    for i in range(1, 61):
        for j in range(1, 97):
            find_and_rep(i, j, find3, g3, rep3)


elems_bfs = numpy.ndarray((62, 98), 'int')


def bfs(i, j, type, touch=None):
    que = []
    elems = []
    que.append((i, j))
    elems.append((i, j))
    elems_bfs[i][j] = 1
    touch_res = False
    if touch == None:
        touch = (-1, -2)
    while len(que) > 0:
        i, j = que.pop(0)
        if not touch_res:
            if j + 1 < 97 and field[i][j + 1] in touch:
                touch_res = True
            if j - 1 >= 0 and field[i][j - 1] in touch:
                touch_res = True
            if i + 1 < 61 and field[i + 1][j] in touch:
                touch_res = True
            if i - 1 >= 0 and field[i - 1][j] in touch:
                touch_res = True
            if i - 1 >= 0 and j + 1 < 97 and field[i - 1][j + 1] in touch:
                touch_res = True
            if i - 1 >= 0 and j - 1 >= 0 and field[i - 1][j - 1] in touch:
                touch_res = True
            if i + 1 < 61 and j + 1 < 97 and field[i + 1][j + 1] in touch:
                touch_res = True
            if i + 1 < 61 and j - 1 >= 0 and field[i + 1][j - 1] in touch:
                touch_res = True

        if j + 1 < 97 and field[i][j + 1] in type and elems_bfs[i][j + 1] == 0:
            que.append((i, j + 1))
            elems.append((i, j + 1))
            elems_bfs[i][j + 1] = 1
        if j - 1 >= 0 and field[i][j - 1] in type and elems_bfs[i][j - 1] == 0:
            que.append((i, j - 1))
            elems.append((i, j - 1))
            elems_bfs[i][j - 1] = 1
        if i + 1 < 61 and field[i + 1][j] in type and elems_bfs[i + 1][j] == 0:
            que.append((i + 1, j))
            elems.append((i + 1, j))
            elems_bfs[i + 1][j] = 1
        if i - 1 >= 0 and field[i - 1][j] in type and elems_bfs[i - 1][j] == 0:
            que.append((i - 1, j))
            elems.append((i - 1, j))
            elems_bfs[i - 1][j] = 1
        if i + 1 < 61 and j + 1 < 97 and field[i + 1][j + 1] in type and elems_bfs[i + 1][j + 1] == 0:
            que.append((i + 1, j + 1))
            elems.append((i + 1, j + 1))
            elems_bfs[i + 1][j + 1] = 1
        if i + 1 < 61 and j - 1 >= 0 and field[i + 1][j - 1] in type and elems_bfs[i + 1][j - 1] == 0:
            que.append((i + 1, j - 1))
            elems.append((i + 1, j - 1))
            elems_bfs[i + 1][j - 1] = 1
        if i - 1 >= 0 and j + 1 < 98 and field[i - 1][j + 1] in type and elems_bfs[i - 1][j + 1] == 0:
            que.append((i - 1, j + 1))
            elems.append((i - 1, j + 1))
            elems_bfs[i - 1][j + 1] = 1
        if i - 1 >= 0 and j - 1 >= 0 and field[i - 1][j - 1] in type and elems_bfs[i - 1][j - 1] == 0:
            que.append((i - 1, j - 1))
            elems.append((i - 1, j - 1))
            elems_bfs[i - 1][j - 1] = 1
    return touch_res, elems


def clear():
    for i in range(0, 62):
        for j in range(0, 98):
            elems_bfs[i][j] = 0
    elems_set = numpy.ndarray((62, 98), 'int')
    for i in range(0, 62):
        for j in range(0, 98):
            elems_set[i][j] = 0

    type1 = (blocks.block['stone'].id, blocks.block['hard_stone'].id, blocks.block['snow_stone'].id,
             blocks.block['medium_stone'].id)
    type2 = [blocks.block['sand'].id]
    type3 = [blocks.block['dirt'].id, blocks.block['obsidian'].id, blocks.block['deep_dirt'].id]
    for i in range(0, 62):
        for j in range(0, 98):
            if field[i][j] in type1 and elems_set[i][j] == 0:
                res, elems = bfs(i, j, type1)
                if len(elems) <= 8:
                    for e in elems:
                        field[e[0]][e[1]] = blocks.block['grass'].id
                else:
                    for item in elems:
                        elems_set[item[0]][item[1]] = 1
            if field[i][j] == type2 and elems_set[i][j] == 0:
                res, elems = bfs(i, j, type2)
                if len(elems) <= 2 or len(elems) >= 8:
                    for e in elems:
                        field[e[0]][e[1]] = blocks.block['grass3'].id
                else:
                    for item in elems:
                        elems_set[item[0]][item[1]] = 1
            if field[i][j] in type3 and elems_set[i][j] == 0:
                res, elems = bfs(i, j, type3)
                if len(elems) <= 8:
                    for e in elems:
                        field[e[0]][e[1]] = blocks.block['grass3'].id
                else:
                    for item in elems:
                        elems_set[item[0]][item[1]] = 1


def water_grow():
    elems_set = set()
    type = [blocks.block['dirt'].id, blocks.block['obsidian'].id]
    for i in range(1, 61):
        for j in range(1, 97):
            if field[i][j] in type and not (i, j) in elems_set:
                res, elems = bfs(i, j, type, (blocks.block['water'].id, blocks.block['deep_water'].id))
                if res:
                    for e in elems:
                        field[e[0]][e[1]] = blocks.block['water'].id
                else:
                    elems_set = elems_set.union(elems)


def gen_square(terrain, left, up, right, down):
    center_x = left + (right - left) // 2
    center_y = up + (down - up) // 2
    terrain[center_y][center_x] = average(
        [terrain[up][left], terrain[up][right], terrain[down][left], terrain[down][right]])
    terrain[center_y][left] = average([terrain[up][left], terrain[center_y][center_x], terrain[down][left]])
    terrain[center_y][right] = average([terrain[up][right], terrain[center_y][center_x], terrain[down][right]])
    terrain[up][center_x] = average([terrain[up][left], terrain[center_y][center_x], terrain[up][right]])
    terrain[down][center_x] = average([terrain[down][left], terrain[center_y][center_x], terrain[down][right]])
    if (center_x - left) // 2 > 0:
        gen_square(terrain, left, up, center_x, center_y)
        gen_square(terrain, center_x, up, right, center_y)
        gen_square(terrain, left, center_y, center_x, down)
        gen_square(terrain, center_x, center_y, right, down)


def generate_terrain():
    global max_h,x_gen,y_gen
    max_h = -1
    x_gen = -13
    y_gen = 25
    terrain = numpy.ndarray((129, 129), 'int') #2^7 + 1
    m = 30
    terrain[0][0] = m
    terrain[0][128] = m
    terrain[128][0] = m
    terrain[128][128] = m
    gen_square(terrain, 0, 0, 128, 128)
    for i in range(62):
        for j in range(98):
            field[i][j] = abs(int(((terrain[i + 32][j + 30]) / max_h) * 9)) % 9
    for v in range(1):
        for i in range(62):
            for j in range(98):
                if i > 0 and 0 < j < 97 and i < 60:
                    if field[i + 1][j] == field[i - 1][j] == field[i][j + 1] == field[i][j - 1]:
                        field[i][j] = field[i][j + 1]
                    elif field[i + 1][j] == field[i - 1][j] == field[i][j + 1]:
                        field[i][j] = field[i][j + 1]
                    elif field[i + 1][j] == field[i - 1][j] == field[i][j - 1]:
                        field[i][j] = field[i][j - 1]
                    elif field[i + 1][j] == field[i][j + 1] == field[i][j - 1]:
                        field[i][j] = field[i + 1][j]
                    elif field[i - 1][j] == field[i][j + 1] == field[i][j - 1]:
                        field[i][j] = field[i - 1][j]

    for i in range(62):
        for j in range(98):
            if 0 < i < 60 and 0 < j < 97:
                if field[i + 1][j] in range(2, 5) and field[i - 1][j] in range(2, 5) and field[i][j + 1] in range(2,
                                                                                                                  5) and \
                        field[i][j - 1] in range(2, 5):
                    field[i][j] = field[i][j + 1]
                elif field[i + 1][j] in range(2, 5) and field[i - 1][j] in range(2, 5) and field[i][j + 1] in range(2,
                                                                                                                    5):
                    field[i][j] = field[i][j + 1]
                elif field[i + 1][j] in range(2, 5) and field[i - 1][j] in range(2, 5) and field[i][j - 1]:
                    field[i][j] = field[i][j - 1]
                elif field[i + 1][j] in range(2, 5) and field[i][j + 1] in range(2, 5) and field[i][j - 1]:
                    field[i][j] = field[i + 1][j]
                elif field[i - 1][j] in range(2, 5) and field[i][j + 1] in range(2, 5) and field[i][j - 1]:
                    field[i][j] = field[i - 1][j]


def building():
    count = 0

    g = [blocks.block['grass'].id, blocks.block['grass2'].id, blocks.block['grass3'].id]
    while count <= 3:
        i = random.randrange(10, 30)
        j = random.randrange(10, 40)

        i1 = random.randrange(30, 60)
        j1 = random.randrange(40, 90)

        i2 = random.randrange(30, 60)
        j2 = random.randrange(10, 40)

        i3 = random.randrange(10, 30)
        j3 = random.randrange(40, 90)
        if count == 3 and field[i3][j3 + 1] in g and field[i3][j3 - 1] in g and field[i3 - 1][j3] in g and \
                field[i3 + 1][j3] in g:
            buildings['fil'] = (j3, i3)
            count += 1
        if count == 2 and field[i2][j2 + 1] in g and field[i2][j2 - 1] in g and field[i2 - 1][j2] in g and \
                field[i2 + 1][j2] in g:
            buildings['obs'] = (j2, i2)
            count += 1
        if count == 1 and field[i][j + 1] in g and field[i][j - 1] in g and field[i - 1][j] in g and field[i + 1][
            j] in g:
            buildings['home2'] = (j, i)
            count += 1
        if count == 0 and field[i1][j1 + 1] in g and field[i1][j1 - 1] in g and field[i1 - 1][j1] in g and \
                field[i1 + 1][j1] in g:
            buildings['home1'] = (j1, i1)
            count += 1


def create_new_world():
    generate_terrain()
    gen_river()
    water_grow()
    gen_add()
    clear()
    gen_deep_dirt()
    gen_wall()
    building()
    return field

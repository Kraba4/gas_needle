import numpy
import blocks
import pygame
import motion

id_brain = blocks.block['brain'].id
id_empty = blocks.block['empty'].id
entity = []
entity_commands = dict()
id = 0
field = None


class EntityObject:
    def __init__(self, body, pos, owner, field1):
        global id, field
        self.body = numpy.array(body, 'int')
        self.size_y = len(body)
        self.size_x = len(body[0])
        self.pos = pos
        self.last = pos
        self.last_c = 0
        self.end_pos = pos
        if field is None:
            field = field1.copy()
        self.saved_bg = []
        self.finish = False
        self.draw_pos = pos
        self.brain = []

        self.finish_end = True
        self.owner = owner
        self.body_size = 0
        self.move = 0
        self.move_set = []
        self.next = (-1, -1)
        for i in range(self.size_y):
            for j in range(self.size_x):
                if self.body[i][j] == id_brain:
                    self.brain.append((i, j))
                    #break
        w = 1
        self.image = pygame.Surface((self.size_x * 10 + 2 * w, self.size_y * 10 + 2 * w), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 0))
        for i in range(self.size_y):
            for j in range(self.size_x):
                if self.body[i][j] != id_empty:
                    self.body_size += 1
                    self.image.blit(blocks.block[blocks.name_from_id[self.body[i][j]]].image, (j * 10 + w, i * 10 + w))
        for i in range(self.size_y):
            for j in range(self.size_x):
                if self.body[i][j] != id_empty:
                    if j + 1 >= self.size_x or self.body[i][j + 1] == id_empty:
                        pygame.draw.line(self.image, self.owner, ((j + 1) * 10 + w, i * 10 + w),
                                         ((j + 1) * 10 + w, (i + 1) * 10), w)
                    if j - 1 < 0 or self.body[i][j - 1] == id_empty:
                        pygame.draw.line(self.image, self.owner, ((j) * 10, i * 10 + w), ((j) * 10, (i + 1) * 10), w)
                    if i + 1 >= self.size_y or self.body[i + 1][j] == id_empty:
                        pygame.draw.line(self.image, self.owner, ((j) * 10 + w, (i + 1) * 10 + w),
                                         ((j + 1) * 10, (i + 1) * 10 + w), w)
                    if i - 1 < 0 or self.body[i - 1][j] == id_empty:
                        pygame.draw.line(self.image, self.owner, ((j) * 10 + w, (i) * 10), ((j + 1) * 10, (i) * 10), w)

    def update_move(self):

        if self.pos != self.end_pos:
            if self.next == (-1, -1):
                self.next = motion.make_path((self.size_x, self.size_y), self.pos, self.end_pos)
                self.next = self.next[len(self.next) - 2]
            self.move += 1
            self.draw_pos = (self.draw_pos[0] + (self.next[0] - self.draw_pos[0]) * (self.move / (self.body_size * 10)),
                             self.draw_pos[1] + (self.next[1] - self.draw_pos[1]) * (self.move / (self.body_size * 10)))
            if self.draw_pos == self.next:

                for i in range(self.size_y):
                    for j in range(self.size_x):
                        field[self.pos[1] + i][self.pos[0] + j] = self.saved_bg[i][j]
                self.pos = self.next
                self.move_set = motion.make_path((self.size_x, self.size_y), self.pos, self.end_pos)
                self.next = self.move_set[len(self.move_set) - 2]
                for i in range(self.size_y):
                    for j in range(self.size_x):
                        self.saved_bg[i][j] = field[self.pos[1] + i][self.pos[0] + j]
                for i in range(self.size_y):
                    for j in range(self.size_x):
                        field[self.pos[1] + i][self.pos[0] + j] = self.body[i][j]
                motion.update_field(field, (1, 1), (96, 60))
                self.move = 0
                if self.pos == self.last:
                    self.last_c += 1
                else:
                    self.last_c = 0
                self.last = self.pos
                if self.last_c == 5:
                    self.last_c = 0
                    self.end_pos = self.last
        else:
            self.move = 0

    def update_body(self):
        pass_brains = set()
        eq = []
        for b in self.brain:
            if b not in pass_brains:
                elems, brains = self.bfs(b[0], b[1])
                pass_brains = pass_brains.union(brains)
                body, pos = self.create_new_body(elems)
                for e in elems:
                    self.body[e[0]][e[1]] = id_empty
                eq.append(EntityObject(body, pos, self.owner, field))

        return self.body, eq

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
        new_body = numpy.ndarray((new_i, new_j))
        for i in range(new_i):
            for j in range(new_j):
                new_body[i][j] = id_empty

        for e in elems:
            new_body[e[0] - min_i][e[1] - min_j] = self.body[e[0]][e[1]]

        return new_body, (self.pos[0] + min_j, self.pos[1] + min_i)

    def bfs(self, i, j):
        que = []
        elems = []
        elems_bfs = numpy.array(self.body, 'int')
        for i1 in range(self.size_y):
            for j1 in range(self.size_x):
                elems_bfs[i1][j1] = 0
        brains = set()
        que.append((i, j))
        elems.append((i, j))
        elems_bfs[i][j] = 1
        while len(que) > 0:
            i, j = que.pop(0)

            if j + 1 < self.size_x and self.body[i][j + 1] != id_empty and elems_bfs[i][j + 1] == 0:
                que.append((i, j + 1))
                elems.append((i, j + 1))
                elems_bfs[i][j + 1] = 1
                if self.body[i][j + 1] == id_brain:
                    brains.add((i, j + 1))
            if j - 1 >= 0 and self.body[i][j - 1] != id_empty and elems_bfs[i][j - 1] == 0:
                que.append((i, j - 1))
                elems.append((i, j - 1))
                elems_bfs[i][j - 1] = 1
                if self.body[i][j - 1] == id_brain:
                    brains.add((i, j - 1))
            if i + 1 < self.size_y and self.body[i + 1][j] != id_empty and elems_bfs[i + 1][j] == 0:
                que.append((i + 1, j))
                elems.append((i + 1, j))
                elems_bfs[i + 1][j] = 1
                if self.body[i + 1][j] == id_brain:
                    brains.add((i + 1, j))
            if i - 1 >= 0 and self.body[i - 1][j] != id_empty and elems_bfs[i - 1][j] == 0:
                que.append((i - 1, j))
                elems.append((i - 1, j))
                elems_bfs[i - 1][j] = 1
                if self.body[i - 1][j] == id_brain:
                    brains.add((i - 1, j))

        return elems, brains

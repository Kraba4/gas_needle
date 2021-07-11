import numpy
import blocks
import p_queue
field_x = None
field_y = None


def init(height, width):
    global field_x
    global field_y
    field_x = numpy.ndarray((height, width), 'int')
    field_y = numpy.ndarray((height, width), 'int')

    for i in range(height):
        for j in range(width):
            field_x[i][j] = 0
            field_y[i][j] = 0


def update_field(field, point1, point2):
    g = [blocks.block['grass'].id, blocks.block['grass2'].id, blocks.block['grass3'].id, blocks.block['wall'].id, blocks.block['hill'].id,
         blocks.block['sand'].id]
    point1 = (max(point1[0]-12,1), max(point1[1]-12,1))

    for i in range(point2[1], point1[1] - 1, -1):
        last_x = (point2[0] + 1) + field_x[i][point2[0] + 1]
        for j in range(point2[0], point1[0] - 1, -1):
            if field[i][j] in g:
                field_x[i][j] = min(12, last_x - j)
            else:
                field_x[i][j] = 0
                last_x = j

    for j in range(point2[0], point1[0] - 1, -1):
        last_y = (point2[1] + 1) + field_y[point2[1] + 1][j]
        for i in range(point2[1], point1[1] - 1, -1):
            if field[i][j] in g:
                field_y[i][j] = min(12, last_y - i)
            else:
                field_y[i][j] = 0
                last_y = i


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def make_path(shape, start, end):
    frontier = p_queue.priority_queue()
    frontier.append(0,start)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0
    near = (heuristic(end, start), start)
    count = 0
    while frontier.empty():
        count +=1
        current = frontier.pop()[1]
        j, i = current
        if current == end:
            break
        if j+shape[0] <98 and field_x[i][j+shape[0]] != 0 and field_y[i][j+shape[0]] >= shape[1]:
            new_cost = cost_so_far[current] + 1
            f = (j+1,i)
            if f not in cost_so_far or new_cost < cost_so_far[f]:
                cost_so_far[f] = new_cost
                priority = new_cost + heuristic(end, f)
                frontier.append(-priority,f)
                came_from[f] = current
                if heuristic(end, f) < near[0]:
                    near = (heuristic(end, f), f)
        if field_x[i][j-1] != 0 and field_y[i][j-1] >= shape[1]:
        # другие направления
        # ...
            new_cost = cost_so_far[current] + 1
            f = (j-1,i)
            if f not in cost_so_far or new_cost < cost_so_far[f]:
                cost_so_far[f] = new_cost
                priority = new_cost + heuristic(end, f)
                frontier.append(-priority,f)
                came_from[f] = current
                if heuristic(end, f) < near[0]:
                    near = (heuristic(end, f), f)
        if field_y[i-1][j] != 0 and field_x[i-1][j] >= shape[0]:
            new_cost = cost_so_far[current] + 1
            f = (j,i-1)
            if f not in cost_so_far or new_cost < cost_so_far[f]:
                cost_so_far[f] = new_cost
                priority = new_cost + heuristic(end, f)
                frontier.append(-priority, f)
                came_from[f] = current
                if heuristic(end, f) < near[0]:
                    near = (heuristic(end, f), f)
        if i+shape[1] < 62 and field_y[i+shape[1]][j] != 0 and field_x[i+shape[1]][j] >= shape[0]:
            new_cost = cost_so_far[current] + 1
            f = (j,i+1)
            if f not in cost_so_far or new_cost < cost_so_far[f]:
                cost_so_far[f] = new_cost
                priority = new_cost + heuristic(end, f)
                frontier.append(-priority,f)
                came_from[f] = current
                if heuristic(end, f) < near[0]:
                    near = (heuristic(end, f), f)

    if end not in came_from:
        end = near[1]
    current = end
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    return path

import generation
import motion
import socket
import pickle
import blocks

blocks.init()
import entities


def trade_with_client():
    global field
    conn, addr = sock.accept()
    print('connected:', addr)
    data = conn.recv(32768)
    print(pickle.loads(data))
    if pickle.loads(
            data) == b'\x80\x04\x95/\x00\x00\x00\x00\x00\x00\x00]\x94(}\x94(\x8c\x01x\x94K\x1a\x8c\x01y\x94K\x0c\x8c\x05param\x94K u}\x94(h\x02K\x16h\x03K\x11h\x04K\x0bue.':
        print("qqqqqqq")
        conn.send(count_new_data(field))
        return
    print(data)
    temp = pickle.loads(data)
    print(temp)
    if temp[1] == 'get_field':
        return conn.send(count_new_data(field))
    elif temp[1] == 'get_entities':
        return conn.send(count_new_data(entities.entity))
    elif temp[1] == 'get_buildings':
        return conn.send(count_new_data(generation.buildings))
    elif temp[1] == 'give_field':
        field = temp[0]
        return conn.send(count_new_data(field))
    elif temp[1] == 'give_commands':
        for i in temp[0]:
            if i.owner == temp[2]:
                entities.entity_commands[i] = temp[0][i]
        return conn.send(count_new_data(field))
    elif temp[1] == 'give_entities':
        entities.entity.extend(temp[0])
        print(entities.entity)
        return conn.send(count_new_data(entities.entity))
    # if(data[0] == {'name':'stop'}):
    # print("stopped")
    # conn.send(bytes([255,255,255]))
    # conn.close()
    # return -1
    # else:
    conn.send(count_new_data(field))
    return 1


def count_new_data(data):
    a = pickle.dumps(field)
    return a


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 55000))
sock.listen(2)
field = generation.create_new_world()
entities.entity.append(entities.EntityObject([1, 1], (0, 0), "none", field))
print('Server is running, please, type stop() on client to stop')
while True:
    if (trade_with_client() == -1):
        break
sock.close()

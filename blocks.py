import pygame

block = dict()
name_from_id = ['obsidian', 'dirt', 'grass', 'grass2', 'grass3', 'hard_stone', 'medium_stone', 'stone', 'snow_stone',
                'wood', 'gas', 'fire', 'water', 'deep_water','deep_water2', 'sand', 'wall',
                'hill', 'deep_dirt', 'brain','philosof','empty', 'home1', 'home2', 'obs','button_up','button_down','button_erase',
                'button_fill','button_add', 'fil', 'leaves']
id_max = 0


class BlockObject:
    def __init__(self, src, durability, collide, size=(10,10)):
        global id_max
        if isinstance(src, str):
            self.image = pygame.image.load(src)
            self.color = self.image.get_at((4,5))

        else:
            self.image = pygame.Surface(size,pygame.SRCALPHA)
            self.image.fill(src)
            self.color = src
        self.durability = durability
        self.collide = collide
        self.id = id_max
        id_max += 1


def init():
    global block
    block['obsidian'] = BlockObject((0,0,0,255), 10, True)
    block['dirt'] = BlockObject((159, 99, 66,255), 1, False)
    block['grass'] = BlockObject((153, 204, 51,255), 1, False)
    block['grass2'] = BlockObject((149, 199, 50,255), 1, False)
    block['grass3'] = BlockObject((138, 184, 46,255), 1, False)
    block['hard_stone'] = BlockObject((127, 127, 127,255), 3, True)
    block['medium_stone'] = BlockObject((146, 146, 146,255), 3, True)
    block['stone'] = BlockObject((195, 195, 195,255), 3, True)
    block['snow_stone'] = BlockObject((255, 255, 255,255), 3, True)
    block['wood'] = BlockObject('tree.jpg', 2, True)
    block['gas'] = BlockObject((0, 255, 0,255), 1, False)
    block['fire'] = BlockObject('fire.png', 1, True)
    block['water'] = BlockObject((0, 162, 232,255), 1, False)
    block['deep_water'] = BlockObject((0, 146, 208,255), 1, True)
    block['deep_water2'] = BlockObject((0,139,199,255), 1, True)
    block['sand'] = BlockObject((232, 239, 88,255), 1, True)
    block['wall'] = BlockObject((124, 165, 41,255), 1, True)
    block['hill'] = BlockObject((127, 156, 127,255), 1, True)
    block['deep_dirt'] = BlockObject((131, 81, 54,255), 1, True)
    block['brain'] = BlockObject('brain.png', 1, True)
    block['philosof'] = BlockObject((255,50,255, 255), 1, True)
    block['empty'] = BlockObject((255,255,255, 0), 1, True)
    block['home1'] = BlockObject('wizardHouseBlue.png', 1, True, (10,20))
    block['home2'] = BlockObject('wizardHouseRed.png', 1, True, (10,20))
    block['obs'] = BlockObject('observatory.png', 1, True, (20, 20))
    block['button_up'] = BlockObject('arrowUp.jpg', 1, True, (140, 10))
    block['button_down'] = BlockObject('arrowDown.jpg', 1, True, (140, 10))
    block['button_erase'] = BlockObject('exitBold.jpg', 1, True, (10, 10))
    block['button_fill'] = BlockObject('fill.jpg', 1, True, (10, 10))
    block['button_add'] = BlockObject('plus.jpg', 1, True, (10, 10))
    block['fil'] = BlockObject('philosopherStone.png', 1, True, (20, 20))
    block['leaves'] = BlockObject('leaves.jpg', 1, True, (10, 10))
    block['empty'].image.fill((0,0,0))

    pygame.draw.rect(block['empty'].image, (100,100,100), ((3,3),(3,3)))


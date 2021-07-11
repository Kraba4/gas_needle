import palette


class Player:
    def __init__(self, name):
        self.name = name
        a = name.__hash__()
        self.color = (a % 256, (a + 100) % 256, (a + 200) % 256)
        self.image = palette.font.render(self.name, False, self.color)

    def draw(self, surface):
        surface.blit(self.image, (20, 20))

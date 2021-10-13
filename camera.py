import pygame


class Camera:
    """ Class that allows player to be followed by the camera """
    def __init__(self, screen_size, canvas_size, block_size):
        self.width, self.height = screen_size
        self.c_width, self.c_height = canvas_size
        self.block_size = block_size
        self.pos = {'x': self.c_width, 'y': self.c_height}
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = None
        self.update_rect()

    def update_rect(self):
        """ Function updating camera-rect position """
        temp_x = self.pos['x'] - self.width/2
        temp_y = self.pos['y'] - self.height/2

        if temp_x < 0:
            x = 0
        elif temp_x > (self.c_width - self.width):
            x = max(self.c_width - self.width, 0)
        else:
            x = temp_x

        if temp_y < 0:
            y = 0
        elif temp_y > (self.c_height - self.height):
            y = max(self.c_height - self.height, 0)
        else:
            y = temp_y

        w = min(self.c_width, self.width)
        h = min(self.c_height, self.height)

        self.rect = pygame.Rect(x, y, w, h)
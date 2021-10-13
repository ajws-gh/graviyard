from static_methods import *
from constants import *
import sprites
from player import Player


class Zombie:
    def __init__(self, x, y, start_x, end_x, height, width, go_left=True):
        self.x, self.y = x, y
        self.start_x, self.end_x = start_x, end_x
        self.height = height
        self.width = width
        self.sprite = S_WALK
        self.status = ZombieStatus(S_WALK, self)
        self.x_speed = 0
        self.delay = 0
        self.dead_time = 0
        self.go_left = go_left
        self.flipped = True
        self.zl, self.zr, self.zu = None, None, None
        self.resurrecting = False

    def update(self, delay, player: Player):
        self.delay = delay
        if not self.status.name == S_ZOMBIE_DEAD:
            self.update_zombie_dirs()
            if self.check_collision(player) == 'jump':
                return 'jump'
            elif self.check_collision(player) == 'die':
                return 'die'
            self.x += self.x_speed * delay
            if self.x <= self.start_x:
                self.go_left = False
                self.flipped = False
            elif self.x >= self.end_x:
                self.go_left = True
                self.flipped = True
        self.status.update(delay)

    def draw(self, screen, flipped=False):
        if self.resurrecting:
            new_index = (self.status.count - 1) - (self.status.index % self.status.count)
            if self.status.index == 4:
                new_index = self.status.index % self.status.count
                self.resurrecting = False
                self.status = ZombieStatus(S_WALK, self)
        else:
            new_index = self.status.index % self.status.count
        sprite_name = 'w_zombie/' + self.sprite + str(new_index)
        sprite = sprites.sprite.get_sprite(sprite_name, flipped)
        if 'zombie_dead' in sprite_name:
            screen.blit(sprite, (self.x, self.y + (50 - sprite.get_height())))
        else:
            screen.blit(sprite, (self.x, self.y))

    def update_zombie_dirs(self):
        d = 10
        self.zl = pygame.Rect(self.x, self.y + d, d, self.height - 2 * d)
        self.zr = pygame.Rect(self.x + self.width - d, self.y + d, d, self.height - 2 * d)
        self.zu = pygame.Rect(self.x - 1/2 * d, self.y, self.width + d, d)

    def check_collision(self, player: Player):
        d = 10
        if player.status.name == S_FALL:
            if player.y_speed >= 1000:
                block = pygame.Rect(player.x - d, player.y - 1/2 * player.height, player.width + d, 2 * player.height)
                self.zu = pygame.Rect(self.x - 1 / 2 * d, self.y - 1/2 * self.height, self.width + d, 3/2 * self.height)
                if block.colliderect(self.zu):
                    self.status = ZombieStatus(S_ZOMBIE_DEAD, self)
                    player.y = self.y
                    return 'jump'
            else:
                block = pygame.Rect(player.x - d, player.y + player.height - d, player.width + d, d)
            if block.colliderect(self.zu):
                self.status = ZombieStatus(S_ZOMBIE_DEAD, self)
                return 'jump'
            elif block.colliderect(self.zr) or block.colliderect(self.zl):
                return 'die'
        else:
            block = pygame.Rect(player.x + d, player.y + 1/2 * player.height, player.width - 2*d, 1/2 * player.width)
            if block.colliderect(self.zl) or block.colliderect(self.zr) or block.colliderect(self.zu):
                return 'die'


class ZombieStatus:
    def __init__(self, status_name: str, zombie: Zombie):
        self.name = status_name
        self.zombie = zombie
        self.block_size = None
        if self.name == S_WALK:
            self.index, self.count, self.elapsed = walk_props()
            self.zombie.sprite = S_WALK
            self.update = self.walk_update
        elif self.name == S_ZOMBIE_DEAD:
            self.index, self.count, self.elapsed = dead_props()
            self.zombie.sprite = S_ZOMBIE_DEAD
            self.update = self.dead_update

    def walk_update(self, delay):
        self.elapsed += delay
        if self.elapsed > 0.35:
            self.index += 1
            self.elapsed = 0
        if self.zombie.go_left:
            self.zombie.x_speed = - ZOMBIE_SPEED
        else:
            self.zombie.x_speed = ZOMBIE_SPEED

    def dead_update(self, delay):
        self.elapsed += delay
        if self.elapsed >= 4:
            self.index = 0
            self.zombie.resurrecting = True
        if self.elapsed > 0.5 and self.index < 4:
            self.index += 1
            self.elapsed = 0

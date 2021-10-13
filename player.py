from static_methods import *
from constants import *
import sprites


class Player:
    def __init__(self, x, y, width, height, block_size, blocks):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.sprite = S_FALL
        self.x_speed, self.y_speed = 0, 0
        self.delay = 0
        self.flipped = False
        self.block_size = block_size
        self.blocks = blocks
        self.pl, self.pd, self.pr, self.pu = None, None, None, None
        self.right_pressed, self.left_pressed = False, False
        self.jump_time = 0
        self.fall_time = 0
        self.status = Status(S_FALL, self)
        self.zombies_positions = []

    def keyboard(self, keys):
        self.right_pressed = bool(keys[pygame.K_RIGHT])
        self.left_pressed = bool(keys[pygame.K_LEFT])
        self.status.keyboard(keys)
        if self.left_pressed:
            self.flipped = True
            self.x_speed = -MOVE_SPEED
        if self.right_pressed:
            self.flipped = False
            self.x_speed = MOVE_SPEED
        if not self.right_pressed and not self.left_pressed:
            self.x_speed = 0

    def update(self, delay):
        self.delay = delay
        self.y += self.y_speed * delay
        self.update_player_dirs()
        self.x += self.x_speed * delay
        self.status.update(self.delay)
        self.get_possible_collision_blocks()

    def draw(self, screen, flipped=False):
        new_index = self.status.index % self.status.count
        sprite_name = self.sprite + str(new_index)
        sprite = sprites.sprite.get_sprite(sprite_name, flipped)
        screen.blit(sprite, (self.x, self.y))

    def get_player_cols(self):
        x = int(self.x / self.block_size)
        w = int(self.width / self.block_size) + 1
        col_min = x - 1
        col_max = x + w + 1
        return col_min, col_max

    def get_possible_collision_blocks(self):
        col_min, col_max = self.get_player_cols()
        blocks = []
        for key in self.blocks.keys():
            if col_min <= key <= col_max:
                for block in self.blocks[key]:
                    if any([(block[-2], block[-1]) == pos for pos in self.zombies_positions]):
                        continue
                    blocks.append(block)
        return blocks

    def update_blocks(self, blocks):
        self.blocks = blocks

    def update_player_dirs(self):
        d = 10
        self.pl = pygame.Rect(self.x, self.y + d, d, self.height - 2 * d)
        self.pd = pygame.Rect(self.x + d, self.y + self.height - d, self.width - 2 * d, d)
        self.pr = pygame.Rect(self.x + self.width - d, self.y + d, d, self.height - 2 * d)
        self.pu = pygame.Rect(self.x + d, self.y, self.width - 2 * d, d)

    def get_zombies_pos(self):
        for key in self.blocks.keys():
            for item in self.blocks[key]:
                if item[0] == 'zombie':
                    self.zombies_positions.append((item[-2], item[-1] + 1))
                    continue


# noinspection PyGlobalUndefined
class Status:
    def __init__(self, status_name: str, player: Player):
        self.name = status_name
        self.player = player
        self.block_size = player.block_size
        if self.name == S_IDLE:
            self.index, self.count, self.elapsed = idle_props()
            self.player.sprite = S_IDLE
            self.keyboard = self.idle_keyboard
            self.update = self.idle_update
        if self.name == S_FALL:
            player.fall_time = 0
            self.index, self.count, self.elapsed = fall_props()
            self.player.sprite = S_FALL
            self.keyboard = self.fall_keyboard
            self.update = self.fall_update
            self.add_gravity = 0
        if self.name == S_RUN:
            self.index, self.count, self.elapsed = run_props()
            self.player.sprite = S_RUN
            self.keyboard = self.run_keyboard
            self.update = self.run_update
        if self.name == S_JUMP:
            player.jump_time = 0
            self.index, self.count, self.elapsed = jump_props()
            self.player.sprite = S_JUMP
            self.keyboard = self.jump_keyboard
            self.update = self.jump_update
        self.elapsed = 0
        self.block_under_player = [0, -1]
        self.block_right_player = [-1, 0]
        self.block_up_player = [0, 1]
        self.block_left_player = [1, 0]

    def idle_keyboard(self, keys):
        if keys[pygame.K_UP]:
            if config.sounds_on[0] == 'On':
                config.jump_sound.play()
            self.player.status = Status(S_JUMP, self.player)
            self.player.y_speed = -JUMP_SPEED
        elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.player.status = Status(S_RUN, self.player)

    def idle_update(self, delay):
        self.elapsed += delay
        if self.elapsed > 0.05:
            self.index += 1
            self.elapsed = 0
        collision, block = self.check_collision(self.block_under_player, self.player.pd)
        if not collision:
            self.player.y_speed = 10
            self.player.status = Status(S_FALL, self.player)

    def fall_keyboard(self, keys):
        if keys[pygame.K_DOWN]:
            self.add_gravity = GRAVITY
        else:
            self.add_gravity = 0

    def fall_update(self, delay):
        if self.player.left_pressed:
            self.common_left_update(self.player.pl)
        elif self.player.right_pressed:
            self.common_right_update(self.player.pr)
        self.player.fall_time += delay
        self.player.y_speed = (FALL_GRAVITY + self.add_gravity) * self.player.fall_time
        self.elapsed += delay
        if self.elapsed > 0.05:
            self.index += 1
            self.elapsed = 0
        collision, block = self.check_collision(self.block_under_player, self.player.pd)
        if collision:
            self.player.y_speed = 0
            self.player.y = block[-1] * self.player.block_size - self.player.height
            self.player.status = Status(S_IDLE, self.player)

    def run_keyboard(self, keys):
        if keys[pygame.K_UP]:
            if config.sounds_on[0] == 'On':
                config.jump_sound.play()
            self.player.status = Status(S_JUMP, self.player)
            self.player.y_speed = -JUMP_SPEED
        if not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.player.status = Status(S_IDLE, self.player)

    def run_update(self, delay):
        if self.player.left_pressed:
            self.common_left_update(self.player.pl)
        elif self.player.right_pressed:
            self.common_right_update(self.player.pr)
        self.elapsed += delay
        if self.elapsed > 0.05:
            self.index += 1
            self.elapsed = 0
        collision, block = self.check_collision(self.block_under_player, self.player.pd)
        if not collision:
            self.player.y_speed = 10
            self.player.status = Status(S_FALL, self.player)

    def jump_keyboard(self, keys):
        if keys[pygame.K_DOWN]:
            self.player.y_speed = 0
            self.player.status = Status(S_FALL, self.player)

    def jump_update(self, delay):
        if self.player.left_pressed:
            self.common_left_update(self.player.pl)
        elif self.player.right_pressed:
            self.common_right_update(self.player.pr)
        self.player.jump_time += delay
        self.elapsed += delay
        if self.elapsed > 0.05:
            self.index += 1
            self.elapsed = 0
        collision, block = self.check_collision(self.block_up_player, self.player.pu)
        self.player.y_speed = -JUMP_SPEED + (GRAVITY**2 * self.player.jump_time) / 140

        if collision or self.player.y_speed > 0:
            if collision:
                self.player.y = block[-1] * self.player.block_size + self.player.block_size
            self.player.y_speed = 0
            self.player.status = Status(S_FALL, self.player)

    def check_collision(self, side_block, p_rect):
        global block_rect
        blocks = self.player.get_possible_collision_blocks()
        for block in blocks:
            name, collision, overflow_x, overflow_y, curr_x, curr_y = block
            if self.player.y_speed >= 1500:
                for i in range(1, 5):
                    if name == 'zombie':
                        block_rect = pygame.Rect(curr_x * self.player.block_size + overflow_x,
                                                 (curr_y + i) * self.player.block_size + 6 + overflow_y,
                                                 self.player.block_size, self.player.block_size)
                    else:
                        block_rect = pygame.Rect(curr_x * self.player.block_size + side_block[0] + overflow_x,
                                                 (curr_y + i) * self.player.block_size + overflow_y,
                                                 self.player.block_size, self.player.block_size)
                    if p_rect.colliderect(block_rect):
                        if collision:
                            collision()
                            return False, None
                        return True, block
            elif self.player.y_speed <= -1500:
                for i in range(1, 5):
                    if name == 'zombie':
                        block_rect = pygame.Rect(curr_x * self.player.block_size + overflow_x,
                                                 (curr_y - i) * self.player.block_size + 6 + overflow_y,
                                                 self.player.block_size, self.player.block_size)
                    else:
                        block_rect = pygame.Rect(curr_x * self.player.block_size + side_block[0] + overflow_x,
                                                 (curr_y - i) * self.player.block_size + overflow_y,
                                                 self.player.block_size, self.player.block_size)
                    if p_rect.colliderect(block_rect):
                        if collision:
                            collision()
                            return False, None
                        return True, block
            else:
                if name == 'zombie':
                    block_rect = pygame.Rect(curr_x * self.player.block_size + overflow_x,
                                             curr_y * self.player.block_size + 6 + overflow_y,
                                             self.player.block_size, self.player.block_size)

                else:
                    block_rect = pygame.Rect(curr_x * self.player.block_size + side_block[0] + overflow_x,
                                             (curr_y + side_block[1]) * self.player.block_size + overflow_y,
                                             self.player.block_size, self.player.block_size)
            if p_rect.colliderect(block_rect):
                if collision:
                    collision()
                    return False, None
                return True, block
        return False, None

    def common_left_update(self, p_rect):
        collision, block = self.check_collision(self.block_left_player, p_rect)
        if collision:
            self.player.x_speed = 0
            self.player.x = block[-2] * self.block_size + self.block_size
            return block

    def common_right_update(self, p_rect):
        collision, block = self.check_collision(self.block_right_player, p_rect)
        if collision:
            self.player.x_speed = 0
            self.player.x = block[-2] * self.block_size - self.player.width
            return block

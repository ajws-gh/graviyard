import json
from random import randint
from static_methods import *
from constants import *
from camera import Camera
from player import Player, Status
from zombie import Zombie, ZombieStatus
import sprites

pygame.init()

pygame.mouse.set_visible(False)
pygame.mixer.init()


# noinspection PyGlobalUndefined
class Game:
    def __init__(self):
        # Screen
        self.screen = pygame.display.set_mode((config.width, config.height), config.screen_type)
        self.bg_width, self.bg_height = config.bg_sprite.get_size()
        self.how_many_bgs = 1
        self.tops = dict()

        # Level&Game
        self.level_cols = None
        self.level_rows = None
        self.block_size = None
        self.player_start_x, self.player_start_y, self.y_speed, self.x_speed = 0, 0, 0, 0
        self.player = None
        self.running = True
        self.score = 0
        self.pause = False

        # Zombies
        self.zombies_positions = []
        self.zombies = list()
        self.zombie_start_x, self.zombie_start_y = 0, 0
        self.zombies_start_pos = []

        # Time
        self.clock = pygame.time.Clock()
        self.time = 999
        self.level_time = 999
        self.delay = 0

        # Camera
        self.camera = None
        self.canvas = None
        self.blocks = dict()

    def start(self):
        """ Main loop """
        while self.running:
            self.screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if adding_user():
                        # Setting up player's nickname
                        play_sound('type')
                        menu.append_to_name(event.key)
                    elif event.key == pygame.K_p and config.game_started:
                        play_sound('select')
                        self.pause = not self.pause
                    elif event.key == pygame.K_r and config.game_started:
                        play_sound('level_up')
                        self.restart()
                    elif event.key == pygame.K_n and config.game_started:
                        self.level_up()
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        play_sound('select')
                        if not menu.settings_active:
                            # Escape key action while none setting is activated
                            if not menu.draw == menu.draw_menu:
                                menu.index = 0
                            menu.score = 0
                            menu.score_updated = False
                            menu.draw = menu.draw_menu
                            # While game is started
                            if config.game_started:
                                config.game_started = False
                                self.pause = False
                                config.current_level = config.entry_level

                        else:
                            # Escape key action while any setting is activated, it restores active setting to the
                            # previous version
                            menu.settings_active = False
                            if menu.index % 6 == 0:
                                menu.is_fullscreen = config.is_fullscreen
                            elif menu.index % 6 == 1:
                                menu.res_index = config.resolution[1]
                            elif menu.index % 6 == 2:
                                menu.max_fps = config.max_fps
                            elif menu.index % 6 == 3:
                                menu.current_level = config.entry_level
                            elif menu.index % 6 == 4:
                                menu.music_on = config.music_on
                            elif menu.index % 6 == 5:
                                menu.sounds_on = config.sounds_on

                    # Navigating the menu
                    # K_DOWN
                    elif event.key == pygame.K_DOWN and arrows_up_down_condition():
                        play_sound('arrow_sound')
                        menu.index += 1

                    # K_UP
                    elif event.key == pygame.K_UP and arrows_up_down_condition():
                        play_sound('arrow_sound')
                        menu.index -= 1

                    # K_LEFT
                    elif event.key == pygame.K_LEFT and arrows_l_r_condition():
                        # Navigating Left/Right the settings menu
                        play_sound('arrow_sound')
                        if menu.draw == menu.draw_how_to_play:
                            menu.lr_index -= 1
                        else:
                            inc_dec_lr_indexes('-')

                    # K_RIGHT
                    elif event.key == pygame.K_RIGHT and arrows_l_r_condition():
                        # Navigating Left/Right the settings menu
                        play_sound('arrow_sound')
                        if menu.draw == menu.draw_how_to_play:
                            menu.lr_index += 1
                        else:
                            inc_dec_lr_indexes('+')

                    # ENTER

                    elif event.key == pygame.K_RETURN:
                        # Navigating the settings menu - choosing options and changing them
                        if menu.draw == menu.draw_settings:
                            play_sound('select')
                            if not menu.settings_active:
                                menu.settings_active = True
                                menu.level_index = config.entry_level
                                menu.music_index = menu.music_on[1]
                                menu.sound_index = menu.sounds_on[1]
                            else:
                                if menu.index % 6 == 0:
                                    config.is_fullscreen = menu.is_fullscreen
                                    config.screen_type = config.fullscreen if config.is_fullscreen[0] else \
                                        config.window_screen
                                    config.save_settings_to_file('fullscreen')
                                    self.update_screen()
                                elif menu.index % 6 == 1:
                                    if menu.selected_resolution == 'Automatic':
                                        config.width = config.monitor.width
                                        config.height = config.monitor.height
                                        config.resolution = ['Automatic', 0]
                                        config.save_settings_to_file('resolution', 0)
                                    else:
                                        config.width = menu.selected_resolution[0]
                                        config.height = menu.selected_resolution[1]
                                        config.resolution = [config.width, config.height], menu.res_index
                                        config.save_settings_to_file('resolution', menu.res_index)
                                    config.update_screen_vars()
                                    self.update_screen()
                                elif menu.index % 6 == 2:
                                    config.max_fps = menu.max_fps
                                    config.save_settings_to_file('fps')
                                elif menu.index % 6 == 3:
                                    config.current_level = menu.current_level
                                    config.entry_level = menu.current_level
                                elif menu.index % 6 == 4:
                                    config.music_on = menu.music_on
                                    if config.music_on[0] == 'On':
                                        pygame.mixer.music.play(-1)
                                    elif config.music_on[0] == 'Off':
                                        pygame.mixer.music.stop()
                                    config.save_settings_to_file('music', menu.music_index)
                                elif menu.index % 6 == 5:
                                    config.sounds_on = menu.sounds_on
                                    config.save_settings_to_file('sounds', menu.sound_index)
                                menu.settings_active = False

                        if is_menu():
                            # Starts the game
                            if menu.index % 6 == 0:
                                play_sound('select')
                                self.load(str(config.entry_level).zfill(3))
                                config.game_started = True

                            # Enters how to play section
                            elif menu.index % 6 == 1:
                                play_sound('select')
                                menu.lr_index = 0
                                menu.draw = menu.draw_how_to_play

                            # Enters settings
                            elif menu.index % 6 == 2:
                                play_sound('select')
                                menu.index = 0
                                menu.draw = menu.draw_settings

                            # Enters credits
                            elif menu.index % 6 == 3:
                                play_sound('select')
                                menu.draw = menu.draw_credits

                            # Enters top scores
                            elif menu.index % 6 == 4:
                                play_sound('select')
                                menu.draw = menu.draw_top_scores

                            # Exit Game
                            elif menu.index % 6 == 5:
                                play_sound('select')
                                self.running = False

            if config.game_started:

                camera_x = follow(self.camera.pos['x'], self.player.x, 4 * self.delay)
                camera_y = follow(self.camera.pos['y'], self.player.y, 4 * self.delay)

                self.camera.pos["x"] = camera_x
                self.camera.pos["y"] = camera_y
                self.camera.update_rect()

                self.draw_blocks()

                for zombie in self.zombies:
                    if not self.pause:
                        if zombie.update(self.delay, self.player) == 'jump':
                            play_sound('hit_sound')
                            self.time += 1
                            self.player.status = Status(S_JUMP, self.player)
                            self.player.y_speed = -4 * JUMP_SPEED
                        elif zombie.update(self.delay, self.player) == 'die':
                            self.restart()
                    zombie.draw(self.canvas, zombie.flipped)

                if not self.pause:
                    self.player.keyboard(pygame.key.get_pressed())
                    self.player.update(self.delay)
                    time_left = config.time_font.render(f'TIME LEFT: {self.time:2.2f}', True, RED)
                    self.score = menu.score + (self.level_time - self.time)
                    score = config.time_font.render(f'SCORE: {self.score:2.2f}', True, RED)
                    self.time -= self.delay

                self.player.draw(self.canvas, self.player.flipped)
                self.camera.surface.blit(self.canvas.subsurface(self.camera.rect), (0, 0))
                self.camera.surface.blit(time_left, (0, 0))
                self.camera.surface.blit(score, (self.screen.get_width() - score.get_width(), 0))
                if self.pause:
                    self.camera.surface.blit(config.pause_sign, ((self.screen.get_width() -
                    config.pause_sign.get_width()) / 2, (self.screen.get_height() - config.pause_sign.get_height())/2))
                self.screen.blit(pygame.transform.smoothscale(self.camera.surface, (config.width, config.height)),
                                 (0, 0))
                pygame.draw.rect(self.canvas, BG_COLOR, self.camera.rect, 0)

                for i in range(self.how_many_bgs):
                    self.canvas.blit(config.bg_sprite, (i * self.bg_width, 0))

                if self.time < 0:
                    self.restart()
                self.check_player_position()

            else:
                menu.update()
                menu.draw()
            self.delay = self.clock.tick(config.max_fps) / 1000
            pygame.display.update()

    def update_screen(self):
        """ Updates items size after screen resolution or type is changed """
        config.menu_bg = pygame.image.load('images/menu_bg.png')
        config.menu_bg = pygame.transform.scale(config.menu_bg, (config.width, config.height))
        config.red_right_arrow = sprites.sprite.get_sprite('red_arrow')
        config.red_left_arrow = sprites.sprite.get_sprite('red_arrow', True)
        config.red_right_arrow = pygame.transform.scale(config.red_right_arrow, (int(72 * config.scale[0]),
                                                                                 int(50 * config.scale[1])))
        config.red_left_arrow = pygame.transform.scale(config.red_left_arrow, (int(72 * config.scale[0]),
                                                                               int(50 * config.scale[1])))
        config.yellow_right_arrow = sprites.sprite.get_sprite('yellow_arrow')
        config.yellow_left_arrow = sprites.sprite.get_sprite('yellow_arrow', True)
        config.yellow_right_arrow = pygame.transform.scale(config.yellow_right_arrow, (int(150 * config.scale[0]),
                                                                                       int(114 * config.scale[1])))
        config.yellow_left_arrow = pygame.transform.scale(config.yellow_left_arrow, (int(150 * config.scale[0]),
                                                                                     int(114 * config.scale[1])))
        config.how_to_restart = sprites.sprite.get_sprite('how_to_restart')
        config.how_to_restart = pygame.transform.scale(config.how_to_restart,
                                                       (int(config.width * 0.7291), int(config.height * 0.7268)))
        config.how_to_pause = sprites.sprite.get_sprite('how_to_pause')
        config.how_to_pause = pygame.transform.scale(config.how_to_pause,
                                                     (int(config.width * 0.7291), int(config.height * 0.7268)))
        config.how_to_escape = sprites.sprite.get_sprite('how_to_escape')
        config.how_to_escape = pygame.transform.scale(config.how_to_escape,
                                                      (int(config.width * 0.7291), int(config.height * 0.7268)))
        config.how_to_attack_move = sprites.sprite.get_sprite('how_to_attack_move')
        config.how_to_attack_move = pygame.transform.scale(config.how_to_attack_move,
                                                           (int(config.width * 0.7291), int(config.height * 0.7268)))
        self.screen = pygame.display.set_mode((config.width, config.height), config.screen_type)
        menu.screen = pygame.display.set_mode((config.width, config.height), config.screen_type)

    def load(self, level_str):
        self.zombies = list()
        self.blocks = dict()
        self.tops = dict()
        menu.scores = dict()
        menu.place = -1
        with open(f"levels/{level_str}.json", "r") as file:
            level = json.load(file)
        self.level_cols = level["cols"]
        self.level_rows = level["rows"]
        self.block_size = level["block_size"]
        self.level_time = self.time = level['time']
        self.player_start_x, self.player_start_y = level["start"]["player_x"], level["start"]["player_y"]
        self.zombies_start_pos = level["start"]["zombies"]
        level_width = self.level_cols * self.block_size
        level_height = self.level_rows * self.block_size
        self.canvas = pygame.Surface((level_width, level_height))
        self.how_many_bgs = level_width // self.bg_width + 1
        self.player = Player(self.player_start_x, self.player_start_y, 32, 50, block_size=self.block_size, blocks=None)
        for zombie in self.zombies_start_pos:
            self.zombies.append(Zombie(zombie[0], zombie[1], zombie[2], zombie[3], 50, 32, zombie[4]))
        self.camera = Camera(self.screen.get_size(), self.canvas.get_size(), self.block_size)
        self.camera.update_rect()
        self.camera.pos["x"] = self.player.x
        self.camera.pos["y"] = self.player.y
        json_blocks = level["blocks"]
        for block in json_blocks:
            self.add_block(block)
        self.player.update_blocks(self.blocks)
        self.player.get_zombies_pos()
        self.generate_tops()

    def restart(self):
        self.time = self.level_time
        self.player.x = self.player_start_x
        self.player.y = self.player_start_y
        self.player.x_speed = self.x_speed
        self.player.y_speed = self.y_speed
        self.player.status = Status(S_FALL, self.player)
        if config.current_level == 1:
            menu.score = 0
        for zombie, start_pos in zip(self.zombies, self.zombies_start_pos):
            zombie.status = ZombieStatus(S_WALK, zombie)
            zombie.x, zombie.y = start_pos[0], start_pos[1]

    def level_up(self):
        config.current_level += 1
        menu.score = self.score
        try:
            self.load(str(config.current_level).zfill(3))
            play_sound('level_up')
        except FileNotFoundError:
            config.game_started = False
            config.current_level = config.entry_level
            menu.score = round(menu.score, 2)
            menu.update_top_scores()
            menu.draw = menu.draw_top_scores

    def generate_tops(self):
        """Generate proper and random positions for static objects such as signs, skeletons..."""
        possible_places = []
        certain_places = []
        for col in self.blocks.keys():
            for block in self.blocks[col]:
                if block[0].startswith("tile_top"):
                    possible_places.append(block)
        pos_len = len(possible_places)

        for i in range(pos_len):
            for j in range(i + 1, pos_len):
                for k in range(j + 1, pos_len):
                    if not (any([block[0] == 'zombie' for block in self.blocks[possible_places[i][-2]]]) or any(
                            [block[0] == 'zombie' for block in self.blocks[possible_places[j][-2]]]) or
                            any([block[0] == 'zombie' for block in self.blocks[possible_places[k][-2]]])):
                        if (possible_places[i][-2] + 1 == possible_places[j][-2] and possible_places[i][-1] ==
                            possible_places[j][-1]) and (
                                possible_places[j][-2] + 1 == possible_places[k][-2] and possible_places[j][-1] ==
                                possible_places[k][-1]) and \
                                randint(1, 100) % 5 == 0:
                            certain_places.append((possible_places[i], 3))
                            break
                if not (any([block[0] == 'zombie' for block in self.blocks[possible_places[i][-2]]]) or any(
                        [block[0] == 'zombie' for block in self.blocks[possible_places[j][-2]]])):
                    if (possible_places[i][-2] + 1 == possible_places[j][-2] and possible_places[i][-1] ==
                        possible_places[j][-1]) and \
                            randint(1, 100) % 5 == 0:
                        certain_places.append((possible_places[i], 2))
                        break

        for block, how_many_blocks in certain_places:
            image_name = 'randomstuff' + str(randint(0, 10))
            image_path = 'images/' + image_name + '.png'
            image = pygame.image.load(image_path)
            image_blocks = (image.get_size()[0] // self.block_size) + 1
            if image_blocks <= how_many_blocks:
                self.tops[block] = image_name

    def add_block(self, block):
        name, x, y, w, h = block["name"], block["x"], block["y"], block["w"], block["h"]
        collision = block['collision'] if 'collision' in block else None
        if collision == 'die':
            collision = self.restart
        if collision == 'win':
            collision = self.level_up
        overflow_x = block['overflow_x'] if 'overflow_x' in block else 0
        overflow_y = block['overflow_y'] if 'overflow_y' in block else 0
        for row in range(h):
            for col in range(w):
                curr_x = x + col
                curr_y = y + row
                if curr_x not in self.blocks.keys():
                    self.blocks[curr_x] = list()
                self.blocks[curr_x].append((name, collision, overflow_x, overflow_y, curr_x, curr_y))

    def draw_blocks(self):
        for block_tuple, sprite_name in self.tops.items():
            name, collision, overflow_x, overflow_y, curr_x, curr_y = block_tuple
            x = curr_x * self.block_size + overflow_x
            y = (curr_y - 1) * self.block_size + overflow_y
            block_sprite = sprites.sprite.get_sprite(sprite_name)
            self.canvas.blit(block_sprite, (x, y))

        for col in self.blocks.keys():
            for block_tuple in self.blocks[col]:
                name, collision, overflow_x, overflow_y, curr_x, curr_y = block_tuple
                x = curr_x * self.block_size + overflow_x
                y = curr_y * self.block_size + overflow_y
                block_sprite = sprites.sprite.get_sprite(name)
                self.canvas.blit(block_sprite, (x, y))

    def check_player_position(self):
        """Checks if player is still in game boundaries"""
        canvas_w, canvas_h = self.canvas.get_size()
        if self.player.x > canvas_w:
            self.restart()
        elif self.player.y > canvas_h:
            self.restart()
        elif self.player.x + self.player.width < 0:
            self.restart()


instance = Game()

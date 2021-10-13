import json
import pygame
from screeninfo import get_monitors
import sprites

pygame.font.init()
pygame.mixer.init()


class Config:
    """ Game settings class """
    def __init__(self):
        with open("config/conf.json", "r") as file:
            self.config = json.load(file)

        # Screen
        self.resolution = self.config["screen"]['resolution']
        self.monitor = get_monitors()[0]
        if self.resolution[0] == 'Automatic':
            self.width = self.monitor.width
            self.height = self.monitor.height
        else:
            self.width = self.resolution[0][0]
            self.height = self.resolution[0][1]
        self.is_fullscreen = self.config["screen"]["fullscreen"]
        self.max_fps = self.config["settings"]["max_fps"]
        self.fullscreen = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        self.window_screen = pygame.HWSURFACE | pygame.DOUBLEBUF
        self.screen_type = self.fullscreen if self.is_fullscreen else self.window_screen
        self.screen = pygame.display.set_mode((self.width, self.height), self.screen_type)
        self.scale = (self.width / 1920), (self.height / 1080)

        # FONTS
        self.credits_font_path = self.config["font"]["credits_path"]
        self.text_font_path = self.config["font"]["text_path"]
        self.title_font_path = self.config["font"]["title_path"]
        self.title_font_size = int(self.height / 6)
        self.time_font_size = int(self.height / 36)
        self.menu_font_size = int(self.height / 21.6)
        self.top_scores_font_size = int(self.height / 31)
        self.credits_font_size = int(self.height / 41)
        self.top_scores_header_font_size = int(self.height / 20)
        self.time_font = pygame.font.Font(self.text_font_path, self.time_font_size)
        self.top_scores_font = pygame.font.Font(self.text_font_path, self.top_scores_font_size)
        self.top_scores_header_font = pygame.font.Font(self.text_font_path, self.top_scores_header_font_size)
        self.title_font = pygame.font.Font(self.title_font_path, self.title_font_size)
        self.credits_font = pygame.font.Font(self.credits_font_path, self.credits_font_size)
        self.menu_font = pygame.font.Font(self.text_font_path, self.menu_font_size)
        self.credits_font.set_bold(True)
        self.menu_font.set_italic(True)
        self.title_font.set_italic(True)

        # Music&Sounds
        self.music_path = self.config['music_path']
        self.music_on = self.config["settings"]['music_on']
        self.sounds_on = self.config["settings"]['sounds_on']
        self.arrow_sound = pygame.mixer.Sound('sounds/arrow.wav')
        self.arrow_sound.set_volume(0.1)
        self.hit_sound = pygame.mixer.Sound('sounds/hit.wav')
        self.hit_sound.set_volume(0.4)
        self.select_sound = pygame.mixer.Sound('sounds/select.wav')
        self.select_sound.set_volume(0.5)
        self.level_up_sound = pygame.mixer.Sound('sounds/level_up.wav')
        self.level_up_sound.set_volume(0.1)
        self.type_sound = pygame.mixer.Sound('sounds/type.wav')
        self.jump_sound = pygame.mixer.Sound('sounds/jump.wav')
        self.jump_sound.set_volume(0.1)
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.set_volume(0.1)
        if self.music_on[0] == 'On':
            pygame.mixer.music.play(-1)

        # Level
        self.current_level = self.entry_level = self.config["settings"]['entry_level']
        self.game_started = False

        # Menu
        self.menu_bg = pygame.image.load('images/menu_bg.png')
        self.menu_bg = pygame.transform.scale(self.menu_bg, (self.width, self.height))

        # BG & Pause IMG
        self.bg_sprite = sprites.sprite.get_sprite('BG')
        self.pause_sign = sprites.sprite.get_sprite('pause')

        # How to images
        self.how_to_restart = sprites.sprite.get_sprite('how_to_restart')
        self.how_to_restart = pygame.transform.scale(self.how_to_restart,
                                                     (int(self.width * 0.7291), int(self.height * 0.7268)))
        self.how_to_pause = sprites.sprite.get_sprite('how_to_pause')
        self.how_to_pause = pygame.transform.scale(self.how_to_pause,
                                                   (int(self.width * 0.7291), int(self.height * 0.7268)))

        self.how_to_escape = sprites.sprite.get_sprite('how_to_escape')
        self.how_to_escape = pygame.transform.scale(self.how_to_escape,
                                                    (int(self.width * 0.7291), int(self.height * 0.7268)))

        self.how_to_attack_move = sprites.sprite.get_sprite('how_to_attack_move')
        self.how_to_attack_move = pygame.transform.scale(self.how_to_attack_move,
                                                         (int(self.width * 0.7291), int(self.height * 0.7268)))

        # Menu arrows
        self.red_right_arrow = sprites.sprite.get_sprite('red_arrow')
        self.red_left_arrow = sprites.sprite.get_sprite('red_arrow', True)
        self.red_right_arrow = pygame.transform.scale(self.red_right_arrow, (int(72 * self.scale[0]),
                                                                             int(50 * self.scale[1])))
        self.red_left_arrow = pygame.transform.scale(self.red_left_arrow, (int(72 * self.scale[0]),
                                                                           int(50 * self.scale[1])))
        self.yellow_right_arrow = sprites.sprite.get_sprite('yellow_arrow')
        self.yellow_left_arrow = sprites.sprite.get_sprite('yellow_arrow', True)
        self.yellow_right_arrow = pygame.transform.scale(self.yellow_right_arrow, (int(150 * self.scale[0]),
                                                                                   int(114 * self.scale[1])))
        self.yellow_left_arrow = pygame.transform.scale(self.yellow_left_arrow, (int(150 * self.scale[0]),
                                                                                 int(114 * self.scale[1])))

        # Text positions
        self.text_pos = self.width * (3 / 5)
        self.menu_start_y = self.height / 3
        self.menu_y_space = self.height / 11
        self.space = self.menu_font_size
        self.y_const = self.height / 11
        self.starting_y_pos = self.height / 3.6
        self.width_tenth = self.width / 10

    def save_settings_to_file(self, setting, index=None):
        """ Saves game settings to 'config.json' file """
        if setting == 'resolution':
            if self.resolution[0] == 'Automatic':
                self.config["screen"]["resolution"] = ['Automatic', 0]
            else:
                self.config["screen"]["resolution"] = [[self.resolution[0][0], self.resolution[0][1]], index]
        elif setting == 'music':
            self.config["settings"]["music_on"] = [self.music_on[0], index]
        elif setting == 'sounds':
            self.config["settings"]["sounds_on"] = [self.sounds_on[0], index]
        elif setting == 'fps':
            self.config["settings"]["max_fps"] = self.max_fps
        elif setting == 'fullscreen':
            self.config["screen"]["fullscreen"] = self.is_fullscreen

        with open('config/conf.json', 'w') as file:
            json.dump(self.config, file, indent=4)

    def update_screen_vars(self):
        """ Updates scalable items size once screen type or resolution is changed """
        self.title_font_size = int(self.height / 6)
        self.time_font_size = int(self.height / 36)
        self.menu_font_size = int(self.height / 21.6)
        self.top_scores_font_size = int(self.height / 31)
        self.top_scores_header_font_size = int(self.height / 20)
        self.credits_font_size = int(self.height / 41)
        self.time_font = pygame.font.Font(self.text_font_path, self.time_font_size)
        self.top_scores_font = pygame.font.Font(self.text_font_path, self.top_scores_font_size)
        self.title_font = pygame.font.Font(self.title_font_path, self.title_font_size)
        self.credits_font = pygame.font.Font(self.credits_font_path, self.credits_font_size)
        self.menu_font = pygame.font.Font(self.text_font_path, self.menu_font_size)
        self.top_scores_header_font = pygame.font.Font(self.text_font_path, self.top_scores_header_font_size)
        self.credits_font.set_bold(True)
        self.menu_font.set_italic(True)
        self.title_font.set_italic(True)
        self.text_pos = self.width * (3 / 5)
        self.menu_start_y = self.height / 3
        self.menu_y_space = self.height / 11
        self.space = self.menu_font_size
        self.y_const = self.height / 11
        self.starting_y_pos = self.height / 3.6
        self.width_tenth = self.width / 10
        self.scale = (self.width / 1920), (self.height / 1080)


config = Config()

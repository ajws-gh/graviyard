from constants import *
from static_methods import *


pygame.font.init()


class Menu:
    def __init__(self):
        # Screen
        self.selected_resolution = config.resolution[0]
        self.is_fullscreen = config.is_fullscreen
        self.screen = pygame.display.set_mode((config.width, config.height), config.screen_type)
        self.max_fps = config.max_fps

        # Top Scores
        self.scores = dict()
        self.score = 0
        self.name = ''
        self.place = -1
        self.score_updated = False
        self.appending = False
        self.nick_too_short = False

        # Indexes
        self.index = 0
        self.lr_index = 1
        self.res_index = config.resolution[1]
        self.fullscreen_index = config.is_fullscreen[1]
        self.level_index = config.entry_level
        self.music_index = config.music_on[1]
        self.sound_index = config.sounds_on[1]

        # Level
        self.nr_of_levels = 2
        self.current_level = config.entry_level

        # Sounds&Music
        self.music_on = config.music_on
        self.sounds_on = config.sounds_on

        # Menu
        self.settings_active = False
        self.draw = self.draw_menu
        self.title = config.title_font.render('GRAVIYARD', True, ORANGE)
        self.new_game = config.menu_font.render('NEW GAME', True, RED if self.index % 6 == 0 else BLACK)
        self.how_to_play = config.menu_font.render('HOW TO PLAY', True, RED if self.index % 6 == 1 else BLACK)
        self.settings = config.menu_font.render('SETTINGS', True, RED if self.index % 6 == 2 else BLACK)
        self.credits = config.menu_font.render('CREDITS', True, RED if self.index % 6 == 3 else BLACK)
        self.top_scores = config.menu_font.render('TOP SCORES', True, RED if self.index % 6 == 4 else BLACK)
        self.exit = config.menu_font.render('EXIT', True, RED if self.index % 6 == 5 else BLACK)

    def update(self):
        """Updates color of menu texts"""
        self.title = config.title_font.render('GRAVIYARD', True, ORANGE)
        self.new_game = config.menu_font.render('NEW GAME', True, RED if self.index % 6 == 0 else BLACK)
        self.how_to_play = config.menu_font.render('HOW TO PLAY', True, RED if self.index % 6 == 1 else BLACK)
        self.settings = config.menu_font.render('SETTINGS', True, RED if self.index % 6 == 2 else BLACK)
        self.credits = config.menu_font.render('CREDITS', True, RED if self.index % 6 == 3 else BLACK)
        self.top_scores = config.menu_font.render('TOP SCORES', True, RED if self.index % 6 == 4 else BLACK)
        self.exit = config.menu_font.render('EXIT', True, RED if self.index % 6 == 5 else BLACK)

    def draw_menu(self):
        self.screen.blit(config.menu_bg, (0, 0))
        self.screen.blit(self.title, (center_text(self.title), config.y_const))
        self.screen.blit(self.new_game, (center_text(self.new_game), config.menu_start_y))
        self.screen.blit(self.how_to_play,
                         (center_text(self.how_to_play), config.menu_start_y + config.menu_y_space))
        self.screen.blit(self.settings, (center_text(self.settings), config.menu_start_y +
                                         2 * config.menu_y_space))
        self.screen.blit(self.credits, (center_text(self.credits), config.menu_start_y + 3 * config.menu_y_space))
        self.screen.blit(self.top_scores,
                         (center_text(self.top_scores), config.menu_start_y + 4 * config.menu_y_space))
        self.screen.blit(self.exit, (center_text(self.exit), config.menu_start_y + 5 * config.menu_y_space))

    def draw_settings(self):
        title = config.title_font.render('Settings', True, ORANGE)
        center_x = center_text(title)
        self.screen.blit(config.menu_bg, (0, 0))
        self.screen.blit(title, (center_x, config.y_const))
        fullscreen = config.menu_font.render('Fullscreen', True, RED if self.index % 6 == 0 else BLACK)
        resolution = config.menu_font.render('Resolution', True, RED if self.index % 6 == 1 else BLACK)
        max_fps = config.menu_font.render('Max FPS', True, RED if self.index % 6 == 2 else BLACK)
        entry_level = config.menu_font.render('Entry Level', True, RED if self.index % 6 == 3 else BLACK)
        music = config.menu_font.render('Music', True, RED if self.index % 6 == 4 else BLACK)
        sounds = config.menu_font.render('Sounds', True, RED if self.index % 6 == 5 else BLACK)
        blit_list = [fullscreen, resolution, max_fps, entry_level, music, sounds]
        for nr, item in enumerate(blit_list):
            self.screen.blit(item, (config.width / 4, config.starting_y_pos + nr * config.y_const))

        resolution_list = ['Automatic', (1280, 720), (1920, 1080), (2560, 1440), (3840, 2160)]

        if self.index % 6 == 0 and self.settings_active:
            if self.fullscreen_index % 2 == 0:
                self.is_fullscreen = True, 2
            else:
                self.is_fullscreen = False, 1

        elif self.index % 6 == 1 and self.settings_active:
            self.selected_resolution = resolution_list[self.res_index % 5]

        elif self.index % 6 == 3 and self.settings_active:
            if self.level_index % 2 == 0:
                self.current_level = 2
            else:
                self.current_level = 1

        elif self.index % 6 == 4 and self.settings_active:
            self.music_on = ['On', 2] if self.music_index % 2 == 0 else ['Off', 1]

        elif self.index % 6 == 5 and self.settings_active:
            self.sounds_on = ['On', 2] if self.sound_index % 2 == 0 else ['Off', 1]

        fps = config.menu_font.render(f'{self.max_fps}', True, BLACK)
        level = config.menu_font.render(f'{self.current_level}', True, BLACK)
        res = config.menu_font.render(
            f'{resolution_list[self.res_index % 5][0]} x {resolution_list[self.res_index % 5][1]}'
            if not resolution_list[self.res_index % 5] == 'Automatic' else 'Automatic', True,
            BLACK)
        music_on = config.menu_font.render(f'{self.music_on[0]}', True, BLACK)
        sounds_on = config.menu_font.render(f'{self.sounds_on[0]}', True, BLACK)
        f_screen = config.menu_font.render('Yes' if self.is_fullscreen[0] else 'No', True, BLACK)

        self.screen.blit(f_screen, (config.text_pos, config.starting_y_pos))
        self.screen.blit(res, (config.text_pos, config.starting_y_pos + config.y_const))
        self.screen.blit(fps, (config.text_pos, config.starting_y_pos + 2 * config.y_const))
        self.screen.blit(level, (config.text_pos, config.starting_y_pos + 3 * config.y_const))
        self.screen.blit(music_on, (config.text_pos, config.starting_y_pos + 4 * config.y_const))
        self.screen.blit(sounds_on, (config.text_pos, config.starting_y_pos + 5 * config.y_const))

        blit_list = [f_screen, res, fps, level, music_on, sounds_on]

        # Drawing settings red arrows
        if self.settings_active:
            for nr, blit in enumerate(blit_list):
                if self.index % 6 == nr:
                    self.screen.blit(config.red_left_arrow, (arrow_pos(blit), config.starting_y_pos +
                                                             nr * config.y_const))
                    self.screen.blit(config.red_right_arrow, (arrow_pos(blit, True), config.starting_y_pos +
                                                              nr * config.y_const))
                    continue

    def draw_credits(self):
        title = config.title_font.render('Credits', True, ORANGE)
        center_x = center_text(title)
        self.screen.blit(config.menu_bg, (0, 0))
        self.screen.blit(title, (center_x, config.y_const))
        pygame.draw.rect(self.screen, (0, 0, 0),
                         (config.width / 75, config.height / 4, config.width * 73 / 75, config.width / 2.75),
                         border_radius=20)
        pygame.draw.rect(self.screen, YELLOW,
                         (config.width / 75, config.height / 4, config.width * 73 / 75, config.width / 2.75), width=8,
                         border_radius=20)
        with open('credits.txt', 'r') as file:
            lines = file.readlines()
        for nr, line in enumerate(lines):
            text = config.credits_font.render(line, True, YELLOW)
            self.screen.blit(text, (config.space, config.starting_y_pos + (nr * config.space / 1.5)))

    def draw_top_scores(self):
        self.screen.blit(config.menu_bg, (0, 0))
        title = config.title_font.render('TOP SCORES!', True, ORANGE)
        center_x = center_text(title)
        self.screen.blit(title, (center_x, config.y_const))
        if self.score_updated:
            my_score = config.top_scores_font.render('YOUR SCORE: ' + str(self.score), True, YELLOW)
            self.screen.blit(my_score, (center_text(my_score), config.height - config.y_const))
        if self.nick_too_short:
            text_to_print = config.top_scores_font.render('NICK MUST CONTAIN AT LEAST 3 CHARS, 1 SPACE ALLOWED', True,
                                                          RED)
            self.screen.blit(text_to_print, (center_text(text_to_print), config.height - 0.5 * config.y_const))

        pygame.draw.rect(self.screen, (0, 0, 0),
                         (config.width / 6, config.height / 3.75, config.width * 4 / 6, config.width / 2.9),
                         border_radius=20)
        pygame.draw.rect(self.screen, YELLOW,
                         (config.width / 6, config.height / 3.75, config.width * 4 / 6, config.width / 2.9), width=8,
                         border_radius=20)

        f_row_list = ['PLACE', 'PLAYER', 'SCORE']
        for number, text in enumerate(f_row_list):
            print_text = config.top_scores_header_font.render(text, True, ORANGE)
            self.screen.blit(print_text, (2 * config.width_tenth + number * 2.5 * config.width_tenth,
                                          config.menu_start_y))

        with open('top_scores.txt', 'r') as file:
            lines = file.readlines()
            for nr, line in enumerate(lines, 1):
                line = line.replace('\n', '').split()
                if len(line) > 3:
                    line[1] = line[1] + ' ' + line[2]
                    line[2] = line[3]
                    del line[3]
                if nr == self.place:
                    line = [line[0], self.name, str(self.score)]
                    for number, text in enumerate(line):
                        text_to_print = config.top_scores_font.render(text, True, RED)
                        self.screen.blit(text_to_print, (2 * config.width_tenth + number * 2.5 * config.width_tenth,
                                                         config.menu_start_y + config.space * self.place))
                else:
                    for number, text in enumerate(line):
                        text_to_print = config.top_scores_font.render(text, True, YELLOW)
                        self.screen.blit(text_to_print, (2 * config.width_tenth + number * 2.5 * config.width_tenth,
                                                         config.menu_start_y + config.space * nr))

    def draw_how_to_play(self):
        self.screen.blit(config.menu_bg, (0, 0))
        title = config.title_font.render('HOW TO PLAY', True, ORANGE)
        center_x = center_text(title)
        self.screen.blit(title, (center_x, config.y_const))

        blit_list = [config.how_to_attack_move, config.how_to_pause, config.how_to_restart, config.how_to_escape]
        if self.lr_index % 5 == 0:
            texts = ['The goal of this game is to achieve as low score as possible. The final',
                     'score is the time in which you complete all levels. Every time you kill a',
                     'zombie your score is decreased by one second!',
                     'GOOD LUCK!'
                     ]
            pygame.draw.rect(self.screen, (0, 0, 0),
                             (config.width / 15, config.height / 4, config.width * 13 / 15, config.width / 4),
                             border_radius=20)
            pygame.draw.rect(self.screen, YELLOW,
                             (config.width / 15, config.height / 4, config.width * 13 / 15, config.width / 4), width=15,
                             border_radius=20)
            for nr, text in enumerate(texts):
                text = config.menu_font.render(text, True, YELLOW)
                self.screen.blit(text, (center_text(text), config.menu_start_y + ((config.width_tenth / 2) * nr)))

        for nr, blit in enumerate(blit_list, 1):
            if self.lr_index % 5 == nr:
                self.screen.blit(blit, (center_text(blit), config.menu_start_y - (config.width_tenth / 2)))
                continue

        self.screen.blit(config.yellow_left_arrow, (center_text(config.how_to_restart) - (config.width_tenth / 2) -
                                                    config.yellow_left_arrow.get_width(), config.height / 2))
        self.screen.blit(config.yellow_right_arrow, (center_text(config.how_to_restart) +
                                                     config.how_to_restart.get_width() + (config.width_tenth / 2),
                                                     config.height / 2))

    def update_top_scores(self):
        """Checks if player score is in top10, if so updates the dictionary with scores"""
        if not self.score_updated:
            with open('top_scores.txt', 'r') as file:
                lines = file.readlines()
                for nr, line in enumerate(lines, 1):
                    split = line.split()
                    if len(split) != 3:
                        if len(split) == 4:
                            split[1] = split[1] + ' ' + split[2]
                            split[2] = split[3]
                            del split[3]
                        elif len(split) > 4:
                            self.scores[nr] = ['UNKNOWN', 'UNKNOWN']
                        elif len(split) < 3:
                            self.scores[nr] = ['UNKNOWN', split[1]]
                            continue
                    self.scores[nr] = [split[1], split[2]]
            for key in self.scores.keys():
                if self.score < float(self.scores[key][1]):
                    for index in range(10, key, -1):
                        self.scores[index] = self.scores[index - 1]
                    self.place = key
                    self.score_updated = True
                    self.update_top_scores_file()
                    self.appending = True
                    break
                else:
                    self.score_updated = True

    def update_top_scores_file(self):
        """If score is in top10 it updates the file with results"""
        with open('top_scores.txt', 'w') as file:
            self.scores[self.place] = [self.name, self.score]
            for key in self.scores.keys():
                file.write(f'{key}. {self.scores[key][0]} {self.scores[key][1]}\n')

    def append_to_name(self, key):
        """In case score is in top10 it allows user to input nickname"""
        if pygame.key.name(key) == 'return' and len(self.name) > 2:
            self.update_top_scores_file()
            self.place = -1
            self.name = ''
            config.game_started = False
            self.nick_too_short = False
            self.appending = False
        elif (pygame.key.name(key) == 'escape' or pygame.key.name(key) == 'return') and len(self.name) < 3:
            self.nick_too_short = True
        elif key == pygame.K_BACKSPACE and self.name:
            self.name = self.name[:-1]
        elif len(pygame.key.name(key)) == 1 and len(self.name) < 8:
            self.name += pygame.key.name(key)
        elif pygame.key.name(key) == 'space' and len(self.name) < 8 and ' ' not in self.name:
            self.name += ' '
        return self.name


menu = Menu()

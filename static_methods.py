import pygame
from config import config


def center_text(width: pygame.Surface):
    """Returns x position for text to be centered"""
    return (config.width - width.get_width()) / 2


def arrow_pos(text_width: pygame.Surface, right=False):
    return config.text_pos - (150 * config.scale[0]) if not right else config.text_pos + text_width.get_width() + \
        (150 * config.scale[0]) - config.red_left_arrow.get_width()


from menu import menu


def adding_user():
    return menu.draw == menu.draw_top_scores and menu.appending


def play_sound(sound):
    if config.sounds_on[0] == 'On':
        if sound == 'select':
            config.select_sound.play()
        elif sound == 'type':
            config.type_sound.play()
        elif sound == 'level_up':
            config.level_up_sound.play()
        elif sound == 'arrow_sound':
            config.arrow_sound.play()
        elif sound == 'hit_sound':
            config.hit_sound.play()


def inc_dec_lr_indexes(symbol):
    exec(f'menu.lr_index {symbol}= 1')
    if menu.index % 6 == 0:
        exec(f'menu.fullscreen_index {symbol}= 1')
    elif menu.index % 6 == 1:
        exec(f'menu.res_index {symbol}= 1')
    elif menu.index % 6 == 2:
        exec(f'menu.max_fps {symbol}= 5')
    elif menu.index % 6 == 3:
        exec(f'menu.level_index {symbol}= 1')
    elif menu.index % 6 == 4:
        exec(f'menu.music_index {symbol}= 1')
    elif menu.index % 6 == 5:
        exec(f'menu.sound_index {symbol}= 1')


def arrows_l_r_condition():
    return (menu.settings_active or menu.draw == menu.draw_how_to_play) and not config.game_started


def is_menu():
    return menu.draw == menu.draw_menu and not config.game_started


def arrows_up_down_condition():
    return not menu.draw == menu.draw_credits and not menu.draw == menu.draw_top_scores and \
           not menu.draw == menu.draw_how_to_play and not config.game_started and not menu.settings_active


def follow(camera_pos, player_pos, speed):
    """Adds delay to camera"""
    return camera_pos + (player_pos - camera_pos) * speed


def idle_props():
    index, count, elapsed = 0, 10, 0
    return index, count, elapsed


def fall_props():
    index, count, elapsed = 0, 4, 0
    return index, count, elapsed


def run_props():
    index, count, elapsed = 0, 4, 0
    return index, count, elapsed


def jump_props():
    index, count, elapsed = 0, 5, 0
    return index, count, elapsed


def walk_props():
    index, count, elapsed = 0, 5, 0
    return index, count, elapsed


def dead_props():
    index, count, elapsed = 0, 5, 0
    return index, count, elapsed


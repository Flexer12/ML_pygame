import math
import os
import csv

import pygame
import threading

from bin.game_classes.addition_helper import has_path
from bin.game_classes.blocks import Block
from bin.game_classes.player import Player
from bin.game_classes.selected_object import SelectedObject
from bin.game_classes.warrior import Warrior
from bin.ui.label import Label


# Класс сцены
class GameScene:
    # Конструктор класса
    def __init__(self, level, screen, settings, audio):
        self.map_ai = None
        self.level = level
        self.screen = screen
        self.settings = settings
        self.audio = audio
        self.data = {
            'win': False,
            'kill': 0,
            'coins': 0,
            'esc': False
        }
        self.max_enemy = 0
        self.clock = pygame.time.Clock()
        self.running_game = True
        self.exit_game = False
        self.map_width = None
        self.map_height = None
        self.k = 120 / int(self.settings.settings['fps'])
        self.size_block = (self.settings.get_resolution()[0] // 30,
                           self.settings.get_resolution()[1] // 16.875)
        self.objects = {
            'characters': pygame.sprite.Group(),
            'blocks': pygame.sprite.Group(),
        }

        self.name_textures = {
            'stone': (pygame.transform.scale(self.load_image('resources/textures/blocks/stone.png'), self.size_block),
                      True),
            'grass': (pygame.transform.scale(self.load_image('resources/textures/blocks/grass.png'), self.size_block),
                      False)
        }
        temp = [i for i in self.get_name_files('resources/textures/objects/coin/', '.png')]
        self.name_textures_objects = {
            'coin': [pygame.transform.scale(self.load_image(f'resources/textures/objects/coin/{i}.png',
                                                            transparent=True), self.size_block)
                     for i in range(len(temp))]
        }
        temp = [i for i in self.get_name_files('resources/textures/objects/portal/', '.png')]
        self.name_textures_objects['portal'] = [
            pygame.transform.scale(self.load_image(f'resources/textures/objects/portal/{i}.png',
                                                   transparent=True), self.size_block)
            for i in range(len(temp))]

        self.name_textures_characters = {
            'player': {},
            'warrior': {}
        }

        self.camera_target = None
        self.labels = {
            'coins': Label(self.settings.get_resolution()[0] / 2,
                           0,
                           f"Монеты = {self.data['coins']}",
                           text_color=(255, 255, 255),
                           font_size=self.settings.get_resolution()[0] // 30,
                           hover=True,
                           center=False),
            'health_player': Label(self.settings.get_resolution()[0] / 2,
                                   0,
                                   f"Здоровье = 0",
                                   text_color=(255, 255, 255),
                                   font_size=self.settings.get_resolution()[0] // 30,
                                   hover=True,
                                   center=False)
        }
        self.labels['coins'].set_position(self.settings.get_resolution()[0] * 0.8, 0)
        self.labels['coins'].update()
        self.labels['health_player'].set_position(
            self.settings.get_resolution()[0] * 0.8,
            self.settings.get_resolution()[1] * 0.05
        )
        self.labels['health_player'].update()

        self.background = None
        if os.path.exists(f'data/levels/level {level}/background.png'):
            self.background = self.load_image(f'data/levels/level {level}/background.png',
                                              self.settings.get_resolution())

    # Функция для получения всех названий файлов в указанной папке
    def get_name_files(self, path, format=''):
        file_list = []

        # Получить список файлов и папок в папке
        for file in os.listdir(path):
            file_path = os.path.join(path, file)

            # Проверяем, является ли файлом (не папкой)
            if os.path.isfile(file_path):
                # Проверяем расширение файла
                if not format:
                    file_list.append(file)
                elif file.endswith(format):
                    file_list.append(file)
        return file_list

    # Функция для вывода частоты кадров
    def show_fps(self):
        fps = str(round(self.clock.get_fps(), 2))
        text = pygame.font.Font(None, 24).render(fps, True, 'black')
        self.screen.blit(text, (3, 3))
        text = pygame.font.Font(None, 24).render(fps, True, 'white')
        self.screen.blit(text, (0, 0))

    # Функция для загрузки картинки
    def load_image(self, path, transparent=False, scale=(), crop=[0.0, 0.0, 0.0, 0.0]):
        if not os.path.exists(path):
            print(f"Файл с изображением '{path}' не найден")
            return False
        else:
            image = pygame.image.load(path)

            # Обрезка изображения
            if crop != [0.0, 0.0, 0.0, 0.0]:
                width, height = image.get_size()
                image = image.subsurface(pygame.Rect(round(width * crop[0]),
                                                     round(height * crop[1]),
                                                     round(width - (width * crop[2])),
                                                     round(height - (height * crop[3]))))

            if scale:
                image = pygame.transform.scale(image, scale)

            if transparent:
                image = image.convert_alpha()
            else:
                image = image.convert()
            return image

    # Функция для загрузки спрайтов для персонажей (Функция работает в мультипотоке)
    def load_image_character(self, character_name, movement, animation):
        path = f'resources/textures/characters/{character_name}/{movement}/{animation}/'
        temp = [i for i in self.get_name_files(path, '.png')]
        anim = []
        crop = [0.20, 0.25, 0.45, 0.36]

        for texture in range(len(temp)):
            image = self.load_image(f'{path}{texture}.png', transparent=True, scale=self.size_block,
                                    crop=crop)
            damage_image = image.copy()
            for x in range(damage_image.get_width()):
                for y in range(damage_image.get_height()):
                    pixel_color = damage_image.get_at((x, y))
                    if pixel_color[0] > 0 or pixel_color[1] > 0 or pixel_color[2] > 0:
                        damage_image.set_at((x, y), pygame.Color(255, pixel_color[1], pixel_color[2]))
            anim.append((image, damage_image))
        self.name_textures_characters[character_name][movement][animation] = anim.copy()

    # Функция загрузки уровня
    def load_level(self):
        self.objects = {
            'characters': pygame.sprite.Group(),
            'blocks_solid': pygame.sprite.Group(),
            'blocks_not_solid': pygame.sprite.Group(),
            'selected_objects': pygame.sprite.Group(),
            'exit': None,
            'player': None
        }

        data_player = {
            'speed_x': (1.5 * self.k) * (self.settings.get_resolution()[0] / 1920),
            'speed_y': (1.5 * self.k) * (self.settings.get_resolution()[1] / 1080),
            'size_block': self.size_block,
            'textures': self.name_textures_characters['player'],
            'time_frame': 4 // self.k,
            'damage': 30,
            'regen_time': 20 * 120 // self.k,
            'time_damage': int(self.settings.settings['fps']) // 2,
            'audio': {
                'attack': 'resources/sounds/strike_sound.mp3',
                'died': 'resources/sounds/human_dead_sound.mp3'
            }
        }

        data_warrior = {
            'speed_x': (1.3 * self.k) * (self.settings.get_resolution()[0] / 1920),
            'speed_y': (1.3 * self.k) * (self.settings.get_resolution()[1] / 1080),
            'size_block': self.size_block,
            'textures': self.name_textures_characters['warrior'],
            'time_frame': 4 // self.k,
            'damage': 25,
            'regen_time': 20 * 120 // self.k,
            'time_damage': int(self.settings.settings['fps']) // 2,
            'distance_visible': self.size_block[0] * 7,
            'max_time_idle': 180 * self.k,
            'audio': {
                'attack': 'resources/sounds/strike_sound.mp3',
                'died': 'resources/sounds/human_dead_sound.mp3'
            }
        }

        # Создаем потоки для загрузки текстур, без этого долго обрабатывать
        threads = []
        for character in self.name_textures_characters.keys():
            for movement in ('back', 'front', 'left_side', 'right_side'):
                self.name_textures_characters[character][movement] = {}
                for animation in ('attack', 'died', 'idle', 'run', 'walk'):
                    thread = threading.Thread(target=self.load_image_character, args=(character, movement, animation))
                    threads.append(thread)
                    thread.start()

        # Ожидание завершения всех потоков
        for thread in threads:
            thread.join()

        map_data = []
        with open(f'data/levels/level {self.level}/map.csv', encoding="utf8") as csvfile:
            map_data = list(csv.reader(csvfile, delimiter=';'))

        self.map_width = 0
        self.map_height = len(map_data) * self.size_block[1]
        if self.map_height:
            self.map_width = len(map_data[0]) * self.size_block[0]

        self.map_ai = []
        for row_i, row in enumerate(map_data):
            self.map_ai.append([])
            map_y = row_i * self.size_block[1]
            for col_i, col in enumerate(row):
                map_x = col_i * self.size_block[0]
                col = col.split(',')
                for block in col:
                    if block in self.name_textures.keys():
                        block_texture = self.name_textures[block]
                        if block_texture[1]:
                            self.objects['blocks_solid'].add(
                                Block(map_x, map_y, True, self.size_block, block_texture[0])
                            )
                            self.map_ai[-1].append(1)
                        else:
                            self.objects['blocks_not_solid'].add(
                                Block(map_x, map_y, False, self.size_block, block_texture[0])
                            )
                            self.map_ai[-1].append(0)
                    if block in self.name_textures_objects.keys():
                        object_textures = self.name_textures_objects[block]
                        self.objects['selected_objects'].add(
                            SelectedObject(map_x, map_y, self.size_block, 10 // self.k, object_textures)
                        )

                    if block == 'exit':
                        self.objects['exit'] = Block(map_x, map_y, False, self.size_block, color='blue',
                                                     textures_anim=self.name_textures_objects['portal'],
                                                     time_frame=10 // self.k)
                    if 'player' in block:
                        self.objects['player'] = Player(data_player, self.audio)
                        self.objects['player'].x = map_x
                        self.objects['player'].y = map_y
                        self.objects['player'].update([], [])
                        self.camera_target = self.objects['player']
                    if 'warrior' in block:
                        warrior = Warrior(data_warrior, self.audio)
                        warrior.x = map_x
                        warrior.y = map_y
                        warrior.update([], [])
                        self.objects['characters'].add(warrior)

            for i in self.map_ai:
                if len(i) == 0:
                    self.map_ai.remove([])
        self.max_enemy = len(self.objects['characters'])
        has_path(self.map_ai, 1, 1, 10, 2)

    # Получения позиции с учетом смещения камеры
    def apply_offset(self, rect, offset_x, offset_y):
        offset_rect = rect.copy()
        offset_rect.x += offset_x
        offset_rect.y += offset_y
        return offset_rect

    # Функция отработки игрового цикла
    def run(self):
        self.audio.play_music(f'data/levels/level {self.level}/background_music.mp3')

        self.load_level()

        while self.running_game:
            if self.background is not None:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((0, 0, 0))
            key_pressed_is = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True
                    self.running_game = False
                    self.data['esc'] = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.audio.play_sound('resources/sounds/lose_sound.mp3')
                        self.data['esc'] = True
                        self.running_game = False

            # Действия игрока
            if self.objects['player']:
                if self.objects['player'].delete:
                    self.objects['player'].kill()
                    self.objects['player'] = None
                else:
                    self.objects['player'].controller_player(key_pressed_is)
                    self.objects['player'].update(self.objects['blocks_solid'],
                                                  self.objects['characters'])

            # Центрирование камеры на игроке
            if self.camera_target:
                offset_x = (self.settings.get_resolution()[0] / 2) - self.camera_target.rect.x
                offset_y = (self.settings.get_resolution()[1] / 2) - self.camera_target.rect.y
            else:
                offset_x = 0
                offset_y = 0

            # Отрисовка
            for block in self.objects['blocks_solid']:
                self.screen.blit(block.image, self.apply_offset(block.rect, offset_x, offset_y))
            for block in self.objects['blocks_not_solid']:
                self.screen.blit(block.image, self.apply_offset(block.rect, offset_x, offset_y))
            for block in self.objects['selected_objects']:
                block.update()
                self.screen.blit(block.image, self.apply_offset(block.rect, offset_x, offset_y))

            for character in self.objects['characters']:
                if character.delete:
                    character.kill()
                else:
                    character.ai_controller(self.objects['player'], self.map_ai)
                    character.update(self.objects['blocks_solid'],
                                     [self.objects['player']])
                    self.screen.blit(character.image, self.apply_offset(character.rect, offset_x, offset_y))

            if self.objects['exit']:
                self.objects['exit'].update()
                self.screen.blit(self.objects['exit'].image,
                                 self.apply_offset(self.objects['exit'].rect, offset_x, offset_y))

            if self.objects['player']:
                self.screen.blit(self.objects['player'].image,
                                 self.apply_offset(self.objects['player'].rect, offset_x, offset_y))

            for key, label in self.labels.items():
                if key == 'health_player':
                    if self.objects['player']:
                        label.update(f'Здоровье = {self.objects["player"].health}')
                    else:
                        label.update(f'Вы погибли!')
                label.draw(self.screen)

            # Проверка на победу
            if self.objects['player'] and pygame.sprite.collide_rect(self.objects['player'], self.objects['exit']):
                if self.size_block[0] // 3 > math.sqrt((self.objects['exit'].rect.x - self.objects['player'].x) ** 2 + (
                        self.objects['exit'].rect.y - self.objects['player'].rect.y) ** 2):
                    self.data['win'] = True
                    self.audio.play_sound('resources/sounds/win_sound.mp3')
                    self.running_game = False

            # Проверка на сбор монеток
            for object in self.objects['selected_objects']:
                if self.objects['player'] and pygame.sprite.collide_mask(self.objects['player'], object):
                    self.data['coins'] += 1
                    self.audio.play_sound('resources/sounds/coin_sound.mp3')
                    self.labels['coins'].update(f"Монеты = {self.data['coins']}")
                    object.kill()

            # Прочее
            if self.settings.settings['show_fps'] == 'yes':
                self.show_fps()
            pygame.display.flip()
            self.clock.tick(int(self.settings.settings['fps']))

        # Фиксация количества поверженных противников
        self.data['kill'] = self.max_enemy - len(self.objects['characters'])
        if self.data['kill'] < 0:
            self.data['kill'] = 0

        # Если персонаж погиб, то не считается как досрочный выход
        if not self.objects['player']:
            self.data['esc'] = False

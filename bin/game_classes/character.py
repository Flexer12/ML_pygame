import pygame
from pygame import Surface, Color, Rect


# Класс персонажей
class Character(pygame.sprite.Sprite):
    # Конструктор класса
    def __init__(self, character_data, audio):
        super().__init__()
        self.health = 100
        self.image = Surface(character_data['size_block'])
        self.image.fill(Color('red'))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = Rect(0, 0, character_data['size_block'][0], character_data['size_block'][1])
        self.damage = character_data['damage']
        self.x = 0.0
        self.y = 0.0
        self.pred_x = 0
        self.pred_y = 0
        self.speed_x = character_data['speed_x']
        self.speed_y = character_data['speed_y']
        self.textures = character_data['textures']
        self.textures_current = [self.textures['front']['idle'], 'front', 'walk']
        self.i_time = 0
        self.time_frame = character_data['time_frame']
        self.attack = self.dead = False
        self.left = self.up = self.right = self.down = False
        self.shift = False
        self.current_frame = 0
        self.audio = audio
        self.audio_path = character_data['audio']
        self.delete = False
        self.time_damage = character_data['time_damage']
        self.i_time_damage = 0
        self.get_damage = False
        self.i_regen_time = 0
        self.regen_time = character_data['regen_time']

        self.column = 0
        self.row = 0

        self.size_block = character_data['size_block']

    # Функция обновления состояния персонажа
    def update(self, solid_blocks, enemy_list):
        self.row = round(self.y / self.size_block[1])
        self.column = round(self.x / self.size_block[0])

        # Если здоровья нет, умирает
        if self.health <= 0:
            if not self.dead:
                self.audio.play_sound(self.audio_path['died'])
                self.current_frame = 0
                self.i_time = 0
                self.dead = True
                self.textures_current[0] = self.textures[self.textures_current[1]]['died']
            else:
                self.i_time += 1

                if self.i_time >= self.time_frame * 10:
                    self.i_time = 0
                    self.current_frame += 1
                    if self.current_frame >= len(self.textures_current):
                        self.current_frame -= 1
                        self.delete = True
        # Описываем атаку
        elif self.attack:
            if self.textures_current[2] != 'attack':
                self.audio.play_sound(self.audio_path['attack'])
                self.textures_current[2] = 'attack'
                self.textures_current[0] = self.textures[self.textures_current[1]]['attack']
                self.i_time = 0
                self.current_frame = 0
            else:
                if self.left and self.textures_current[1] != 'left_side':
                    self.textures_current[1] = 'left_side'
                    self.textures_current[0] = self.textures[self.textures_current[1]]['attack']
                elif self.left:
                    pass
                elif self.right and self.textures_current[1] != 'right_side':
                    self.textures_current[1] = 'right_side'
                    self.textures_current[0] = self.textures[self.textures_current[1]]['attack']
                elif self.right:
                    pass
                elif self.up and self.textures_current[1] != 'back':
                    self.textures_current[1] = 'back'
                    self.textures_current[0] = self.textures[self.textures_current[1]]['attack']
                elif self.up:
                    pass
                elif self.down and self.textures_current[1] != 'front':
                    self.textures_current[1] = 'front'
                    self.textures_current[0] = self.textures[self.textures_current[1]]['attack']
                elif self.down:
                    pass

                self.i_time += 1

                if self.i_time >= self.time_frame:
                    self.i_time = 0
                    self.current_frame += 1
                    if self.current_frame >= len(self.textures_current[0]):
                        self.attack = False
                        self.current_frame = 0
                        self.i_time = 0

                        for enemy in enemy_list:
                            if enemy:
                                if pygame.sprite.collide_rect(self, enemy):
                                    enemy.health -= self.damage
                                    enemy.get_damage = True
                                    enemy.i_time_damage = 0

                        self.textures_current[2] = 'idle'
                        self.textures_current[0] = self.textures[self.textures_current[1]]['idle']
        # Описываем не атаку
        else:
            if self.health < 100 and self.i_regen_time > self.regen_time:
                self.i_regen_time = 0
                self.health += 1
            else:
                self.i_regen_time += 1

            change_move = False

            if self.left and self.textures_current[1] != 'left_side':
                self.textures_current[1] = 'left_side'
                change_move = True
            elif self.left:
                pass
            elif self.right and self.textures_current[1] != 'right_side':
                self.textures_current[1] = 'right_side'
                change_move = True
            elif self.right:
                pass
            elif self.up and self.textures_current[1] != 'back':
                self.textures_current[1] = 'back'
                change_move = True
            elif self.up:
                pass
            elif self.down and self.textures_current[1] != 'front':
                self.textures_current[1] = 'front'
                change_move = True
            elif self.down:
                pass

            if self.up or self.down or self.left or self.right:
                if self.shift and self.textures_current[2] != 'run':
                    self.textures_current[2] = 'run'
                    change_move = True
                elif not self.shift and self.textures_current[2] != 'walk':
                    self.textures_current[2] = 'walk'
                    change_move = True
            else:
                if self.textures_current[2] != 'idle':
                    self.textures_current[2] = 'idle'
                    self.textures_current[0] = self.textures[self.textures_current[1]]['idle']

            if change_move:
                self.i_time = 0
                self.current_frame = 0
                if self.shift:
                    self.textures_current[0] = self.textures[self.textures_current[1]]['run']
                else:
                    self.textures_current[0] = self.textures[self.textures_current[1]]['walk']

            self.i_time += 1

            if self.i_time >= self.time_frame:
                self.i_time = 0
                self.current_frame += 1
                if self.current_frame >= len(self.textures_current[0]):
                    self.current_frame = 0

        if self.textures_current and self.textures_current[0]:
            self.image = self.textures_current[0][self.current_frame][0]
            # Визуализация урона
            if self.get_damage:
                self.i_time_damage += 1
                if self.i_time_damage >= self.time_damage:
                    self.get_damage = False
                    self.i_time_damage = 0
                else:
                    self.image = self.textures_current[0][self.current_frame][1]

            self.mask = pygame.mask.from_surface(self.image)

        # Если здоровье есть, двигаемся
        if self.health > 0:
            self.pred_x = self.rect.x
            self.pred_y = self.rect.y

            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

            for block in solid_blocks:
                if pygame.sprite.collide_mask(self, block):
                    self.rect.x = self.pred_x
                    self.rect.y = self.pred_y
                    self.x = float(self.pred_x)
                    self.y = float(self.pred_y)

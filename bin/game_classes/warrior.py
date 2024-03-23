import math
import random
import pygame
from bin.game_classes.addition_helper import has_path
from bin.game_classes.character import Character


# Класс персонажа-врагов
class Warrior(Character):
    # Конструктор класса
    def __init__(self, character_data, audio):
        super().__init__(character_data, audio)
        self.distance_visible = character_data['distance_visible']
        self.max_time_idle = character_data['max_time_idle']
        self.current_time_idle = character_data['max_time_idle']
        self.target_cell = None
        self.path = []
        self.time_idle = 0

    # Функция для движения персонажа в определённую клетку
    def move_to_cell(self, target_cell):
        # 0 - x
        # 1 - y
        # Двигаемся вверх
        if target_cell[1] * self.size_block[1] < self.rect.y:
            if abs((self.y - self.speed_y) - (target_cell[1] * self.size_block[1])) < self.size_block[1] * 0.12:
                self.up = True
                self.y = target_cell[1] * self.size_block[1]
                self.target_cell = None
            else:
                self.up = True
                self.y -= self.speed_y

        # Двигаемся вниз
        elif target_cell[1] * self.size_block[1] > self.rect.y:
            if abs((self.y + self.speed_y) - (target_cell[1] * self.size_block[1])) < self.size_block[1] * 0.12:
                self.down = True
                self.y = target_cell[1] * self.size_block[1]
                self.target_cell = None
            else:
                self.down = True
                self.y += self.speed_y

        # Двигаемся вправо
        elif target_cell[0] * self.size_block[0] > self.rect.x:
            if abs((self.x + self.speed_x) - (target_cell[0] * self.size_block[0])) < self.size_block[0] * 0.12:
                self.right = True
                self.x = target_cell[0] * self.size_block[0]
                self.target_cell = None
            else:
                self.right = True
                self.x += self.speed_x

        # Двигаемся влево
        elif target_cell[0] * self.size_block[0] < self.rect.x:
            if abs((self.x - self.speed_x) - (target_cell[0] * self.size_block[0])) < self.size_block[0] * 0.12:
                self.left = True
                self.x = target_cell[0] * self.size_block[0]
                self.target_cell = None
            else:
                self.left = True
                self.x -= self.speed_x

        if not self.up and not self.down and not self.left and not self.right:
            self.target_cell = None

    # Контроллер имитирующий искусственный интеллект
    def ai_controller(self, enemy, map_ai):
        self.up = self.down = self.left = self.right = False
        check_enemy = False
        # Если враг существует, проверить путь до него
        if enemy is not None:
            distance = math.sqrt((enemy.rect.x - self.rect.x) ** 2 + (enemy.rect.y - self.rect.y) ** 2)
            if distance < self.distance_visible and self.target_cell is None:
                check_enemy = True
                path_to_enemy = has_path(map_ai, self.column, self.row, enemy.column, enemy.row)
                if path_to_enemy:
                    path_to_enemy = path_to_enemy[1:]
                    if path_to_enemy[0]:
                        if self.target_cell is None:
                            self.target_cell = path_to_enemy[0]
                        else:
                            self.move_to_cell(self.target_cell)

                if pygame.sprite.collide_rect(self, enemy):
                    self.attack = True

        # Если враг не обнаружен, патрулируем местность
        if not check_enemy:
            if self.target_cell:
                self.move_to_cell(self.target_cell)
            elif self.time_idle > 0:
                self.time_idle += 1

                if self.time_idle > self.max_time_idle:
                    self.time_idle = 0
            elif self.path:
                self.target_cell = self.path[0]
                self.path = self.path[1:]
            else:
                if random.randint(0, 1):
                    self.time_idle += 1
                    self.current_time_idle = random.randint(1, self.max_time_idle)
                else:
                    path_y_random = random.randint(0, len(map_ai) - 1)
                    path_x_random = random.randint(0, len(map_ai[path_y_random]) - 1)
                    while map_ai[path_y_random][path_x_random] != 0:
                        path_y_random = random.randint(0, len(map_ai) - 1)
                        path_x_random = random.randint(0, len(map_ai[path_y_random]) - 1)

                    self.path = has_path(map_ai, self.column, self.row, path_x_random, path_y_random)
        else:
            self.path = []

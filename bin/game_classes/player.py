import pygame
from bin.game_classes.character import Character


# Класс персонажа игрока
class Player(Character):
    # Конструктор класса
    def __init__(self, character_data, audio):
        super().__init__(character_data, audio)

    # Управление персонажем за счет кнопок с клавиатуры
    def controller_player(self, keys):
        if keys[pygame.K_BACKSPACE]:
            self.health = 0
            self.get_damage = True

        if keys[pygame.K_LSHIFT]:
            self.shift = True
        else:
            self.shift = False

        if keys[pygame.K_w]:
            self.up = True
            if keys[pygame.K_LSHIFT]:
                self.y -= self.speed_y * 2
            elif keys[pygame.K_LCTRL]:
                self.y -= self.speed_y / 2
            else:
                self.y -= self.speed_y
        else:
            self.up = False

        if keys[pygame.K_s]:
            self.down = True
            if keys[pygame.K_LSHIFT]:
                self.y += self.speed_y * 2
            elif keys[pygame.K_LCTRL]:
                self.y += self.speed_y / 2
            else:
                self.y += self.speed_y
        else:
            self.down = False

        if keys[pygame.K_a]:
            self.left = True
            if keys[pygame.K_LSHIFT]:
                self.x -= self.speed_x * 2
            elif keys[pygame.K_LCTRL]:
                self.x -= self.speed_x / 2
            else:
                self.x -= self.speed_x
        else:
            self.left = False

        if keys[pygame.K_d]:
            self.right = True
            if keys[pygame.K_LSHIFT]:
                self.x += self.speed_x * 2
            elif keys[pygame.K_LCTRL]:
                self.x += self.speed_x / 2
            else:
                self.x += self.speed_x
        else:
            self.right = False

        if keys[pygame.K_SPACE] and not self.attack:
            self.attack = True

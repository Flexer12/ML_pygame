import pygame
from pygame import *


# Класс блока
class Block(sprite.Sprite):
    # Конструктор класса
    def __init__(self, x, y, is_solid, size_block, texture=None, color=None, textures_anim=[], time_frame=1):
        sprite.Sprite.__init__(self)

        self.image = texture
        self.rect = Rect(x, y, size_block[0], size_block[1])
        self.is_solid = is_solid
        if self.image:
            self.mask = pygame.mask.from_surface(self.image)

        self.textures_anim = textures_anim

        if color:
            self.image = Surface(size_block)
            self.image.fill(Color(color))
            self.rect = Rect(0, 0, size_block[0], size_block[1])
            self.rect.x = x
            self.rect.y = y

        # Если спрайтов несколько, делаем анимацию
        self.time_frame = time_frame
        self.current_frame = 0
        if self.textures_anim:
            self.image = self.textures_anim[0]
        self.i_time = 0

    # Функция обновления, отрабатывает если есть много текстур
    def update(self):
        if self.textures_anim:
            self.i_time += 1
            if self.i_time >= self.time_frame:
                self.current_frame = self.current_frame + 1
                if self.current_frame >= len(self.textures_anim):
                    self.current_frame = 0
                    self.mask = pygame.mask.from_surface(self.image)
                self.image = self.textures_anim[self.current_frame]
                self.i_time = 0

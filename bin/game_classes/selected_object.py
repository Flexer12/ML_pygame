import pygame.sprite
from pygame import Surface, Color, Rect


# Класс подбираемых объектов
class SelectedObject(pygame.sprite.Sprite):
    # Конструктор класса
    def __init__(self, x, y, size_block, time_frame, textures=None, color='white'):
        super().__init__()
        self.image = Surface(size_block)
        self.image.fill(Color(color))
        self.rect = Rect(x, y, size_block[0], size_block[1])
        self.textures_anim = textures
        self.time_frame = time_frame
        self.current_frame = 0
        if self.textures_anim:
            self.image = self.textures_anim[0]
        self.i_time = 0

    # Обновление анимации объекта
    def update(self):
        self.i_time += 1
        if self.i_time >= self.time_frame:
            self.current_frame = self.current_frame + 1
            if self.current_frame >= len(self.textures_anim):
                self.current_frame = 0
            self.image = self.textures_anim[self.current_frame]
            self.i_time = 0

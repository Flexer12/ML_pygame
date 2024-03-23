import pygame


# Класс надписи
class Label:
    # Конструктор надписи
    def __init__(self, x, y, text='', font_size=20, text_color=(0, 0, 0), name='label', hover=False, center=True):
        self.rect = pygame.Rect(x, y, font_size * len(text) * 1.5, font_size * 2)
        self.rect_hover = pygame.Rect(x + (font_size / 10), y + (font_size / 10),
                                      font_size * len(text) * 1.5, font_size * 2)
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(None, font_size)
        self.text_color = text_color
        self.hover = hover
        self.name = name
        self.text_rect = None
        self.text_render = None
        self.text_rect_hover = None
        self.text_render_hover = None
        self.center = center

    # Установка позиции надписи
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.rect_hover.x = x + (self.font_size / 10)
        self.rect_hover.y = y + (self.font_size / 10)

    # Отрисовка надписи
    def draw(self, surface):
        if self.hover:
            surface.blit(self.text_render_hover, self.text_rect_hover)
        surface.blit(self.text_render, self.text_rect)

    # Обновление надписи
    def update(self, text=None):
        if text is not None:
            self.text = text

        self.text_render = self.font.render(self.text, True, self.text_color)
        if self.center:
            self.text_rect = self.text_render.get_rect(center=self.rect.center)
        else:
            self.text_rect = self.text_render.get_rect(topleft=self.rect.topleft)

        self.text_render_hover = self.font.render(self.text, True, (0, 0, 0))
        if self.center:
            self.text_rect_hover = self.text_render_hover.get_rect(center=self.rect_hover.center)
        else:
            self.text_rect_hover = self.text_render_hover.get_rect(topleft=self.rect_hover.topleft)

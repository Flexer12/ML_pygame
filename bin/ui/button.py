import pygame


# Класс кнопки
class Button:
    # Конструктор класса
    def __init__(self, x, y, width, height, text='', font_size=20, bg_color=(255, 255, 255),
                 hover_color=(200, 200, 200),
                 text_color=(0, 0, 0), name='button'):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.click_event = None
        self.name = name

    # Установка позиции кнопки
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    # Установка функции для выполнения при нажатии на кнопку
    def set_click_event(self, event_handler):
        self.click_event = event_handler

    # Рисуем кнопку
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        text_render = self.font.render(self.text, True, self.text_color)
        text_rect = text_render.get_rect(center=self.rect.center)
        surface.blit(text_render, text_rect)

    # Обновляем кнопку
    def update(self, click):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.is_hovered = True

            if click:
                if self.click_event is not None:
                    self.click_event()
        else:
            self.is_hovered = False

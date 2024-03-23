from bin.ui.button import Button


# Класс модификатор кнопки. Позволяет переключать значения
class ButtonSlider(Button):
    # Конструктор класса
    def __init__(self, x, y, width, height, text='', values=None, font_size=20, bg_color=(255, 255, 255),
                 hover_color=(200, 200, 200),
                 text_color=(0, 0, 0), name='button_slider'):
        super().__init__(x, y, width, height, text, font_size, bg_color, hover_color, text_color, name)

        if values is None:
            self.values = []
            self.values_i = None
        else:
            self.values = values
            self.values_i = -1

        self.default_text = text
        self.click_event = self.click_button_slider
        self.click_button_slider()

    # Нажатие на кнопку-слайдер
    def click_button_slider(self):
        self.text = self.default_text

        if self.values:
            self.values_i = (self.values_i + 1) % len((self.values))
            self.text += ': ' + str(self.values[self.values_i])
        else:
            self.values_i = None

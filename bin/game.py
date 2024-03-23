import ctypes

import pygame

from bin.game_scene import GameScene
from bin.settings import Settings
from bin.audio import AudioManager
from bin.ui.button import Button
from bin.ui.button_sliider import ButtonSlider
from bin.ui.label import Label


# Класс игры (всех меню)
class Game:
    # Конструктор класса
    def __init__(self):
        self.background = None
        self.exit_game = False
        self.clock = None
        self.font_fps = None
        self.settings = None
        self.restart = False
        self.audio = None
        self.screen = None
        self.window = 'main_menu'

    # Функция для вывода частоты кадров
    def show_fps(self):
        fps = str(round(self.clock.get_fps(), 2))
        text = pygame.font.Font(None, 24).render(fps, True, 'black')
        self.screen.blit(text, (3, 3))
        text = pygame.font.Font(None, 24).render(fps, True, 'white')
        self.screen.blit(text, (0, 0))

    # Функция для запуска и установки настроек игры
    def run(self):
        pygame.init()
        ctypes.windll.user32.SetProcessDPIAware()

        self.settings = Settings(pygame.display.list_modes())
        self.clock = pygame.time.Clock()

        if self.settings.settings['full_screen'] == 'no':
            self.screen = pygame.display.set_mode(self.settings.get_resolution())
        else:
            self.screen = pygame.display.set_mode(self.settings.get_resolution(), pygame.FULLSCREEN)

        self.background = pygame.image.load(f'resources/game/background_menu.png').convert()
        self.background = pygame.transform.scale(self.background, self.settings.get_resolution())

        self.screen.blit(self.background, (0, 0))
        label = Label(x=self.settings.get_resolution()[0] / 10,
                      y=self.settings.get_resolution()[1] / 20,
                      text='Загрузка',
                      font_size=self.settings.get_resolution()[0] // 40,
                      text_color=(255, 255, 255),
                      hover=True)
        label.set_position(self.settings.get_resolution()[0] / 2 - (label.rect.width / 2),
                           self.settings.get_resolution()[1] / 2 - (label.rect.height / 2))
        label.update()
        label.draw(self.screen)
        pygame.display.flip()

        self.audio = AudioManager()
        self.audio.set_music_volume(int(self.settings.settings['music_volume']) / 100)
        self.audio.set_sound_volume(int(self.settings.settings['sound_volume']) / 100)

        pygame.display.set_caption('Mythical Labyrinth')
        pygame.display.set_icon(pygame.image.load('resources/game/icon.ico').convert())
        self.audio.play_music('resources/game/main_menu.mp3')
        self.set_window('main_menu')

        # Игровой цикл для переключений меню и игровой сцены
        while not self.exit_game:
            if self.window == 'main_menu':
                self.main_menu()
            elif self.window == 'level_menu':
                self.level_menu()
            elif self.window == 'settings_menu':
                self.settings_menu()
            elif self.window == 'statistic_menu':
                self.statistic_menu()
            elif 'game' in self.window:
                if 'new' in self.window:
                    self.settings.db.delete_all('saves')

                if 'repeat' in self.window:
                    self.window = self.window.replace('repeat_', '')

                self.game(int(self.window.split('_')[-1]))

        pygame.quit()

    # Функция для вывода главного меню
    def main_menu(self):
        window = 'main_menu'
        buttons = set()
        button = Button(x=self.settings.get_resolution()[0] / 10,
                        y=self.settings.get_resolution()[1] / 20,
                        width=self.settings.get_resolution()[0] / 3,
                        height=self.settings.get_resolution()[1] / 20,
                        text='Уровни',
                        font_size=self.settings.get_resolution()[0] // 40)
        button.set_click_event(lambda: self.set_window('level_menu'))
        buttons.add(button)

        button = Button(x=self.settings.get_resolution()[0] / 10,
                        y=self.settings.get_resolution()[1] / 20 * 2.5,
                        width=self.settings.get_resolution()[0] / 3,
                        height=self.settings.get_resolution()[1] / 20,
                        text='Статистика',
                        font_size=self.settings.get_resolution()[0] // 40)
        button.set_click_event(lambda: self.set_window('statistic_menu'))
        buttons.add(button)

        button = Button(x=self.settings.get_resolution()[0] / 10,
                        y=self.settings.get_resolution()[1] / 20 * 4,
                        width=self.settings.get_resolution()[0] / 3,
                        height=self.settings.get_resolution()[1] / 20,
                        text='Настройка',
                        font_size=self.settings.get_resolution()[0] // 40)
        button.set_click_event(lambda: self.set_window('settings_menu'))
        buttons.add(button)

        button = Button(x=self.settings.get_resolution()[0] / 10,
                        y=self.settings.get_resolution()[1] / 20 * 5.5,
                        width=self.settings.get_resolution()[0] / 3,
                        height=self.settings.get_resolution()[1] / 20,
                        text='Выход из игры',
                        font_size=self.settings.get_resolution()[0] // 40)
        button.set_click_event(self.set_exit_game)
        buttons.add(button)

        while self.window == window and not self.exit_game:
            self.screen.blit(self.background, (0, 0))
            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.set_window('')
                        self.set_exit_game()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True

            for button in buttons:
                button.update(click)
                button.draw(self.screen)

            if self.settings.settings['show_fps'] == 'yes':
                self.show_fps()
            pygame.display.flip()
            self.clock.tick(int(self.settings.settings['fps']))
        buttons.clear()

    # Функция для вывода меню уровней
    def level_menu(self):
        window = 'level_menu'
        self.set_window('level_menu')
        buttons = set()

        button = Button(x=self.settings.get_resolution()[0] / 10,
                        y=self.settings.get_resolution()[1] / 20,
                        width=self.settings.get_resolution()[0] / 3,
                        height=self.settings.get_resolution()[1] / 20,
                        text='Начать новую игру',
                        font_size=self.settings.get_resolution()[0] // 40)
        button.set_click_event(lambda: self.set_window('game_new_1'))
        buttons.add(button)

        button = Button(x=self.settings.get_resolution()[0] / 10,
                        y=self.settings.get_resolution()[1] / 20 * 2.5,
                        width=self.settings.get_resolution()[0] / 3,
                        height=self.settings.get_resolution()[1] / 20,
                        text='Уровень 1',
                        font_size=self.settings.get_resolution()[0] // 40)
        button.set_click_event(lambda: self.set_window('game_1'))
        buttons.add(button)

        button = ButtonSlider(x=self.settings.get_resolution()[0] / 10,
                              y=self.settings.get_resolution()[1] / 20 * 4,
                              width=self.settings.get_resolution()[0] / 3,
                              height=self.settings.get_resolution()[1] / 20,
                              text='Уровень 2',
                              font_size=self.settings.get_resolution()[0] // 40)
        button.set_click_event(lambda: self.set_window('game_2'))
        buttons.add(button)

        button = ButtonSlider(x=self.settings.get_resolution()[0] / 10,
                              y=self.settings.get_resolution()[1] / 20 * 5.5,
                              width=self.settings.get_resolution()[0] / 3,
                              height=self.settings.get_resolution()[1] / 20,
                              text='Уровень 3',
                              font_size=self.settings.get_resolution()[0] // 40)
        button.set_click_event(lambda: self.set_window('game_3'))
        buttons.add(button)

        button = Button(x=self.settings.get_resolution()[0] / 10 + self.settings.get_resolution()[0] / 3 * 1.1,
                        y=self.settings.get_resolution()[1] / 20 * 5.5,
                        width=self.settings.get_resolution()[0] / 3,
                        height=self.settings.get_resolution()[1] / 20,
                        text='Выйти в главное меню',
                        font_size=self.settings.get_resolution()[0] // 40)
        button.set_click_event(lambda: self.set_window('main_menu'))
        buttons.add(button)

        while self.window == window and not self.exit_game:
            self.screen.blit(self.background, (0, 0))
            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.set_window('main_menu')

                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True

            for button in buttons:
                button.update(click)
                button.draw(self.screen)

            if self.settings.settings['show_fps'] == 'yes':
                self.show_fps()
            pygame.display.flip()
            self.clock.tick(int(self.settings.settings['fps']))

    # Функция для вывода меню настроек
    def settings_menu(self):
        window = 'setting_menu'
        self.set_window('setting_menu')
        buttons = set()
        button = ButtonSlider(x=self.settings.get_resolution()[0] / 10,
                              y=self.settings.get_resolution()[1] / 20,
                              width=self.settings.get_resolution()[0] / 3,
                              height=self.settings.get_resolution()[1] / 20,
                              text='Полноэкранный режим',
                              values=['Да', 'Нет'] if self.settings.settings['full_screen'] == 'yes' else ['Нет', 'Да'],
                              name='full_screen',
                              font_size=self.settings.get_resolution()[0] // 40)
        buttons.add(button)

        temp = self.settings.resolutions.index(self.settings.get_resolution())
        button = ButtonSlider(x=self.settings.get_resolution()[0] / 10,
                              y=self.settings.get_resolution()[1] / 20 * 2.5,
                              width=self.settings.get_resolution()[0] / 3,
                              height=self.settings.get_resolution()[1] / 20,
                              text='Разрешение',
                              values=self.settings.resolutions[temp:] + self.settings.resolutions[:temp],
                              name='resolution',
                              font_size=self.settings.get_resolution()[0] // 40)
        buttons.add(button)

        button = ButtonSlider(x=self.settings.get_resolution()[0] / 10,
                              y=self.settings.get_resolution()[1] / 20 * 4,
                              width=self.settings.get_resolution()[0] / 3,
                              height=self.settings.get_resolution()[1] / 20,
                              text='Показывать ЧК',
                              values=['Да', 'Нет'] if self.settings.settings['show_fps'] == 'yes' else ['Нет', 'Да'],
                              name='show_fps',
                              font_size=self.settings.get_resolution()[0] // 40)
        buttons.add(button)

        temp = [i for i in range(20, 130, 10)].index(int(self.settings.settings['fps']))
        button = ButtonSlider(x=self.settings.get_resolution()[0] / 10,
                              y=self.settings.get_resolution()[1] / 20 * 5.5,
                              width=self.settings.get_resolution()[0] / 3,
                              height=self.settings.get_resolution()[1] / 20,
                              text='Частота кадров',
                              values=[i for i in range(20, 130, 10)][temp:] + [i for i in range(20, 130, 10)][:temp],
                              name='fps',
                              font_size=self.settings.get_resolution()[0] // 40)
        buttons.add(button)

        volume = [i for i in range(0, 110, 10)]
        temp = volume.index(int(self.settings.settings['music_volume']))
        button = ButtonSlider(x=self.settings.get_resolution()[0] / 10,
                              y=self.settings.get_resolution()[1] / 20 * 7,
                              width=self.settings.get_resolution()[0] / 3,
                              height=self.settings.get_resolution()[1] / 20,
                              text='Громкость музыки',
                              values=volume[temp:] + volume[:temp],
                              name='music_volume',
                              font_size=self.settings.get_resolution()[0] // 40)
        buttons.add(button)

        volume = [i for i in range(0, 110, 10)]
        temp = volume.index(int(self.settings.settings['sound_volume']))
        button = ButtonSlider(x=self.settings.get_resolution()[0] / 10,
                              y=self.settings.get_resolution()[1] / 20 * 8.5,
                              width=self.settings.get_resolution()[0] / 3,
                              height=self.settings.get_resolution()[1] / 20,
                              text='Громкость звуков',
                              values=volume[temp:] + volume[:temp],
                              name='sound_volume',
                              font_size=self.settings.get_resolution()[0] // 40)
        buttons.add(button)

        button = Button(x=self.settings.get_resolution()[0] / 10 + self.settings.get_resolution()[0] / 3 * 1.1,
                        y=self.settings.get_resolution()[1] / 20 * 7,
                        width=self.settings.get_resolution()[0] / 3,
                        height=self.settings.get_resolution()[1] / 20,
                        text='Сохранить и выйти',
                        font_size=self.settings.get_resolution()[0] // 40)
        button.set_click_event(lambda: self.setting_save(buttons))
        buttons.add(button)

        button = Button(x=self.settings.get_resolution()[0] / 10 + self.settings.get_resolution()[0] / 3 * 1.1,
                        y=self.settings.get_resolution()[1] / 20 * 8.5,
                        width=self.settings.get_resolution()[0] / 3,
                        height=self.settings.get_resolution()[1] / 20,
                        text='Отмена',
                        font_size=self.settings.get_resolution()[0] // 40)
        button.set_click_event(lambda: self.set_window('main_menu'))
        buttons.add(button)

        while not self.exit_game and window == self.window:
            self.screen.blit(self.background, (0, 0))
            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.set_window('main_menu')

                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True

            for button in buttons:
                button.update(click)
                button.draw(self.screen)

            if self.settings.settings['show_fps'] == 'yes':
                self.show_fps()
            pygame.display.flip()
            self.clock.tick(int(self.settings.settings['fps']))

    # Функция сохранения настроек
    def setting_save(self, buttons):
        for button in buttons:
            if button.name == 'full_screen':
                if button.values[button.values_i] == 'Да':
                    self.settings.settings['full_screen'] = 'yes'
                else:
                    self.settings.settings['full_screen'] = 'no'

            if button.name == 'resolution':
                self.settings.settings['resolution'] = 'x'.join(map(str, button.values[button.values_i]))

            if button.name == 'show_fps':
                if button.values[button.values_i] == 'Да':
                    self.settings.settings['show_fps'] = 'yes'
                else:
                    self.settings.settings['show_fps'] = 'no'

            if button.name == 'fps':
                self.settings.settings['fps'] = str(button.values[button.values_i])

            if button.name == 'music_volume':
                self.settings.settings['music_volume'] = str(button.values[button.values_i])

            if button.name == 'sound_volume':
                self.settings.settings['sound_volume'] = str(button.values[button.values_i])

        self.settings.save_settings()
        self.restart = True
        self.exit_game = True

    # Функция для вывода статистики по уровню
    def level_statistics_menu(self, level, data):
        window = self.window

        labels = set()

        label = Label(x=self.settings.get_resolution()[0] / 10,
                      y=self.settings.get_resolution()[1] / 20,
                      text='Победа!' if data['win'] else 'Поражение!',
                      font_size=self.settings.get_resolution()[0] // 40,
                      text_color=(255, 255, 255),
                      hover=True)
        label.set_position(self.settings.get_resolution()[0] / 2 - (label.rect.width / 2), label.rect.y)
        label.update()
        labels.add(label)

        label = Label(x=self.settings.get_resolution()[0] / 10,
                      y=self.settings.get_resolution()[1] / 20 * 2.5,
                      text=f'Собрано монет = {data["coins"]}',
                      font_size=self.settings.get_resolution()[0] // 40,
                      text_color=(255, 255, 255),
                      hover=True)
        label.set_position(self.settings.get_resolution()[0] / 2 - (label.rect.width / 2), label.rect.y)
        label.update()
        labels.add(label)

        label = Label(x=self.settings.get_resolution()[0] / 10,
                      y=self.settings.get_resolution()[1] / 20 * 4,
                      text=f'Побеждено противников = {data["kill"]}',
                      font_size=self.settings.get_resolution()[0] // 40,
                      text_color=(255, 255, 255),
                      hover=True)
        label.set_position(self.settings.get_resolution()[0] / 2 - (label.rect.width / 2), label.rect.y)
        label.update()
        labels.add(label)

        label = Label(x=self.settings.get_resolution()[0] / 10,
                      y=self.settings.get_resolution()[1] / 20 * 5.5,
                      text='Нажмите "ESC" для выхода в меню',
                      font_size=self.settings.get_resolution()[0] // 40,
                      text_color=(255, 255, 255),
                      hover=True)
        label.set_position(self.settings.get_resolution()[0] / 2 - (label.rect.width / 2), label.rect.y)
        label.update()
        labels.add(label)

        label = Label(x=self.settings.get_resolution()[0] / 10,
                      y=self.settings.get_resolution()[1] / 20 * 7,
                      text='Нажмите "ENTER" для повторного прохождения уровня',
                      font_size=self.settings.get_resolution()[0] // 40,
                      text_color=(255, 255, 255),
                      hover=True)
        label.set_position(self.settings.get_resolution()[0] / 2 - (label.rect.width / 2), label.rect.y)
        label.update()
        labels.add(label)

        while not self.exit_game and window == self.window:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.set_window('level_menu')
                    if event.key == pygame.K_RETURN:
                        self.set_window(f'game_level_repeat_{level}')

            for label in labels:
                label.draw(self.screen)

            if self.settings.settings['show_fps'] == 'yes':
                self.show_fps()
            pygame.display.flip()
            self.clock.tick(int(self.settings.settings['fps']))

        db_save = self.settings.db.select_by_col('saves', 'level', level)

        data['level'] = level
        if db_save:
            db_save = db_save[0]
            if data['win']:
                data['win'] = 0
                data['win'] += 1
                data['win'] += db_save[2]
            else:
                data['win'] = 0
                data['win'] = db_save[2]

            if not data['win']:
                data['lose'] = 0
                data['lose'] += 1
                data['lose'] += db_save[2]
            else:
                data['lose'] = 0
                data['lose'] = db_save[2]
            data['kill'] = data['kill'] + db_save[4]
            data['coins'] = data['coins'] + db_save[5]
            self.settings.db.update_save(data)
        else:
            self.settings.db.insert_save(data)

    # Функция для вывода статистики по всем уровням
    def statistic_menu(self):
        window = 'statistic_menu'
        self.set_window('statistic_menu')
        data = self.settings.db.select_all('saves')
        labels = set()

        label = Label(x=self.settings.get_resolution()[0] * 0.01,
                      y=self.settings.get_resolution()[1] * 0.01,
                      text='Нажмите "ESC" чтобы выйти в главное меню',
                      font_size=self.settings.get_resolution()[0] // 40,
                      text_color=(255, 255, 255),
                      hover=True,
                      center=False)
        label.update()
        labels.add(label)

        label = Label(x=self.settings.get_resolution()[0] * 0.01,
                      y=self.settings.get_resolution()[1] * 0.1,
                      text='Уровень',
                      font_size=self.settings.get_resolution()[0] // 40,
                      text_color=(255, 255, 255),
                      hover=True,
                      center=False)
        label.update()
        labels.add(label)

        label = Label(x=self.settings.get_resolution()[0] * 0.2,
                      y=self.settings.get_resolution()[1] * 0.1,
                      text='Побед',
                      font_size=self.settings.get_resolution()[0] // 40,
                      text_color=(255, 255, 255),
                      hover=True,
                      center=False)
        label.update()
        labels.add(label)

        label = Label(x=self.settings.get_resolution()[0] * 0.4,
                      y=self.settings.get_resolution()[1] * 0.1,
                      text='Поражений',
                      font_size=self.settings.get_resolution()[0] // 40,
                      text_color=(255, 255, 255),
                      hover=True,
                      center=False)
        label.update()
        labels.add(label)

        label = Label(x=self.settings.get_resolution()[0] * 0.6,
                      y=self.settings.get_resolution()[1] * 0.1,
                      text='Врагов',
                      font_size=self.settings.get_resolution()[0] // 40,
                      text_color=(255, 255, 255),
                      hover=True,
                      center=False)
        label.update()
        labels.add(label)

        label = Label(x=self.settings.get_resolution()[0] * 0.8,
                      y=self.settings.get_resolution()[1] * 0.1,
                      text='Монет',
                      font_size=self.settings.get_resolution()[0] // 40,
                      text_color=(255, 255, 255),
                      hover=True,
                      center=False)
        label.update()
        labels.add(label)

        x_pos = [0.01, 0.2, 0.4, 0.6, 0.8]
        for index_level, level in enumerate(data):
            level = level[1:]
            for index_arg, arg in enumerate(level):
                label = Label(x=self.settings.get_resolution()[0] * x_pos[index_arg],
                              y=self.settings.get_resolution()[1] * (0.2 + (0.1 * index_level)),
                              text=str(arg),
                              font_size=self.settings.get_resolution()[0] // 40,
                              text_color=(255, 255, 255),
                              hover=True,
                              center=False)
                label.update()
                labels.add(label)

        while not self.exit_game and window == self.window:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        self.set_window('main_menu')

            for label in labels:
                label.draw(self.screen)

            if self.settings.settings['show_fps'] == 'yes':
                self.show_fps()
            pygame.display.flip()
            self.clock.tick(int(self.settings.settings['fps']))

    # Функция для установки значения для выхода
    def set_exit_game(self):
        self.exit_game = True

    # Функция для установки активного окна
    def set_window(self, window):
        self.window = window

    # Функция для загрузки игровой сцены и отображения последующих результатов
    def game(self, level):
        pygame.mouse.set_visible(False)
        self.screen.blit(self.background, (0, 0))
        label = Label(x=self.settings.get_resolution()[0] / 10,
                      y=self.settings.get_resolution()[1] / 20,
                      text='Загрузка',
                      font_size=self.settings.get_resolution()[0] // 40,
                      text_color=(255, 255, 255),
                      hover=True)
        label.set_position(self.settings.get_resolution()[0] / 2 - (label.rect.width / 2),
                           self.settings.get_resolution()[1] / 2 - (label.rect.height / 2))
        label.update()
        label.draw(self.screen)
        pygame.display.flip()

        game_scene = GameScene(level, self.screen, self.settings, self.audio)
        game_scene.run()

        pygame.mouse.set_visible(True)
        self.audio.play_music('resources/game/main_menu.mp3')

        if game_scene.exit_game:
            self.set_exit_game()

        if not self.exit_game:
            data = game_scene.data

            if not data['esc']:
                del data['esc']
                self.level_statistics_menu(level, data)
            else:
                self.set_window('level_menu')

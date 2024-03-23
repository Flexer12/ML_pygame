import pygame


# Класс аудио-менеджера для проигрывания музыки и звуков
class AudioManager:
    # Конструктор класса
    def __init__(self):
        pygame.mixer.init()
        self.music_volume = 0.5
        self.sound_volume = 0.5

    # Функция проигрывания музыки
    def play_music(self, file_path, repeat=True):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(self.music_volume)

        if repeat:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.play()

    # Функция остановки проигрывания музыки
    def stop_music(self):
        pygame.mixer.music.stop()

    # Функция установки громкости музыки
    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(self.music_volume)

    # Функция проигрывания звуков
    def play_sound(self, file_path):
        sound = pygame.mixer.Sound(file_path)
        sound.set_volume(self.sound_volume)
        sound.play()

    # Установка громкости звуков
    def set_sound_volume(self, volume):
        self.sound_volume = volume

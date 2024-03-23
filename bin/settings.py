from bin.databasa_manager import DatabaseManager


# Класс настроек
class Settings:
    # Конструктор класса
    def __init__(self, resolutions):
        self.db = DatabaseManager()

        # Получаем список поддерживаемых разрешений
        self.resolutions = [resolution for resolution in resolutions if resolution[0] >= 600 and resolution[1] >= 600]
        self.settings = {
            'fps': 120,
            'resolution': f'{self.resolutions[-1][0]}x{self.resolutions[-1][1]}',
            'full_screen': 'no',
            'show_fps': 'yes',
            'music_volume': '50',
            'sound_volume': '50'
        }

        self.load_settings()

    # Функция для получения текущего разрешения окна
    def get_resolution(self):
        return tuple(map(int, self.settings['resolution'].split('x')))

    # Функция для загрузки настроек игры
    def load_settings(self):
        data = self.db.select_all('settings')
        if len(data):
            for row in data:
                self.settings[row[1]] = row[2]
        self.save_settings()

    # Функция для сохранения настроек
    def save_settings(self):
        self.db.update_settings(self.settings)

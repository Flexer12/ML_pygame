from bin.game import Game

# Создаем экземпляр игры и запускаем
game = Game()
game.run()

# Функция перезапуска игры
while game.restart:
    game = Game()
    game.run()

del game

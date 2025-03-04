import random


class Cart:
    def __init__(self):
        # Генерация 15 уникальных чисел для карточки
        self.numbers = sorted(random.sample(range(1, 91), 15))
        # Разделение на 3 строки по 5 чисел
        self.rows = [self.numbers[i*5:(i+1)*5] for i in range(3)]
        # Добавление пустых клеток и сортировка
        for row in self.rows:
            row.sort()
            # Добавляем 4 пустые клетки в случайные позиции
            empty_indices = random.sample(range(9), 4)
            for i in sorted(empty_indices, reverse=True):
                row.insert(i, '  ')  # Два пробела для выравнивания

    def display(self, title):
        print(title)
        for row in self.rows:
            # Форматируем строку для красивого вывода
            print(' '.join(f'{num:2}' for num in row))
        print('-' * 30)

    def mark_number(self, number):
        for row in self.rows:
            if number in row:
                index = row.index(number)
                row[index] = '--'  # Зачеркиваем число
                return True
        return False

    def is_complete(self):
        # Проверяем, все ли числа зачеркнуты
        return all(num == '--' for row in self.rows for num in row if num != '  ')

class PlayerComp:
    def __init__(self, name):
        self.name = name  # Имя игрока
        self.cart = Cart()

    def take_turn(self, number):
        if self.cart.mark_number(number):
            print(f"{self.name} зачеркнул число {number}")
        else:
            print(f"{self.name} пропустил число {number}")
        # Компьютер никогда не проигрывает из-за пропуска числа
        return True  # Всегда возвращаем True

class PlayerHuman:
    def __init__(self, name):
        self.name = name  # Имя игрока
        self.cart = Cart()

    def take_turn(self, number):
        self.cart.display(f"------ Карточка {self.name} ------")
        choice = input(f"Число {number} есть на вашей карточке? Зачеркнуть? (y/n): ")
        if choice.lower() == 'y':
            if not self.cart.mark_number(number):
                print(f"{self.name}, такого числа нет на вашей карточке. Вы проиграли!")
                return False
        else:
            if self.cart.mark_number(number):
                print(f"{self.name}, вы пропустили число, которое есть на вашей карточке. Вы проиграли!")
                return False
        return True

import random

class Game:
    def __init__(self, player1_type='human', player2_type='comp', player1_name="Игрок 1", player2_name="Игрок 2"):
        self.barrels = random.sample(range(1, 91), 90)  # Все бочонки
        # Создаем игроков в зависимости от выбранного типа
        self.player1 = PlayerHuman(player1_name) if player1_type == 'human' else PlayerComp(player1_name)
        self.player2 = PlayerHuman(player2_name) if player2_type == 'human' else PlayerComp(player2_name)

    def start(self):
        for turn, number in enumerate(self.barrels, 1):
            print(f"\nНовый бочонок: {number} (осталось {90 - turn})")
            # Ход первого игрока
            if not self.player1.take_turn(number):
                print(f"{self.player1.name} проиграл. Игра завершена.")
                break
            # Ход второго игрока
            if not self.player2.take_turn(number):
                print(f"{self.player2.name} проиграл. Игра завершена.")
                break
            # Проверяем завершение игры
            if self.player1.cart.is_complete():
                print(f"Поздравляем! {self.player1.name} выиграл!")
                break
            if self.player2.cart.is_complete():
                print(f"Поздравляем! {self.player2.name} выиграл!")
                break
#  Выбор типа игроков
def select_player_type(player_number):
    while True:
        choice = input(f"Выберите тип игрока {player_number} (human/comp): ").lower()
        if choice in ['human', 'comp']:
            return choice
        print("Неверный ввод. Пожалуйста, введите 'human' или 'comp'.")

# Ввод имени игрока
def enter_player_name(player_number):
    name = input(f"Введите имя для игрока {player_number}: ")
    return name if name else f"Игрок {player_number}"  # Если имя не введено, используем "Игрок N"

# Основная программа
if __name__ == "__main__":
    print("Добро пожаловать в игру Лото!")
    player1_type = select_player_type(1)
    player1_name = enter_player_name(1)
    player2_type = select_player_type(2)
    player2_name = enter_player_name(2)
    game = Game(player1_type, player2_type, player1_name, player2_name)
    game.start()
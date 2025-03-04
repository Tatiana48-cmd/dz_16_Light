
import unittest
from unittest.mock import patch, call
from io import StringIO
from main import PlayerHuman, Cart  # классы находятся в файле main.py

class TestPlayerHuman(unittest.TestCase):
    def setUp(self):
        # Создаем экземпляр PlayerHuman для тестирования
        self.player = PlayerHuman("Игрок")

        # Инициализируем карточку игрока
        self.player.cart.numbers = [5, 10, 15]
        self.player.cart.rows = [
            [5, '  ', '  ', '  ', 10],  # Первая строка: 2 числа и 3 пустые клетки
            ['  ', 15, '  ', '  ', '  ']  # Вторая строка: 1 число и 4 пустые клетки
        ]

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=['y'])
    def test_take_turn_correct_choice(self, mock_input, mock_stdout):
        # Проверяем, что игрок правильно зачеркивает число
        result = self.player.take_turn(5)

        # Проверяем вывод в консоль
        output = mock_stdout.getvalue().strip()
        self.assertIn("------ Карточка Игрок ------", output)

        # Проверяем, что input был вызван с правильным запросом
        mock_input.assert_called_once_with("Число 5 есть на вашей карточке? Зачеркнуть? (y/n): ")

        # Проверяем, что метод вернул True
        self.assertTrue(result)

        # Проверяем, что число зачеркнуто в карточке
        self.assertIn('--', self.player.cart.rows[0])  # Число 5 заменено на '--'

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=['n'])
    def test_take_turn_incorrect_choice(self, mock_input, mock_stdout):
        # Проверяем, что игрок проигрывает, если пропускает число
        result = self.player.take_turn(5)

        # Проверяем вывод в консоль
        output = mock_stdout.getvalue().strip()
        self.assertIn("------ Карточка Игрок ------", output)
        self.assertIn("Игрок, вы пропустили число, которое есть на вашей карточке. Вы проиграли!", output)

        # Проверяем, что input был вызван с правильным запросом
        mock_input.assert_called_once_with("Число 5 есть на вашей карточке? Зачеркнуть? (y/n): ")

        # Проверяем, что метод вернул False
        self.assertFalse(result)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=['y'])
    def test_take_turn_number_not_found(self, mock_input, mock_stdout):
        # Проверяем, что игрок проигрывает, если зачеркивает число, которого нет
        # Убираем число 5 из карточки
        self.player.cart.numbers = [10, 15]
        self.player.cart.rows = [['  ', '  ', '  ', '  ', 10], ['  ', 15, '  ', '  ', '  ']]

        result = self.player.take_turn(5)

        # Проверяем вывод в консоль
        output = mock_stdout.getvalue().strip()
        self.assertIn("------ Карточка Игрок ------", output)
        self.assertIn("Игрок, такого числа нет на вашей карточке. Вы проиграли!", output)

        # Проверяем, что input был вызван с правильным запросом
        mock_input.assert_called_once_with("Число 5 есть на вашей карточке? Зачеркнуть? (y/n): ")

        # Проверяем, что метод вернул False
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
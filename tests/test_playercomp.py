import unittest
from unittest.mock import patch
from io import StringIO
from main import PlayerComp, Cart  # классы находятся в файле main.py

class TestPlayerComp(unittest.TestCase):
    def setUp(self):
        # Создаем экземпляр PlayerComp для тестирования
        self.player = PlayerComp("Компьютер")

    def test_initialization(self):
        # Проверяем, что объект инициализируется корректно
        self.assertEqual(self.player.name, "Компьютер")
        self.assertIsInstance(self.player.cart, Cart)

    @patch('sys.stdout', new_callable=StringIO)
    def test_take_turn_number_found(self, mock_stdout):
        # Проверяем, что число найдено и зачеркнуто
        # Добавим число в карточку игрока
        self.player.cart.numbers = [5, 10, 15]  # Заменяем числа в карточке на известные
        self.player.cart.rows = [[5, '  ', '  ', '  ', 10], ['  ', 15, '  ', '  ', '  ']]

        # Вызываем метод take_turn
        result = self.player.take_turn(5)

        # Проверяем вывод в консоль
        output = mock_stdout.getvalue().strip()
        self.assertIn("Компьютер зачеркнул число 5", output)

        # Проверяем, что метод вернул True
        self.assertTrue(result)

        # Проверяем, что число зачеркнуто в карточке
        self.assertIn('--', self.player.cart.rows[0])  # Число 5 заменено на '--'

    @patch('sys.stdout', new_callable=StringIO)
    def test_take_turn_number_not_found(self, mock_stdout):
        # Проверяем, что число не найдено и игрок его пропустил
        # Добавим число в карточку игрока
        self.player.cart.numbers = [5, 10, 15]  # Заменяем числа в карточке на известные
        self.player.cart.rows = [[5, '  ', '  ', '  ', 10], ['  ', 15, '  ', '  ', '  ']]

        # Вызываем метод take_turn с числом, которого нет в карточке
        result = self.player.take_turn(20)

        # Проверяем вывод в консоль
        output = mock_stdout.getvalue().strip()
        self.assertIn("Компьютер пропустил число 20", output)

        # Проверяем, что метод вернул True
        self.assertTrue(result)

        # Проверяем, что карточка не изменилась
        self.assertNotIn('--', self.player.cart.rows[0])  # Ничего не зачеркнуто

if __name__ == '__main__':
    unittest.main()
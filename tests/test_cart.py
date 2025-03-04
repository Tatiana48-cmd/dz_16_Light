import unittest
import random
from unittest.mock import patch
from io import StringIO
from main import Cart

class TestCart(unittest.TestCase):

    def setUp(self):
        # Фиксируем случайные числа для повторяемости тестов
        random.seed(42)
        self.cart = Cart()

    def test_initialization(self):
        # Проверяем, что в карточке 15 уникальных чисел
        self.assertEqual(len(self.cart.numbers), 15)
        self.assertEqual(len(set(self.cart.numbers)), 15)

        # Проверяем, что числа отсортированы
        self.assertEqual(self.cart.numbers, sorted(self.cart.numbers))

        # Проверяем, что в каждой строке 5 чисел и 4 пустых клетки
        for row in self.cart.rows:
            self.assertEqual(len(row), 9)
            self.assertEqual(row.count('  '), 4)
            self.assertEqual(len([num for num in row if num != '  ']), 5)

    def test_mark_number(self):
        # Выбираем число, которое точно есть в карточке
        number_to_mark = self.cart.numbers[0]

        # Проверяем, что число успешно зачеркнуто
        self.assertTrue(self.cart.mark_number(number_to_mark))

        # Проверяем, что число заменено на '--'
        for row in self.cart.rows:
            if number_to_mark in row:
                self.assertEqual(row[row.index(number_to_mark)], '--')

        # Пробуем зачеркнуть число, которого нет в карточке
        self.assertFalse(self.cart.mark_number(100))

    def test_is_complete(self):
        # Проверяем, что карточка не завершена изначально
        self.assertFalse(self.cart.is_complete())

        # Зачеркиваем все числа в карточке
        for number in self.cart.numbers:
            self.cart.mark_number(number)

        # Проверяем, что карточка завершена
        self.assertTrue(self.cart.is_complete())

    @patch('sys.stdout', new_callable=StringIO)
    def test_display(self, mock_stdout):
        # Проверяем вывод карточки
        self.cart.display("Test Cart")
        output = mock_stdout.getvalue().strip()
        self.assertIn("Test Cart", output)
        self.assertIn('-' * 30, output)

if __name__ == '__main__':
    unittest.main()
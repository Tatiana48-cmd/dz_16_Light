import unittest
from unittest.mock import MagicMock, patch
import random

# Подключаем тестируемый класс
from main import Game, PlayerHuman, PlayerComp


class TestGame(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Фиксируем seed для предсказуемых тестов

    @patch("builtins.input", side_effect=["human", "Игрок 1", "comp", "Игрок 2"])
    def test_game_initialization(self, mock_input):
        game = Game()
        self.assertIsInstance(game.player1, PlayerHuman)
        self.assertIsInstance(game.player2, PlayerComp)
        self.assertEqual(game.player1.name, "Игрок 1")
        self.assertEqual(game.player2.name, "Игрок 2")
        self.assertEqual(len(game.barrels), 90)
        self.assertEqual(len(set(game.barrels)), 90)  # Проверка уникальности бочонков

    @patch.object(PlayerHuman, 'take_turn', return_value=True)
    @patch.object(PlayerComp, 'take_turn', return_value=True)
    def test_game_winner(self, mock_p2_turn, mock_p1_turn):
        game = Game()  # Создаем игру

        # Создаем мокнутые объекты cart после создания игры
        game.player1.cart = unittest.mock.Mock()
        game.player2.cart = unittest.mock.Mock()

        game.player1.cart.is_complete.return_value = True  # Победа первого игрока
        game.player2.cart.is_complete.return_value = False

        with patch("builtins.print") as mock_print:
            game.start()
            mock_print.assert_any_call("Поздравляем! Игрок 1 выиграл!")

    @patch("builtins.print")
    def test_game_end_when_player_loses(self, mock_print):
        # Создаем игру с явным указанием имени первого игрока
        game = Game(player1_type='human', player2_type='comp', player1_name="Иван")

        # Настраиваем mock для метода take_turn, чтобы первый игрок проиграл на первом ходу
        game.player1.take_turn = MagicMock(return_value=False)
        game.player2.take_turn = MagicMock(return_value=True)

        # Запускаем игру
        game.start()

        # Проверяем, что игра завершилась из-за проигрыша первого игрока
        mock_print.assert_any_call("Иван проиграл. Игра завершена.")


if __name__ == "__main__":
    unittest.main()
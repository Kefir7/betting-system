# app/strategy.py
from abc import ABC, abstractmethod

class WinCalculationStrategy(ABC):
    @abstractmethod
    def calculate(self, bet_amount: float, odds: float) -> float:
        pass

class NormalStrategy(WinCalculationStrategy):
    def calculate(self, bet_amount: float, odds: float) -> float:
        return bet_amount * odds

class VIPStrategy(WinCalculationStrategy):
    def calculate(self, bet_amount: float, odds: float) -> float:
        return bet_amount * odds * 1.05  # бонус 5%

# Пример использования
def calculate_win(user_type: str, bet_amount: float, odds: float):
    strategy = NormalStrategy() if user_type == "normal" else VIPStrategy()
    return strategy.calculate(bet_amount, odds)

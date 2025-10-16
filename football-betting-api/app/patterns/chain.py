# app/chain.py
from abc import ABC, abstractmethod

class Handler(ABC):
    def __init__(self, next_handler=None):
        self.next = next_handler    

    @abstractmethod
    def handle(self, user, bet_amount):
        if self.next:
            return self.next.handle(user, bet_amount)
        return True

class BalanceCheck(Handler):
    def handle(self, user, bet_amount):
        if user['balance'] < bet_amount:
            print("[Chain] Недостаточно средств")
            return False
        return super().handle(user, bet_amount)

class BetLimitCheck(Handler):
    def handle(self, user, bet_amount):
        if bet_amount > 1000:
            print("[Chain] Превышен лимит ставки")
            return False
        return super().handle(user, bet_amount)

# Использование
def place_bet(user, bet_amount):
    chain = BalanceCheck(BetLimitCheck())
    if chain.handle(user, bet_amount):
        print(f"[Chain] Ставка пользователя {user['id']} принята")
    else:
        print(f"[Chain] Ставка пользователя {user['id']} отклонена")

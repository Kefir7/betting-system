# app/observer.py
from typing import List, Protocol

class Observer(Protocol):
    def update(self, match_id: int, score: str):
        ...

class MatchSubject:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, match_id: int, score: str):
        for observer in self._observers:
            observer.update(match_id, score)

# Пример подписчика
class BettingService:
    def update(self, match_id: int, score: str):

        print(f"[Observer] Матч {match_id} обновлён. Новый счёт: {score}")

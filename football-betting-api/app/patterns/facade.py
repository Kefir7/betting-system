from .observer import MatchSubject, BettingService
from .strategy import calculate_win
from .chain import place_bet
from .adapter import PaymentAdapter, OldPaymentSystem
from app import crud
from contextlib import contextmanager
from app.db import SessionLocal

subject = MatchSubject()
subject.attach(BettingService())

@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class BettingFacade:
    def __init__(self):
        self.subject = subject

    def update_match_score(self, match_id: int, new_score: str, user: dict, bet_amount: float, odds: float):
        # 1. Обновляем матч в БД
        with get_session() as db:
            match = crud.get_match(db, match_id)
            if match:
                match.home_goals, match.away_goals = map(int, new_score.split(":"))
                if match.home_goals > match.away_goals:
                    match.result = "HOME"
                elif match.home_goals < match.away_goals:
                    match.result = "AWAY"
                else:
                    match.result = "DRAW"
                db.commit()

        print(f"[Facade] Матч {match_id} обновлен с результатом {new_score}")

        # 2. Observer
        self.subject.notify(match_id, new_score)

        # 3. Chain of Responsibility
        if not place_bet(user, bet_amount):
            return "Ставка отклонена"

        # 4. Strategy
        win = calculate_win(user.get("type", "normal"), bet_amount, odds)
        print(f"[Facade] Возможный выигрыш пользователя {user['id']}: {win}")

        # 5. Adapter
        old_system = OldPaymentSystem()
        adapter = PaymentAdapter(old_system)
        adapter.pay(user, win)

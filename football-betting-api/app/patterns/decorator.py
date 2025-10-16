from functools import wraps
from .chain import place_bet

def log_action(func):
    """Декоратор для логирования действий"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[Decorator] Выполняется: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def auth_required(func):
    """Пример проверки авторизации"""
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        if not user.get("is_authenticated"):
            print("[Decorator] Пользователь не авторизован")
            return None
        return func(user, *args, **kwargs)
    return wrapper

# Пример использования
@log_action
@auth_required
def make_bet(user, match_id, amount):
    print(f"[Bet] Пользователь {user['id']} делает ставку на матч {match_id} на сумму {amount}")

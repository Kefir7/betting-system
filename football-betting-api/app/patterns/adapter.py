class OldPaymentSystem:
    """Сторонняя система оплаты, интерфейс которой неудобен для проекта"""
    def make_transaction(self, user_id, amount):
        print(f"[OldPayment] Транзакция: {user_id}, сумма: {amount}")

class PaymentAdapter:
    """
    Адаптер преобразует старый интерфейс в нужный нам формат
    """
    def __init__(self, old_system: OldPaymentSystem):
        self.old_system = old_system

    def pay(self, user, amount):
        user_id = user.get("id")
        self.old_system.make_transaction(user_id, amount)
        print("[Adapter] Оплата прошла через адаптер")

# Пример использования
def process_payment(user, amount):
    old_system = OldPaymentSystem()
    adapter = PaymentAdapter(old_system)
    adapter.pay(user, amount)

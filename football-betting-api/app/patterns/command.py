# app/command.py
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class FetchMatchesCommand(Command):
    def execute(self):
        print("[Command] Получаем новые матчи с API")
        # Здесь можно вызывать функцию обновления матчей и записывать в БД

class Scheduler:
    def __init__(self):
        self.commands = []

    def add_command(self, command: Command):
        self.commands.append(command)

    def run(self):
        for cmd in self.commands:
            cmd.execute()

# Использование
scheduler = Scheduler()
scheduler.add_command(FetchMatchesCommand())
scheduler.run()

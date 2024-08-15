"""Модуль для роботи з Нотатками"""


from datetime import datetime


class Notes:
    """Клас для зберігання Нотаток"""
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.created_at = datetime.now()

    def __str__(self):
        return f"{self.title}: {self.content}"


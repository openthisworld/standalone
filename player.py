class Player:
    def __init__(self, user_id):
        self.user_id = user_id
        self.name = ""
        self.faction = ""
        self.state = "waiting_for_name"
        self.health = 100
        self.commands = []  # Список команд гравця
        self.standalone_responses = []  # Список відповідей моделі
        self.messages = []  # Список повідомлень гравця

    def rest(self):
        self.health += 20
        if self.health > 100:
            self.health = 100

    # Додайте інші методи гравця за потреби

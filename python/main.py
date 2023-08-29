from character import Character
from plot_generator import generate_plot
from action_generator import generate_actions

class Game:
    def __init__(self):
        self.character = None
        self.actions_history = []
    
    def start(self):
        print("Ласкаво просимо до Текстової РПГ у світі S.T.A.L.K.E.R.!")
        character_name = input("Введіть ім'я персонажа: ")
        character_faction = input("Оберіть фракцію (Обов'язок, Воля, тощо): ")

        self.character = Character(character_name, character_faction)
        print(f"Ласкаво просимо, {self.character.name} з фракції {self.character.faction}!")

        while True:
            plot = generate_plot(self.character)
            self.print_long_text(plot)

            actions = generate_actions()
            print("Ваші дії:")
            for idx, action in enumerate(actions, start=1):
                print(f"{idx}. {action}")

            choice = input("Введіть номер вашого вибору: ")
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(actions):
                    chosen_action = actions[choice_idx]
                    print(f"Ви обрали: {chosen_action}")
                    self.actions_history.append(chosen_action)
                    self.perform_action(chosen_action)

                else:
                    print("Неправильний вибір. Будь ласка, введіть правильний номер.")

            except ValueError:
                print("Невірний ввід. Будь ласка, введіть число.")
    
    def perform_action(self, action):
        # Реалізуйте логіку виконання дій тут
        pass

    def print_long_text(self, text):
        lines = text.split("\n")
        for line in lines:
            print(line)
            input("Продовжити...")

if __name__ == "__main__":
    game = Game()
    game.start()

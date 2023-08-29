# game_logic.py

import openai

# Клас Player та його методи

# Змінні для зберігання та керування діалогами гравців
players = {}

# Інші імпорти та функції

# Ваш код для генерації відповіді від ChatGPT
def generate_gpt_response(prompt):
    openai.api_key = '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'
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=100,
        stop=None
    )
    return response.choices[0].text.strip()

# Функція для генерації сюжетного блоку
def generate_story_block(player, story_context):
    context = "\n".join(story_context)
    
    if player.faction == "Свобода":
        prompt = f"Гравець {player.name} з фракції Свобода. В минулому він {context}."
    # Додайте код для інших фракцій
    
    gpt_response = generate_gpt_response(prompt)
    return gpt_response + "\n\nЩо ви будете робити?\n" + generate_action_options(player.available_choices)


# Функція для генерації варіантів дій
def generate_action_options(options):
    formatted_options = "\n".join([f"{i+1}. {option}" for i, option in enumerate(options)])
    return formatted_options

# Функція для обробки вибору гравця та генерації наступного сюжетного блоку
def handle_player_choice(player, choice, story_context):
    response = ""

    if player.awaiting_choice:
        if choice in player.available_choices:
            story_context.append(choice)
            next_story_block = generate_story_block(player, story_context)
            response = next_story_block
        else:
            response = "Будь ласка, оберіть один із доступних варіантів."

    return player, response

# Оновлення контексту діалогу гравця
def update_dialogue(player, message, response):
    player.messages.append({"message": message, "response": response})

# ... решта коду ...

# Цей блок служить для тестування вашої логіки гри
if __name__ == "__main__":
    user_id = "test_user"  # Змініть на дійсний ідентифікатор користувача
    example_message = "дослідити печеру"  # Змініть на дійсний ввід користувача
    player = players.setdefault(user_id, Player(user_id))
    player, response = handle_message(example_message, user_id)
    print("Гравець:", example_message)
    print("Відповідь:", response)

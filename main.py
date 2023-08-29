import telebot
import openai

# Конфігурації
BOT_TOKEN = '6504314249:AAHqLEfvAXlP76l0AqxGvZ6MNmhw36YIP0o'
OPENAI_API_KEY = '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'

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

class Player:
    def __init__(self, user_id):
        self.user_id = user_id
        self.name = None
        self.faction = None
        self.story_context = []
        self.available_choices = []
        self.awaiting_choice = False

players = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    players[user_id] = Player(user_id)
    bot.send_message(message.chat.id, "Ласкаво просимо до гри 'Standalone'!\nБудь ласка, назвіть свого персонажа:")

@bot.message_handler(func=lambda message: players.get(str(message.from_user.id)) and not players[str(message.from_user.id)].name)
def set_name(message):
    user_id = str(message.from_user.id)
    players[user_id].name = message.text
    factions = ["Свобода", "Долина", "Оселедець", "Моноліт", "Бандити", "Науковці", "Вільні Сталкери", "Торговці", "Обов'язок", "Мутанти"]
    factions_text = "\n".join([f"{i + 1}. {faction}" for i, faction in enumerate(factions)])
    bot.send_message(message.chat.id, f"{players[user_id].name}, тепер виберіть фракцію, до якої ваш персонаж буде належати:\n{factions_text}")

@bot.message_handler(func=lambda message: players.get(str(message.from_user.id)) and not players[str(message.from_user.id)].faction)
def set_faction(message):
    user_id = str(message.from_user.id)
    players[user_id].faction = message.text
    bot.send_message(message.chat.id, f"{players[user_id].name}, ви обрали фракцію: {players[user_id].faction}\nПочинаємо генерацію сюжету гри!\n"
                                      f"Натисніть кнопку 'Поїхали', щоб розпочати гру.")

@bot.message_handler(func=lambda message: players.get(str(message.from_user.id)) and message.text == "Поїхали")
def start_game(message):
    user_id = str(message.from_user.id)
    player = players[user_id]
    player.awaiting_choice = True
    generate_story(player)

@bot.message_handler(func=lambda message: players.get(str(message.from_user.id)) and players[str(message.from_user.id)].awaiting_choice)
def handle_choice(message):
    user_id = str(message.from_user.id)
    player = players[user_id]
    
    if message.text in player.available_choices:
        choice = message.text
        player.story_context.append(choice)
        generate_story(player)
    else:
        bot.send_message(message.chat.id, "Будь ласка, оберіть один із доступних варіантів.")

def generate_story(player):
    context = "\n".join(player.story_context)
    
    if player.faction == "Свобода":
        prompt = f"Гравець {player.name} з фракції Свобода. В минулому він {context}."
    elif player.faction == "Долина":
        prompt = f"Гравець {player.name} з фракції Долина. В минулому він {context}."
    elif player.faction == "Оселедець":
        prompt = f"Гравець {player.name} з фракції Оселедець. В минулому він {context}."
    elif player.faction == "Моноліт":
        prompt = f"Гравець {player.name} з фракції Моноліт. В минулому він {context}."
    elif player.faction == "Бандити":
        prompt = f"Гравець {player.name} з фракції Бандити. В минулому він {context}."
    elif player.faction == "Науковці":
        prompt = f"Гравець {player.name} з фракції Науковці. В минулому він {context}."
    elif player.faction == "Вільні Сталкери":
        prompt = f"Гравець {player.name} з фракції Вільні Сталкери. В минулому він {context}."
    elif player.faction == "Торговці":
        prompt = f"Гравець {player.name} з фракції Торговці. В минулому він {context}."
    elif player.faction == "Обов'язок":
        prompt = f"Гравець {player.name} з фракції Обов'язок. В минулому він {context}."
    elif player.faction == "Мутанти":
        prompt = f"Гравець {player.name} - мутант. В минулому він {context}."
    
    gpt_response = generate_gpt_response(prompt)
    choices = generate_action_options(player.available_choices)
    bot.send_message(player.user_id, f"{gpt_response}\n\nЩо ви будете робити?\n{choices}")

    
    gpt_response = generate_gpt_response(prompt)
    choices = generate_action_options(player.available_choices)
    bot.send_message(player.user_id, f"{gpt_response}\n\nЩо ви будете робити?\n{choices}")
    
def generate_gpt_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,

def generate_action_options(options):
    formatted_options = "\n".join([f"{i+1}. {option}" for i, option in enumerate(options)])
    return formatted_options
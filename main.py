# main.py

import game_logic
import openai_integration
import telebot
from telebot import types

# Ваш API-ключ бота від BotFather
BOT_TOKEN = '6504314249:AAHqLEfvAXlP76l0AqxGvZ6MNmhw36YIP0o'

bot = telebot.TeleBot(BOT_TOKEN)

# Створення клавіатури для вибору фракції
def create_faction_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Обовʼязок'))
    keyboard.add(types.KeyboardButton('Вільні Сталкери'))
    keyboard.add(types.KeyboardButton('Торговці'))
    keyboard.add(types.KeyboardButton('Свобода'))
    return keyboard

# Обробник команди /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    game_logic.players[user_id] = {'state': 'choosing_name'}
    bot.reply_to(message, "Ласкаво просимо до гри 'Standalone'!\nБудь ласка, виберіть ім'я свого персонажа:")

# Обробник текстових повідомлень
@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    user_id = str(message.from_user.id)
    player_data = game_logic.players.setdefault(user_id, {})
    user_input = message.text

    if player_data.get('state') == 'choosing_name':
        player_data['name'] = user_input
        player_data['state'] = 'choosing_faction'
        bot.reply_to(message, f"Добре, ви обрали ім'я: {user_input}\nТепер будь ласка, виберіть фракцію:",
                     reply_markup=create_faction_keyboard())
    elif player_data.get('state') == 'choosing_faction':
        player_data['faction'] = user_input
        player_data['state'] = 'playing'
        bot.reply_to(message, f"Ви обрали фракцію: {user_input}\nПочинаємо генерацію сюжету гри!")

        # Генерація першого блоку сюжету та виведення його користувачу
        response = openai_integration.generate_story_block(player_data)
        bot.reply_to(message, response)

# Реагування на кнопки вибору дії
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_start_button(message):
    user_id = str(message.from_user.id)
    player_data = game_logic.players.setdefault(user_id, {})
    user_input = message.text

    if player_data.get('state') == 'waiting_for_start' and user_input == 'Поїхали':
        player_data['state'] = 'playing'
        bot.reply_to(message, "Починаємо генерацію сюжету гри!")

        # Генерація першого блоку сюжету та виведення його користувачу
        response = openai_integration.generate_story_block(player_data)
        bot.reply_to(message, response)

        # Вивід варіантів дій
        options = game_logic.get_current_options(player_data)
        options_text = "\n".join([f"{index + 1}. {option}" for index, option in enumerate(options)])
        bot.reply_to(message, f"Що ви будете робити?\n{options_text}")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_action_choice(message):
    user_id = str(message.from_user.id)
    player_data = game_logic.players.setdefault(user_id, {})
    user_input = message.text

    if player_data.get('state') == 'playing' and user_input.isdigit():
        action_index = int(user_input) - 1
        options = game_logic.get_current_options(player_data)
        if 0 <= action_index < len(options):
            player_data['state'] = 'playing'
            response = openai_integration.generate_story_block(player_data, action_choice=options[action_index])
            bot.reply_to(message, response)

            # Вивід нових варіантів дій
            new_options = game_logic.get_current_options(player_data)
            new_options_text = "\n".join([f"{index + 1}. {option}" for index, option in enumerate(new_options)])
            bot.reply_to(message, f"Що ви будете робити далі?\n{new_options_text}")


def main():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()





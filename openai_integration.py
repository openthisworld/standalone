import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_response(dialogue):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=dialogue,
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].text.strip()


def generate_dialogue(player_name, player_messages, standalone_responses):
    dialogue = f"{player_name}:\n"
    for message, response in zip(player_messages, standalone_responses):
        dialogue += f"Player: {message}\nStandalone: {response}\n"
    return dialogue

def generate_story(player):
    dialogue = generate_dialogue(player.name, player.messages, player.standalone_responses)
    response = generate_response(dialogue)
    return response

def update_dialogue(player, message, response):
    player.messages.append(message)
    player.standalone_responses.append(response)
    if len(player.messages) > 4:  # Обмежити кількість повідомлень у діалозі
        player.messages.pop(0)
        player.standalone_responses.pop(0)

def generate_story_block(player_data):
    player = player_data["player"]
    story_context = player_data["story_context"]
    return game_logic.generate_story_block(player, story_context)  # Використовуємо функцію з game_logic


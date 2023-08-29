import openai

def generate_actions():
    openai.api_key = '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'  # Потрібно замінити на реальний ключ

    prompt = "Продовжити сюжет після попереднього блоку тексту. Ваші дії:"
    response = openai.Completion.create(
        engine="text-davinci-003",  # Виберіть відповідний engine
        prompt=prompt,
        max_tokens=150,  # Максимальна кількість токенів у відповіді
        temperature=0.7,  # Вплив на різноманітність генерованих дій
        n=4  # Кількість генерованих варіантів дій
    )
    
    actions = [choice.text.strip() for choice in response.choices]
    return actions
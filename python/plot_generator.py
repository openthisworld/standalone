import openai

def generate_plot(character):
    openai.api_key = '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'  # Потрібно замінити на реальний ключ

    prompt = f"Згенерувати сюжет для персонажа {character.name} з фракції {character.faction} у світі S.T.A.L.K.E.R."
    response = openai.Completion.create(
        engine="text-davinci-003",  # Виберіть відповідний engine
        prompt=prompt,
        max_tokens=150  # Максимальна кількість токенів у відповіді
    )
    
    plot = response.choices[0].text.strip()
    return plot

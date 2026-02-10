import requests
import json
import os
from datetime import date
import random

API_KEY = os.environ["MISTRAL_API_KEY"]

def generate_words():
    prompt = """
Génère 8 mots français adaptés à des seniors (culture générale).
Retourne un JSON strict :
[
  {"word": "...", "clue": "..."},
  ...
]
Les mots doivent faire entre 4 et 8 lettres.
"""

    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistral-small",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
    )

    content = response.json()["choices"][0]["message"]["content"]
    return json.loads(content)

def create_cross_grid(words):
    size = 10
    grid = [["#" for _ in range(size)] for _ in range(size)]

    center = size // 2
    main_word = words[0]["word"].upper()

    # Place main horizontal word
    start_col = center - len(main_word)//2
    for i, letter in enumerate(main_word):
        grid[center][start_col + i] = letter

    placed = [words[0]]

    # Place vertical words crossing main word
    for w in words[1:]:
        word = w["word"].upper()
        for i, letter in enumerate(word):
            for j, main_letter in enumerate(main_word):
                if letter == main_letter:
                    row = center - i
                    col = start_col + j
                    if 0 <= row and row + len(word) <= size:
                        for k, l in enumerate(word):
                            grid[row + k][col] = l
                        placed.append(w)
                        break
            if w in placed:
                break

    clues = []
    for idx, w in enumerate(placed):
        clues.append(f"{idx+1}. {w['clue']}")

    return grid, clues

words = generate_words()
grid, clues = create_cross_grid(words)

data = {
    "date": str(date.today()),
    "grid": grid,
    "clues": clues
}

with open("data.json", "w") as f:
    json.dump(data, f)

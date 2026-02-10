import os
import json
import random
import requests
from datetime import date

API_KEY = os.environ.get("MISTRAL_API_KEY")

if not API_KEY:
    print("❌ ERROR: MISTRAL_API_KEY not set!")
    exit(1)

def generate_words():
    prompt = """
    Génère un JSON strict avec 5 mots + définitions en français :
    [
      {"word":"CHAT", "clue":"Animal domestique"},
      ...
    ]
    Mots de 4 à 8 lettres maximum.
    """

    try:
        resp = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistral-small-latest",
                "messages": [
                    {"role":"user","content":prompt}
                ],
                "temperature": 0.7
            },
            timeout=30
        )

        print("HTTP status:", resp.status_code)
        print("Response text:", resp.text)

        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        words = json.loads(content)
        return words

    except Exception as e:
        print("❌ API ERROR:", e)
        print("Using fallback words.")
        return [
            {"word":"CHAT","clue":"Animal domestique"},
            {"word":"MAISON","clue":"Lieu d'habitation"},
            {"word":"MER","clue":"Grande étendue d'eau salée"},
            {"word":"LIVRE","clue":"Objet qu’on lit"},
            {"word":"ARBRE","clue":"Plante avec un tronc"}
        ]

def build_grid(words):
    size = 10
    grid = [["#" for _ in range(size)] for _ in range(size)]

    main = words[0]["word"].upper()
    center = size // 2
    start = center - len(main) // 2

    for i, letter in enumerate(main):
        grid[center][start+i] = letter

    clues = [f"1. {words[0]['clue']}"]
    return grid, clues

words = generate_words()
grid, clues = build_grid(words)

out = {
    "date": str(date.today()),
    "grid": grid,
    "clues": clues
}

with open("data.json","w") as f:
    json.dump(out,f)
print("✅ data.json written")

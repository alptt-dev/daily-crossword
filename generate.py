import os
import json
import requests
from datetime import date

API_KEY = os.environ.get("MISTRAL_API_KEY")

if not API_KEY:
    raise Exception("MISTRAL_API_KEY manquante")

PROMPT = """
Génère STRICTEMENT un JSON valide avec 6 mots croisés en français :

Format exact :
[
  {"word":"CHAT","clue":"Animal domestique"},
  {"word":"MER","clue":"Grande étendue d'eau salée"}
]

Contraintes :
- Mots entre 4 et 8 lettres
- Culture générale senior
- Pas de texte autour
"""

def generate_words():
    r = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistral-small-latest",
            "messages":[{"role":"user","content":PROMPT}],
            "temperature":0.7
        },
        timeout=30
    )

    r.raise_for_status()

    content = r.json()["choices"][0]["message"]["content"]
    return json.loads(content)

def build_grid(words):
    size = 10
    grid = [["#" for _ in range(size)] for _ in range(size)]

    center = size // 2
    main = words[0]["word"].upper()
    start = center - len(main)//2

    for i,l in enumerate(main):
        grid[center][start+i] = l

    clues = [f"{i+1}. {w['clue']}" for i,w in enumerate(words)]

    return grid, clues

words = generate_words()
grid, clues = build_grid(words)

data = {
    "date": str(date.today()),
    "grid": grid,
    "clues": clues
}

with open("data.json","w") as f:
    json.dump(data,f)

import random
import json
from datetime import date

words = [
    ("CHAT", "Animal domestique"),
    ("MAISON", "Lieu d'habitation"),
    ("SOLEIL", "Étoile du système solaire"),
    ("LIVRE", "On le lit"),
    ("MER", "Grande étendue d'eau salée")
]

def create_grid():
    size = 7
    grid = [["#" for _ in range(size)] for _ in range(size)]

    selected = random.sample(words, 3)

    row = 1
    clues = []

    for word, clue in selected:
        for i, letter in enumerate(word):
            grid[row][i+1] = letter
        clues.append(f"{row}. {clue}")
        row += 2

    return grid, clues

grid, clues = create_grid()

data = {
    "date": str(date.today()),
    "grid": grid,
    "clues": clues
}

with open("data.json", "w") as f:
    json.dump(data, f)

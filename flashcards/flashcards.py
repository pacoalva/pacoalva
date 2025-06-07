import json
import os
import random


def load_flashcards(path: str):
    """Load flashcards from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_quiz(flashcards):
    """Run an interactive flashcard quiz."""
    print("Bienvenido al sistema de tarjetas de estudio")
    print("Presiona ENTER para ver la respuesta y 'q' para salir.\n")
    random.shuffle(flashcards)
    for card in flashcards:
        print("Pregunta: " + card["question"])
        input("Tu respuesta (presiona ENTER para mostrar la respuesta)")
        print("Respuesta: " + card["answer"])
        cont = input("Pulsa ENTER para continuar o 'q' para salir: ")
        if cont.lower().startswith("q"):
            break


def main():
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, "data", "flashcards.json")
    flashcards = load_flashcards(data_path)
    run_quiz(flashcards)


if __name__ == "__main__":
    main()

# Flashcard App

This repository contains a simple graphical flashcard application implemented in Python using `tkinter` and an SQLite database.

## Features

- Import cards from CSV files.
- Select cards by topic.
- Shuffle cards automatically.
- Track correct and incorrect answers for each card.
- View overall statistics.

## Requirements

- Python 3.x

The application uses only the Python standard library so no additional packages are required.

## Running the application

```bash
python flashcards.py
```

The first run will create a `flashcards.db` database in the project directory. You can import example cards using `sample_cards.csv` via the **File > Import CSV** menu.

## CSV Format

CSV files should contain the following headers:

```
question,answer,topic
```

Each row represents a flashcard. The `topic` field is optional and can be used to filter cards via the **Topics** menu.

import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import random

DB_NAME = 'flashcards.db'

# Database functions

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                topic TEXT,
                correct_count INTEGER DEFAULT 0,
                wrong_count INTEGER DEFAULT 0
            )"""
    )
    conn.commit()
    conn.close()


def import_csv(path):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            c.execute(
                "INSERT INTO cards(question, answer, topic) VALUES (?, ?, ?)",
                (row.get('question'), row.get('answer'), row.get('topic')),
            )
    conn.commit()
    conn.close()


def get_cards(topic=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if topic:
        c.execute("SELECT * FROM cards WHERE topic=?", (topic,))
    else:
        c.execute("SELECT * FROM cards")
    cards = c.fetchall()
    conn.close()
    random.shuffle(cards)
    return cards


def update_stats(card_id, correct):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if correct:
        c.execute(
            "UPDATE cards SET correct_count = correct_count + 1 WHERE id=?",
            (card_id,),
        )
    else:
        c.execute(
            "UPDATE cards SET wrong_count = wrong_count + 1 WHERE id=?",
            (card_id,),
        )
    conn.commit()
    conn.close()


class FlashcardApp:
    def __init__(self, master):
        self.master = master
        master.title('Flashcards')
        self.cards = []
        self.current = None

        self.frame = tk.Frame(master, padx=20, pady=20)
        self.frame.pack()

        self.question_label = tk.Label(self.frame, text='', font=('Arial', 16))
        self.question_label.pack(pady=10)

        self.answer_button = tk.Button(
            self.frame, text='Show Answer', command=self.show_answer
        )
        self.answer_button.pack(pady=5)

        self.result_label = tk.Label(self.frame, text='', font=('Arial', 14))
        self.result_label.pack(pady=10)

        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(pady=5)

        self.correct_button = tk.Button(
            self.button_frame, text='Correct', command=lambda: self.next_card(True)
        )
        self.correct_button.grid(row=0, column=0, padx=5)

        self.wrong_button = tk.Button(
            self.button_frame, text='Incorrect', command=lambda: self.next_card(False)
        )
        self.wrong_button.grid(row=0, column=1, padx=5)

        self.menu = tk.Menu(master)
        master.config(menu=self.menu)
        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Import CSV', command=self.import_cards)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=master.quit)

        stats_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Stats', menu=stats_menu)
        stats_menu.add_command(label='Show Stats', command=self.show_stats)

        topic_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Topics', menu=topic_menu)
        topic_menu.add_command(label='All', command=lambda: self.load_cards())
        self.topic_menu = topic_menu

        self.load_topics()
        self.load_cards()

    def load_topics(self):
        self.topic_menu.delete(1, 'end')
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT DISTINCT topic FROM cards WHERE topic IS NOT NULL")
        topics = [row[0] for row in c.fetchall() if row[0]]
        conn.close()
        for t in topics:
            self.topic_menu.add_command(
                label=t, command=lambda topic=t: self.load_cards(topic)
            )

    def load_cards(self, topic=None):
        self.cards = get_cards(topic)
        if not self.cards:
            self.question_label.config(text='No cards available')
            self.answer_button.config(state='disabled')
            self.correct_button.config(state='disabled')
            self.wrong_button.config(state='disabled')
        else:
            self.answer_button.config(state='normal')
            self.correct_button.config(state='normal')
            self.wrong_button.config(state='normal')
            self.current_index = 0
            self.show_card()

    def show_card(self):
        if not self.cards:
            return
        self.current = self.cards[self.current_index]
        self.question_label.config(text=self.current[1])
        self.result_label.config(text='')
        self.answer_button.config(state='normal')

    def show_answer(self):
        if self.current:
            self.result_label.config(text=self.current[2])
            self.answer_button.config(state='disabled')

    def next_card(self, correct):
        if self.current:
            update_stats(self.current[0], correct)
            self.current_index += 1
            if self.current_index >= len(self.cards):
                messagebox.showinfo('Done', 'No more cards.')
                self.load_cards()
            else:
                self.show_card()

    def import_cards(self):
        path = filedialog.askopenfilename(
            title='Select CSV file',
            filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
        )
        if path:
            try:
                import_csv(path)
                self.load_topics()
                self.load_cards()
                messagebox.showinfo('Import', 'Cards imported successfully.')
            except Exception as e:
                messagebox.showerror('Error', str(e))

    def show_stats(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "SELECT SUM(correct_count), SUM(wrong_count) FROM cards"
        )
        correct, wrong = c.fetchone()
        conn.close()
        correct = correct or 0
        wrong = wrong or 0
        total = correct + wrong
        msg = f'Total answers: {total}\nCorrect: {correct}\nIncorrect: {wrong}'
        messagebox.showinfo('Stats', msg)


if __name__ == '__main__':
    init_db()
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()

#!/home/mrdiz/anaconda3/bin/python
# -*- coding: utf-8 -*-

import csv
import math
import random
import tkinter as tk
import tkinter.messagebox as tkMessageBox
from PIL import Image, ImageTk

class Window(tk.Frame):
    """
    Класс, отвечающий за прорисовку окна. Создает рамку внутри главного окна master.
    master - главное окно, self - контейнер внутри
    """

    def __init__(self, master=None):
        """master - указатель на главное окно"""

        tk.Frame.__init__(self, master)  # конструктор базового класса, создающий рамку

        self.master = master

        # Загаданное слово
        self.wordLabel = tk.Label(self, text=Word.show_word())

        # Описание слова
        self.wordDesc = tk.Label(self, text=Word.description)

        # Очки на барабане
        self.scoreText = GameManager.select_score() + " очков на барабане!"
        self.scoreLabel = tk.Label(self, text=self.scoreText)

        # Отслеживание текста в textbox
        self.textLabelValue = tk.StringVar(self)
        self.textLabelValue.trace('w', self.limit_wordLabel)

        # Поле ввода
        self.textbox = tk.Entry(self, textvariable=self.textLabelValue)

        # Алфавит
        self.alphabetLabel = tk.Label(self, text=GameManager.get_alphabet())

        # Набранные очки
        self.playerScoreText = "Набранные очки: " + GameManager.get_playerScore()
        self.playerScoreLabel = tk.Label(self, text=self.playerScoreText)

        # Виджеты для ИИ
        # Счёт ИИ

        self.aiScoreText = "Счёт ИИ: " + GameManager.get_aiScore()
        self.aiScoreLabel = tk.Label(self, text=self.aiScoreText)

        # Названная ИИ буква
        self.aiLetterText = ""
        self.aiLetterLabel = tk.Label(self, text=self.aiLetterText)

        self.init_window()
        self.bind_events()

    # Методы инициализации

    def init_window(self):
        self.master.title("Field Of Wonders")
        self.pack(fill=tk.BOTH, expand=True)

        self.init_menu()
        self.config_widgets()

        self.show_logo()
        self.init_buttons()
        self.show_word()

        self.draw_sep()
        self.show_score()
        self.draw_sep()

        self.init_textbox()

        self.show_alphabet()

        self.show_playerscore()
        self.show_aiScore()

        self.show_aiLetter()

    def config_widgets(self):
        self.wordLabel.configure(font=("Arial", 18, "bold"))
        self.wordDesc.configure(font=("Arial", 10, "normal"), wraplength=460)
        self.scoreLabel.configure(font=("Arial", 12, "bold"))
        self.alphabetLabel.configure(font=("Arial", 10, "normal"), wraplength=460, pady=10)
        self.playerScoreLabel.configure(font=("Arial", 10, "normal"), pady=5)
        self.aiScoreLabel.configure(font=("Arial", 10, "normal"), pady=5)
        self.aiLetterLabel.configure(font=("Arial", 10, "normal"), pady=20)

    def bind_events(self):
        self.textbox.bind('<Return>', self.make_turn)
        self.bind('<Key>', self.textbox.focus_force())

    # Создание виджетов

    def init_menu(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        file = tk.Menu(menu)
        file.add_command(label="Новая игра", command=self.start_new)
        file.add_separator()
        file.add_command(label="Выход", command=self.close_window)

        menu.add_cascade(label="Файл", menu=file)

    def show_logo(self):
        load = Image.open("logo.png")
        render = ImageTk.PhotoImage(load)

        logo = tk.Label(self, image=render)
        logo.image = render
        logo.pack(side='top')

    def init_buttons(self):
        attemptButton = tk.Button(self, text="Назвать букву", command=self.make_turn)
        attemptButton.pack(side="bottom", pady=10)

    def show_word(self):
        textLabel = tk.Label(self, text='Слово')
        textLabel.configure(font=("Arial", 12, "bold"))

        textLabel.pack(side="top")
        self.wordLabel.pack(side="top", pady=10)
        self.wordDesc.pack(side="top", pady=5)

    def init_textbox(self):
        textboxLabel = tk.Label(self, text="Буква")
        textboxLabel.configure(font=("Arial", 12, "normal"))

        self.textbox.configure(font=("Arial", 20, "normal"),  width=2)

        textboxLabel.pack(side="top", pady=5)
        self.textbox.pack(side="top", pady=5)

    def show_score(self):
        self.scoreLabel.pack(side="top")

    def show_alphabet(self):
        self.alphabetLabel.pack(side="top")

    def draw_sep(self):
        sepLabel = tk.Label(self, text='-' * 65)
        sepLabel.pack(side="top", pady=5)

    def show_playerscore(self):
        self.playerScoreLabel.pack(side="bottom")

    def show_aiScore(self):
        self.aiScoreLabel.pack(side="bottom")

    def show_aiLetter(self):
        self.aiLetterLabel.pack(side="bottom")

    # Методы для управления

    def close_window(self):
        exit()

    def update_info(self):
        self.wordLabel.configure(text=Word.show_word())
        self.textLabelValue.set("")

        self.wordDesc.configure(text=Word.description)

        self.alphabetLabel.configure(text=GameManager.get_alphabet())

        self.playerScoreText = "Набранные очки: " + GameManager.get_playerScore()
        self.playerScoreLabel.configure(text=self.playerScoreText)

        self.aiScoreText = "Счёт ИИ: " + GameManager.get_aiScore()
        self.aiScoreLabel.configure(text=self.aiScoreText)

        self.aiLetterText = ""
        self.aiLetterLabel.configure(text=self.aiLetterText)

        self.scoreText = GameManager.select_score() + " очков на барабане!"
        self.scoreLabel.configure(text=self.scoreText)

    def make_turn(self, event=None):

        if not GameManager.endOfGame:
            letter = self.textbox.get().lower()

            # если русская буква
            if letter in GameManager.alpVerify:
                if GameManager.check_input(letter):

                    GameManager.check_isEnd()

                    if not GameManager.endOfGame:

                        letterAI = GameManager.ai_letterSelect()

                        aiSelScore = GameManager.select_score()
                        GameManager.ai_checkLetter(letterAI)

                        self.update_info()

                        self.aiLetterText = "ИИ крутит барабан.\n" \
                                        "На барабане {0} очков.\n" \
                                        "ИИ называет букву \"{1}\"".format(aiSelScore, letterAI)
                        self.aiLetterLabel.configure(text=self.aiLetterText)

                    GameManager.check_isEnd()

                    if GameManager.endOfGame:
                        header, text = GameManager.choose_winner()
                        if tkMessageBox.askyesno(header, text + "\n\nНачать новую игру?"):
                            self.start_new()
                else:
                    self.textLabelValue.set("")
            else:
                self.textLabelValue.set("")
                tkMessageBox.showerror("Ошибка*", "Введите букву русского алфавита!")
        else:
            self.textLabelValue.set("")
            tkMessageBox.showinfo("", "Игра окончена!")

    def start_new(self):
        GameManager.start_new()
        self.update_info()

    def limit_wordLabel(self, *args):
        value = self.textLabelValue.get()
        if len(value) > 1:
            self.textLabelValue.set(value[:1])


class Word():
    """
    Класс загаданного слова
    """

    word = ""
    description = ""
    wordMask = []

    @classmethod
    def form_mask(cls):
        cls.wordMask.clear()
        for i in range(len(cls.word)):
            cls.wordMask.append(False)

    @classmethod
    def show_word(cls):
        doneWord = ""

        for i in range(len(cls.word)):
            if cls.wordMask[i]:
                doneWord += cls.word[i]
            else:
                doneWord += '*'

        return doneWord


class GameManager:

    words = []
    alpVerify = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й',
                'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
                'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    alphabet = alpVerify.copy()

    letter_freqVerify = {'а': 8.01, 'б': 1.59, 'в': 4.54, 'г': 1.7, 'д': 2.98,
                         'е': 8.45, 'ж': 0.94, 'з': 1.65, 'и': 7.35, 'й': 1.21,
                         'к': 3.49, 'л': 4.4, 'м': 3.21, 'н': 6.7, 'о': 10.97,
                         'п': 2.81, 'р': 4.73, 'с': 5.47, 'т': 6.26, 'у': 2.62,
                         'ф': 0.26, 'х': 0.97, 'ц': 0.48, 'ч': 1.44, 'ш': 0.73,
                         'щ': 0.36, 'ъ': 0.04, 'ы': 1.9, 'ь': 1.74, 'э': 0.32,
                         'ю': 0.64, 'я': 2.01, 'ё': 0.04}
    letter_freq = letter_freqVerify.copy()

    scoreList = [10, 50, 100, 300, 500, 1000, 2000]
    selectedScore = 0
    score = 0
    scoreAI = 0

    endOfGame = False

    @classmethod
    def read_words(cls):
        """
        Считать слова из файла words.csv. Если файл не найден, создается новый пустой файл.
        """
        try:
            with open('words.csv', encoding='utf-8') as csvfile:
                readCSV= csv.reader(csvfile, delimiter = '|')

                for i, row in enumerate(readCSV):
                    if len(row) != 2:
                        errMsg = "Неверный формат строки! Индекс {0}. Строка пропущена."
                        print(errMsg.format(i))
                        continue

                    cls.words.append(row)
        except FileNotFoundError:
            print("Файл не найден! Создан новый") # MessageBox
            f =  open('words.csv', 'w')
            f.close()

    @classmethod
    def select_word(cls):
        try:
            choice = random.choice(cls.words)
            Word.word = choice[0]
            Word.description = choice[1]
        except IndexError:
            tkMessageBox.showerror("Ошибка", "Пустой набор слов в файле!")

    @classmethod
    def select_score(cls):
        cls.selectedScore = random.choice(cls.scoreList)
        return str(cls.selectedScore)

    @classmethod
    def get_alphabet(cls):
        alphabetString = ' '.join(cls.alphabet)
        return alphabetString

    @classmethod
    def check_input(cls, letter):
        for i, char in enumerate(Word.word):
            if letter == char:
                Word.wordMask[i] = True
                cls.score += cls.selectedScore
        try:
            GameManager.alphabet.remove(letter)
            GameManager.letter_freq.pop(letter)
            return True
        except:
            tkMessageBox.showinfo("Информация", "Буква уже была названа!")
            return False

    @classmethod
    def get_playerScore(cls):
        return str(cls.score)

    # Методы ИИ

    @classmethod
    def get_aiScore(cls):
        return str(cls.scoreAI)

    @classmethod
    def ai_letterSelect(cls):
        minFreq = min(cls.letter_freq.values())
        maxFreq = max(cls.letter_freq.values())

        choice = 0
        selFreq = 0
        letter = ''

        mode = random.random()
        bound1 = 0.2
        bound2 = 0.7

        if 0 <= mode < bound1:
            choice = minFreq
            selFreq = minFreq
        elif bound1 <= mode < bound2:
            choice = random.triangular(minFreq, maxFreq)
            selFreq = minFreq
        elif bound2 <= mode <= 1:
            choice = maxFreq
            selFreq = maxFreq

        for let in cls.alphabet:
            if (cls.letter_freq[let] >= selFreq) and (cls.letter_freq[let] <= choice):
                letter = let
                selFreq = cls.letter_freq[let]

        cls.letter_freq.pop(letter)

        return letter

    @classmethod
    def ai_checkLetter(cls, letter):
        for i, char in enumerate(Word.word):
            if letter == char:
                Word.wordMask[i] = True
                cls.scoreAI += cls.selectedScore
        try:
            GameManager.alphabet.remove(letter)
        except:
            tkMessageBox.showinfo("Информация", "ИИ сошел с ума и называет букву {0} снова".format(letter))

    # Методы игры

    @classmethod
    def check_isEnd(cls):
        if not False in Word.wordMask:
            cls.endOfGame = True

    @classmethod
    def start_new(cls):
        cls.alphabet = cls.alpVerify.copy()
        cls.letter_freq = cls.letter_freqVerify.copy()
        cls.select_word()
        Word.form_mask()
        cls.score = 0
        cls.scoreAI = 0
        cls.endOfGame = False

    @classmethod
    def choose_winner(cls):
        if cls.score > cls.scoreAI:
            return "Победа", "Вы выиграли со счётом {0} против {1}!".format(cls.score, cls.scoreAI)
        elif cls.score < cls.scoreAI:
            return "Поражение", "Вы проиграли со счётом {0} против {1}!".format(cls.score, cls.scoreAI)
        elif cls.score == cls.scoreAI:
            return "Ничья", "Да ладно! Рандом сравнял вас!"


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('500x650')
    root.resizable(width=False, height=False)

    GameManager.read_words()
    GameManager.select_word()
    Word.form_mask()

    app = Window(root)

    root.mainloop()
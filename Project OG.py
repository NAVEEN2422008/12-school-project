#OG:Offline Game Gallary

#1.HANGMAN GAME
#Let a be Self
#m be master
#att_lab be att_lab
#attempts be att
'''import tkinter as tk
import random

class Hangman:
    def __init__(a, m):
        a.m = m
        a.m.title("Hangman Game")
        a.m.configure(bg='lightblue')

        a.word_list = ['python', 'hangman', 'programming', 'tkinter', 'development','pen','pencil','sharpner','books','kingdom','fork','random','glitch','jackiechan','shinchan','naruto','kakashi','doraemon','powerrangers','pad','belt','keyboard','mouse','blastmohan',
             'leodas','jailer','lion','tiger','simba','mufasa','thegoat','read','heat','box','money','life','love','dove','bool','gandhi','nethaji','nehru','mama','anna','nee','naan','dhoni','viratkohli','sachin','neethan','naathan'
             'toy','loosu','keyboard','mersal','m','thambi','boss',]
        a.word = random.choice(a.word_list)
        a.guesses = []
        a.att = 6

        a.create_widgets()

    def create_widgets(a):
        a.label = tk.Label(a.m, text="Guess the word:", bg='lightblue', font=('Helvetica', 16))
        a.label.pack(pady=20)

        a.word_display = tk.Label(a.m, text=a.get_display_word(), bg='lightblue', font=('Helvetica', 24))
        a.word_display.pack(pady=20)

        a.entry = tk.Entry(a.m, font=('Helvetica', 16))
        a.entry.pack(pady=20)

        a.guess_button = tk.Button(a.m, text="Guess", command=a.make_guess, bg='green', fg='white')
        a.guess_button.pack(pady=10)

        a.hint_button = tk.Button(a.m, text="Hint", command=a.give_hint, bg='orange', fg='white')
        a.hint_button.pack(pady=10)

        a.att_lab = tk.Label(a.m, text=f"Attempts left: {a.att}", bg='lightblue', font=('Helvetica', 16))
        a.att_lab.pack(pady=20)

        a.guessed_label = tk.Label(a.m, text="Already guessed: ", bg='lightblue', font=('Helvetica', 16))
        a.guessed_label.pack(pady=20)

        a.hangman_canvas = tk.Canvas(a.m, width=200, height=200, bg='lightblue')
        a.hangman_canvas.pack(pady=20)

        a.draw_hangman()

    def get_display_word(a):
        return ' '.join([letter if letter in a.guesses else '_' for letter in a.word])

    def make_guess(a):
        guess = a.entry.get().lower()
        a.entry.delete(0, tk.END)

        if guess and guess not in a.guesses:
            a.guesses.append(guess)
            if guess not in a.word:
                a.att -= 1
            a.update_game()

    def update_game(a):
        a.word_display.config(text=a.get_display_word())
        a.att_lab.config(text=f"att left: {a.att}")
        a.guessed_label.config(text="Already guessed: " + ', '.join(a.guesses))
        a.draw_hangman()

        if a.att <= 0:
            a.label.config(text="Game Over! The word was: " + a.word)
            a.guess_button.config(state='disabled')
            a.hint_button.config(state='disabled')

        if '_' not in a.get_display_word():
            a.label.config(text="Congratulations! You've guessed the word!")

    def give_hint(a):
        hint_letter = random.choice([letter for letter in a.word if letter not in a.guesses])
        a.guesses.append(hint_letter)
        a.update_game()

    def draw_hangman(a):
        a.hangman_canvas.delete("all")
        if a.att < 6:
            a.hangman_canvas.create_line(50, 150, 150, 150)  # base
        if a.att < 5:
            a.hangman_canvas.create_line(100, 150, 100, 50)  # pole
        if a.att < 4:
            a.hangman_canvas.create_line(100, 50, 150, 50)  # top
        if a.att < 3:
            a.hangman_canvas.create_line(150, 50, 150, 75)  # rope
        if a.att < 2:
            a.hangman_canvas.create_oval(130, 75, 170, 115)  # head
        if a.att < 1:
            a.hangman_canvas.create_line(150, 115, 130, 140)  # left arm
            a.hangman_canvas.create_line(150, 115, 170, 140)  # right arm
            a.hangman_canvas.create_line(150, 115, 150, 160)  # body
            a.hangman_canvas.create_line(150, 160, 130, 180)  # left leg
            a.hangman_canvas.create_line(150, 160, 170, 180)  # right leg

if __name__ == "__main__":
    root = tk.Tk()
    game = Hangman(root)
    root.mainloop()'''
#2
'''# Tic Tac Toe Game using Tkinter
import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, master):
        self.master = master
        master.title("Tic Tac Toe")
        master.configure(bg="#f0f8ff")  # Light blue background

        self.current_player = "X"
        self.board = [" " for _ in range(9)]
        self.buttons = []

        # Define colors for players
        self.colors = {
            "X": "#ff6347",  # Tomato color for X
            "O": "#4682b4",  # Steel blue for O
            "default": "#e0ffff"  # Light cyan for empty buttons
        }

        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(master, text=" ", font=('Arial', 40), width=5, height=2,
                                   command=lambda idx=i*3+j: self.make_move(idx), bg=self.colors['default'])
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_game, bg="#ffcccb", font=('Arial', 16))
        self.reset_button.grid(row=3, column=0, columnspan=3)

    def make_move(self, idx):
        if self.board[idx] == " ":
            self.board[idx] = self.current_player
            self.buttons[idx // 3][idx % 3].config(text=self.current_player, bg=self.colors[self.current_player])
            
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            elif " " not in self.board:
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)               # Diagonals
        ]
        for a, b, c in winning_combinations:
            if self.board[a] == self.board[b] == self.board[c] != " ":
                return True
        return False

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        for row in self.buttons:
            for button in row:
                button.config(text=" ", bg=self.colors['default'])

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()'''
#

# Drawing Game with Tkinter

#
'''import tkinter as tk
from tkinter import messagebox, colorchooser
import random

class DrawingGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Drawing Game")
        
        self.canvas1 = tk.Canvas(master, width=300, height=300, bg='white')
        self.canvas1.grid(row=0, column=0)
        self.canvas1.bind("<B1-Motion>", self.draw1)

        self.canvas2 = tk.Canvas(master, width=300, height=300, bg='white')
        self.canvas2.grid(row=0, column=1)
        self.canvas2.bind("<B1-Motion>", self.draw2)

        self.current_player = 1
        self.prompt_label = tk.Label(master, text="", font=("Arial", 14))
        self.prompt_label.grid(row=1, columnspan=2)

        self.color_button = tk.Button(master, text="Choose Color", command=self.choose_color)
        self.color_button.grid(row=2, column=0)

        self.thickness_label = tk.Label(master, text="Line Thickness:")
        self.thickness_label.grid(row=2, column=1)
        
        self.thickness_scale = tk.Scale(master, from_=1, to=10, orient='horizontal')
        self.thickness_scale.set(2)
        self.thickness_scale.grid(row=3, column=1)

        self.submit_button = tk.Button(master, text="Submit Drawing", command=self.submit_drawing)
        self.submit_button.grid(row=4, columnspan=2)

        self.prompt_list = ["Circle", "Square", "Triangle"]
        self.next_turn()

        self.pen_color = "black"

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.pen_color = color

    def next_turn(self):
        self.prompt = random.choice(self.prompt_list)
        self.prompt_label.config(text=f"Draw: {self.prompt}")
        self.canvas1.delete("all")
        self.canvas2.delete("all")
        self.current_player = 1

    def draw1(self, event):
        x, y = event.x, event.y
        self.canvas1.create_oval(x - self.thickness_scale.get(), y - self.thickness_scale.get(),
                                  x + self.thickness_scale.get(), y + self.thickness_scale.get(),
                                  fill=self.pen_color, outline=self.pen_color)

    def draw2(self, event):
        x, y = event.x, event.y
        self.canvas2.create_oval(x - self.thickness_scale.get(), y - self.thickness_scale.get(),
                                  x + self.thickness_scale.get(), y + self.thickness_scale.get(),
                                  fill=self.pen_color, outline=self.pen_color)

    def submit_drawing(self):
        if self.current_player == 1:
            self.current_player = 2
            self.prompt_label.config(text="Player 2's Turn!")
        elif self.current_player == 2:
            self.judge_drawings()
            self.next_turn()

    def judge_drawings(self):
        player1_score = random.randint(50, 100)  # Random score for Player 1
        player2_score = random.randint(50, 100)  # Random score for Player 2

        messagebox.showinfo("Results", f"Player 1 Score: {player1_score}%\nPlayer 2 Score: {player2_score}%\n"
                                         f"{'Player 1 wins!' if player1_score > player2_score else 'Player 2 wins!' if player2_score > player1_score else 'It\'s a tie!'}")

if __name__ == "__main__":
    root = tk.Tk()
    game = DrawingGame(root)
    root.mainloop()'''
class Game:
    def __init__(self):
        self.games = {
            "1": self.play_game_1,
            "2": self.play_game_2,
            "3": self.play_game_3,
            "4": self.play_game_4
        }

    def main_menu(self):
        while True:
            print("\nWelcome to the Game Menu!")
            print("1. Play Game 1")
            print("2. Play Game 2")
            print("3. Play Game 3")
            print("4. Play Game 4")
            print("5. Exit")

            choice = input("Please select an option (1-5): ")

            if choice in self.games:
                self.games[choice]()
            elif choice == '5':
                print("Thank you for playing!")
                break
            else:
                print("Invalid choice. Please try again.")

    def  __init__(self):
        print("Starting Game 1...")

    def play_game_2(self):
        print("Starting Game 2...")

    def play_game_3(self):
        print("Starting Game 3...")

    def play_game_4(self):
        print("Starting Game 4...")

if __name__ == "__main__":
    game = Game()
    game.main_menu()

#


#Movie
import tkinter as tk
from tkinter import messagebox, colorchooser
import random

class MovieGuessingGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Movie Guessing Game")
        self.master.geometry("400x400")
        self.master.configure(bg="#f0f0f0")

        self.movies = {
            "Avengers Endgame": ["One vs infinity superhero", "Infinity stones", "Fifty percentage of world disappear"],
            "Fast and Furious": ["Car based movie", "High-octane car chasing", "Thrilling chase"],
            "Titanic": ["A tragic love story", "Set on a ship", "Ship pose"],
            "Avatar": ["Set on an alien planet", "Features blue-skinned beings", "Different planet and Different character"],
            "Harry potter": ["About a Wizard world", "9-3/4 gateway", "The Hogwarts university'"]
        }

        self.score = 0
        self.attempts = 3
        self.current_movie = ""
        self.clue_index = 0

        self.title_label = tk.Label(master, text="Guess the Movie!", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        self.title_label.pack(pady=10)

        self.clue_label = tk.Label(master, text="", font=("Arial", 14), bg="#f0f0f0", fg="#555")
        self.clue_label.pack(pady=10)

        self.guess_entry = tk.Entry(master, font=("Arial", 14))
        self.guess_entry.pack(pady=10)

        self.submit_button = tk.Button(master, text="Submit Guess", command=self.check_guess, bg="#4CAF50", fg="white", font=("Arial", 14, "bold"))
        self.submit_button.pack(pady=5)

        self.next_button = tk.Button(master, text="Next Clue", command=self.next_clue, bg="#2196F3", fg="white", font=("Arial", 14, "bold"))
        self.next_button.pack(pady=5)

        self.score_label = tk.Label(master, text="Score: 0", font=("Arial", 14), bg="#f0f0f0", fg="#333")
        self.score_label.pack(pady=10)

        self.start_new_game()

    def start_new_game(self):
        self.current_movie, self.clues = random.choice(list(self.movies.items()))
        self.clue_index = 0
        self.attempts = 3
        self.score_label.config(text=f"Score: {self.score}")
        self.clue_label.config(text="Clue: " + self.clues[self.clue_index])
        self.guess_entry.delete(0, tk.END)

    def check_guess(self):
        guess = self.guess_entry.get().strip()
        if guess.lower() == self.current_movie.lower():
            self.score += 1
            messagebox.showinfo("Correct!", f"Correct! The movie was '{self.current_movie}'.")
            self.start_new_game()
        else:
            self.attempts -= 1
            if self.attempts <= 0:
                messagebox.showinfo("Game Over", f"You've run out of attempts. The movie was '{self.current_movie}'.")
                self.start_new_game()
            else:
                messagebox.showinfo("Wrong!", f"Wrong guess! Attempts left: {self.attempts}")

    def next_clue(self):
        self.clue_index += 1
        if self.clue_index < len(self.clues):
            self.clue_label.config(text="Clue: " + self.clues[self.clue_index])
        else:
            messagebox.showinfo("No More Clues", "You've reached the end of the clues!")
            self.attempts = 0  # Force game over since no clues are left

if __name__ == "__main__":
    root = tk.Tk()
    game = MovieGuessingGame(root)
    root.mainloop()
#

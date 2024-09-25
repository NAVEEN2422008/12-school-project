import tkinter as tk
from tkinter import messagebox, colorchooser, PhotoImage
import random

# Hangman Game
def start_hangman():
    hangman_window = tk.Toplevel()
    hangman_window.title("Hangman Game")
    hangman_window.configure(bg='lightblue')

    word_list = ['python', 'hangman', 'programming', 'tkinter', 'development']
    word = random.choice(word_list)
    guesses = []
    att = 6

    def get_display_word():
        return ' '.join([letter if letter in guesses else '_' for letter in word])

    def draw_hangman():
        hangman_canvas.delete("all")
        if att < 6:
            hangman_canvas.create_line(50, 150, 150, 150)  # base
        if att < 5:
            hangman_canvas.create_line(100, 150, 100, 50)  # pole
        if att < 4:
            hangman_canvas.create_line(100, 50, 150, 50)  # top
        if att < 3:
            hangman_canvas.create_line(150, 50, 150, 75)  # rope
        if att < 2:
            hangman_canvas.create_oval(130, 75, 170, 115)  # head
        if att < 1:
            hangman_canvas.create_line(150, 115, 130, 140)  # left arm
            hangman_canvas.create_line(150, 115, 170, 140)  # right arm
            hangman_canvas.create_line(150, 115, 150, 160)  # body
            hangman_canvas.create_line(150, 160, 130, 180)  # left leg
            hangman_canvas.create_line(150, 160, 170, 180)  # right leg

    def make_guess():
        nonlocal att
        guess = entry.get().lower()
        entry.delete(0, tk.END)

        if guess and guess not in guesses:
            guesses.append(guess)
            if guess not in word:
                att -= 1
            update_game()

    def update_game():
        word_display.config(text=get_display_word())
        att_lab.config(text=f"Attempts left: {att}")
        guessed_label.config(text="Already guessed: " + ', '.join(guesses))
        draw_hangman()

        if att <= 0:
            label.config(text="Game Over! The word was: " + word)
            guess_button.config(state='disabled')
            hint_button.config(state='disabled')

        if '_' not in get_display_word():
            label.config(text="Congratulations! You've guessed the word!")

    def give_hint():
        hint_letter = random.choice([letter for letter in word if letter not in guesses])
        guesses.append(hint_letter)
        update_game()

    label = tk.Label(hangman_window, text="Guess the word:", bg='lightblue', font=('Helvetica', 16))
    label.pack(pady=20)

    word_display = tk.Label(hangman_window, text=get_display_word(), bg='lightblue', font=('Helvetica', 24))
    word_display.pack(pady=20)

    entry = tk.Entry(hangman_window, font=('Helvetica', 16))
    entry.pack(pady=20)

    guess_button = tk.Button(hangman_window, text="Guess", command=make_guess, bg='lightgreen', fg='white')
    guess_button.pack(pady=10)

    hint_button = tk.Button(hangman_window, text="Hint", command=give_hint, bg='orange', fg='white')
    hint_button.pack(pady=10)

    att_lab = tk.Label(hangman_window, text=f"Attempts left: {att}", bg='lightblue', font=('Helvetica', 16))
    att_lab.pack(pady=20)

    guessed_label = tk.Label(hangman_window, text="Already guessed: ", bg='lightblue', font=('Helvetica', 16))
    guessed_label.pack(pady=20)

    hangman_canvas = tk.Canvas(hangman_window, width=200, height=200, bg='lightblue')
    hangman_canvas.pack(pady=20)

    draw_hangman()

# Tic Tac Toe Game
def start_tictactoe():
    tictactoe_window = tk.Toplevel()
    tictactoe_window.title("Tic Tac Toe")
    tictactoe_window.configure(bg="#e0f7fa")

    current_player = "X"
    board = [" " for _ in range(9)]
    buttons = []

    colors = {
        "X": "#ff4081",
        "O": "#2196f3",
        "default": "#b2ebf2"
    }

    def reset_game():
        nonlocal current_player
        board[:] = [" " for _ in range(9)]
        current_player = "X"
        for row in buttons:
            for button in row:
                button.config(text=" ", bg=colors['default'])

    for i in range(3):
        row = []
        for j in range(3):
            button = tk.Button(tictactoe_window, text=" ", font=('Arial', 40), width=5, height=2,
                               command=lambda idx=i*3+j: make_move(idx), bg=colors['default'])
            button.grid(row=i, column=j)
            row.append(button)
        buttons.append(row)

    reset_button = tk.Button(tictactoe_window, text="Reset", command=reset_game, bg="#ffcccb", font=('Arial', 16))
    reset_button.grid(row=3, columnspan=3)
    def make_move(idx):
        nonlocal current_player
        if board[idx] == " ":
            board[idx] = current_player
            buttons[idx // 3][idx % 3].config(text=current_player, bg=colors[current_player])

            if check_winner():
                messagebox.showinfo("Game Over", f"Player {current_player} wins!")
                reset_game()
            elif " " not in board:
                messagebox.showinfo("Game Over", "It's a draw!")
                reset_game()
            else:
                current_player = "O" if current_player == "X" else "X"

    def check_winner():
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in winning_combinations:
            if board[a] == board[b] == board[c] != " ":
                return True
        return False

# Drawing Game
def start_drawing():
   import tkinter as tk
from tkinter import colorchooser, messagebox
import random

# Start the drawing game
def start_drawing():
    drawing_window = tk.Toplevel()
    drawing_window.title("Beautiful Drawing Game")
    drawing_window.configure(bg='#f0f4f8')  # Soft pastel background

    # Choose a random topic for both players
    topics = ["House", "Tree", "Car", "Flower", "Mountain"]
    chosen_topic = random.choice(topics)

    # Create canvases for both players with stylish borders
    canvas1 = tk.Canvas(drawing_window, width=300, height=300, bg='white', highlightthickness=2, highlightbackground='lightblue')
    canvas1.grid(row=1, column=0, padx=20, pady=10)
    canvas1.bind("<B1-Motion>", lambda event: draw(event, canvas1))

    canvas2 = tk.Canvas(drawing_window, width=300, height=300, bg='white', highlightthickness=2, highlightbackground='lightblue')
    canvas2.grid(row=1, column=1, padx=20, pady=10)
    canvas2.bind("<B1-Motion>", lambda event: draw(event, canvas2))
    canvas2.config(state=tk.DISABLED)  # Initially disable the second canvas

    current_player = 1  # Track the current player
    color = '#000000'   # Default drawing color
    thickness = 2       # Default brush thickness

    # Label to show drawing prompt with updated fonts and colors
    prompt_label = tk.Label(drawing_window, text=f"Player 1, draw a {chosen_topic}", font=("Arial", 16, 'bold'), bg='#f0f4f8', fg='#1565c0')
    prompt_label.grid(row=0, columnspan=2, pady=10)

    # Choose a drawing color
    def choose_color():
        nonlocal color
        color = colorchooser.askcolor()[1]

    # Set the eraser functionality
    def choose_eraser():
        nonlocal color
        color = '#ffffff'

    # Buttons for choosing color and eraser with soft color themes
    color_button = tk.Button(drawing_window, text="Choose Color", command=choose_color, bg='#64b5f6', fg='white', font=('Arial', 12), relief='flat')
    color_button.grid(row=2, column=0, pady=10)

    eraser_button = tk.Button(drawing_window, text="Eraser", command=choose_eraser, bg='#ffcccb', fg='white', font=('Arial', 12), relief='flat')
    eraser_button.grid(row=2, column=1, pady=10)

    # Function to handle drawing on the canvas
    def draw(event, canvas):
        x, y = event.x, event.y
        r = thickness
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=color)

    # Submit the drawings and switch between players
    def submit_drawings():
        nonlocal current_player
        if current_player == 1:
            canvas2.config(state=tk.NORMAL)  # Enable canvas for Player 2
            canvas1.config(state=tk.DISABLED)  # Disable canvas for Player 1
            prompt_label.config(text=f"Player 2, draw the same!")  # Update prompt for Player 2
            current_player = 2
        else:
            prompt_label.config(text="Drawings submitted! Let's see the results...")
            canvas2.config(state=tk.DISABLED)
            compare_drawings()

    # Compare drawings based on the number of filled pixels
    def compare_drawings():
        score1 = score_drawing(canvas1)
        score2 = score_drawing(canvas2)

        # Announce the winner and show percentages
        if score1 > score2:
            winner = "Player 1 Wins!"
        elif score2 > score1:
            winner = "Player 2 Wins!"
        else:
            winner = "It's a Draw!"

        messagebox.showinfo("Results", f"Player 1: {score1}%\nPlayer 2: {score2}%\n{winner}")

    # Calculate the percentage of filled pixels for scoring
    def score_drawing(canvas):
        pixel_count = 0
        for i in range(300):
            for j in range(300):
                item = canvas.find_closest(i, j)
                if item:
                    coords = canvas.coords(item)
                    if coords and (coords[0] - 2 <= i <= coords[2] + 2) and (coords[1] - 2 <= j <= coords[3] + 2):
                        pixel_count += 1
        return int((pixel_count / (300 * 300)) * 100)  # Return percentage of filled pixels

    # Submit button with updated aesthetics
    submit_button = tk.Button(drawing_window, text="Submit Drawing", command=submit_drawings, bg='#a5d6a7', fg='white', font=('Arial', 12), relief='flat')
    submit_button.grid(row=4, columnspan=2, pady=20)

# Maze Game
def start_maze():
    maze_window = tk.Toplevel()
    maze_window.title("Maze Game")
    
    width, height = 20, 20
    cell_size = 30
    canvas = tk.Canvas(maze_window, width=width * cell_size, height=height * cell_size, bg='#f0f0f0')
    canvas.pack()

    def generate_maze(width, height):
        maze = [[1 for _ in range(width)] for _ in range(height)]

        def carve_path(x, y):
            maze[y][x] = 0
            directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                    maze[y + dy // 2][x + dx // 2] = 0
                    carve_path(nx, ny)

        carve_path(1, 1)
        return maze

    maze = generate_maze(width, height)
    player_x, player_y = 1, 1

    def draw_maze():
        canvas.delete("all")
        for i in range(height):
            for j in range(width):
                color = '#cce5ff' if maze[i][j] == 0 else '#003366'
                canvas.create_rectangle(j * cell_size, i * cell_size,
                                        (j + 1) * cell_size, (i + 1) * cell_size,
                                        fill=color, outline='#333333')

        canvas.create_rectangle(player_x * cell_size, player_y * cell_size,
                                (player_x + 1) * cell_size, (player_y + 1) * cell_size,
                                fill='#ff5733')

        canvas.create_rectangle((width - 2) * cell_size, (height - 2) * cell_size,
                                (width - 1) * cell_size, (height - 1) * cell_size,
                                fill='#28a745')

    def move(event):
        nonlocal player_x, player_y
        if event.keysym == 'Up' and player_y > 0 and maze[player_y - 1][player_x] == 0:
            player_y -= 1
        elif event.keysym == 'Down' and player_y < height - 1 and maze[player_y + 1][player_x] == 0:
            player_y += 1
        elif event.keysym == 'Left' and player_x > 0 and maze[player_y][player_x - 1] == 0:
            player_x -= 1
        elif event.keysym == 'Right' and player_x < width - 1 and maze[player_y][player_x + 1] == 0:
            player_x += 1
        draw_maze()

        if player_x == width - 2 and player_y == height - 2:
            canvas.create_text(width * cell_size / 2, height * cell_size / 2,
                               text="You Win!", fill="#ff5733", font=('Helvetica', 24, 'bold'))

    def reset_maze():
        nonlocal maze, player_x, player_y
        maze = generate_maze(width, height)
        player_x, player_y = 1, 1
        draw_maze()

    maze_window.bind("<KeyPress>", move)

    draw_maze()

    tk.Button(maze_window, text="Reset", command=reset_maze).pack(pady=10)

# Main menu with image icons
import tkinter as tk
from tkinter import PhotoImage

def main_menu():
    main_window = tk.Tk()
    main_window.title("Mini Games Hub")
    main_window.geometry("800x200")  # Adjust the window size as needed

    title_label = tk.Label(main_window, text="Welcome to Mini Games Hub!", font=("Arial", 16))
    title_label.pack(pady=20)

    # Load images for the buttons and resize them
    button_size = (100, 100)  # Set desired size for buttons
    hangman_img = PhotoImage(file="D:/kk/hangman_icon.png").subsample(9, 9)  # Adjust for your image
    tictactoe_img = PhotoImage(file="D:/kk/tictactoe_icon.png").subsample(3,3)
    drawing_img = PhotoImage(file="D:/kk/drawing_icon.png").subsample(6, 6)
    maze_img = PhotoImage(file="D:/kk/maze_icon.png").subsample(2, 2)

    # Create a frame for landscape layout
    button_frame = tk.Frame(main_window)
    button_frame.pack(pady=10)

    # Create buttons with images and fixed size
    hangman_button = tk.Button(button_frame, image=hangman_img, command=start_hangman, width=button_size[0], height=button_size[1])
    hangman_button.image = hangman_img  # Keep a reference to the image
    hangman_button.pack(side=tk.LEFT, padx=5)

    tictactoe_button = tk.Button(button_frame, image=tictactoe_img, command=start_tictactoe, width=button_size[0], height=button_size[1])
    tictactoe_button.image = tictactoe_img  # Keep a reference to the image
    tictactoe_button.pack(side=tk.LEFT, padx=5)

    drawing_button = tk.Button(button_frame, image=drawing_img, command=start_drawing, width=button_size[0], height=button_size[1])
    drawing_button.image = drawing_img  # Keep a reference to the image
    drawing_button.pack(side=tk.LEFT, padx=5)

    maze_button = tk.Button(button_frame, image=maze_img, command=start_maze, width=button_size[0], height=button_size[1])
    maze_button.image = maze_img  # Keep a reference to the image
    maze_button.pack(side=tk.LEFT, padx=5)

    main_window.mainloop()

if __name__ == "__main__":
    main_menu()

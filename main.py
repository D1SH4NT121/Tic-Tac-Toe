import tkinter as tk
from tkinter import messagebox
import random

def check_winner():
    global winner
    for combo in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != "":
            winner = True
            animate_winner(combo)
            return True
    return False

def check_draw():
    if all(button["text"] != "" for button in buttons) and not winner:
        messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
        root.after(500, reset_game)
        return True
    return False

def animate_winner(combo):
    colors = ["#FFA", "#FF8", "#FF6", "#FF4", "#FF2", "#FF0", "green"]

    def highlight(index=0):
        if index < len(colors):
            for i in combo:
                buttons[i].config(bg=colors[index])
            root.after(100, lambda: highlight(index + 1))
        else:
            messagebox.showinfo("Tic-Tac-Toe", f"Player {buttons[combo[0]]['text']} wins!")
            root.after(500, reset_game)

    highlight()

def button_click(index):
    if buttons[index]["text"] == "" and not winner:
        buttons[index]["text"] = current_player
        touch_animation(index)
        if not check_winner():
            if not check_draw():  # Check for draw after checking winner
                toggle_player()
                if mode_var.get() == "Player vs Computer" and current_player == "O" and not winner:
                    root.after(500, computer_move)

def touch_animation(index):
    original_color = buttons[index].cget("bg")
    buttons[index].config(bg="lightblue")
    root.after(200, lambda: buttons[index].config(bg=original_color))

def toggle_player():
    global current_player
    current_player = "X" if current_player == "O" else "O"
    label.config(text=f"Player {current_player}'s turn")

def reset_game():
    global winner, current_player
    winner = False
    current_player = "X"
    label.config(text=f"Player {current_player}'s turn")
    for button in buttons:
        button.config(text="", bg="#D3D3D3")

def computer_move():
    empty_buttons = [i for i, button in enumerate(buttons) if button["text"] == ""]
    if empty_buttons and not winner:
        index = random.choice(empty_buttons)
        buttons[index].config(text="O")
        touch_animation(index)
        if not check_winner():
            check_draw()
            if not winner:
                toggle_player()

def welcome_animation():
    welcome_text = "Welcome to Tic-Tac-Toe!"
    label.config(text="")
    def update_label(index=0):
        if index < len(welcome_text):
            label.config(text=label.cget("text") + welcome_text[index])
            root.after(100, lambda: update_label(index + 1))
        else:
            root.after(1000, start_game)
    update_label()

def start_game():
    for i, button in enumerate(buttons):
        button.config(state=tk.NORMAL)
    label.config(text=f"Player {current_player}'s turn")

root = tk.Tk()
root.title("Tic-Tac-Toe")

buttons = [tk.Button(root, text="", font=("Helvetica", 25), width=6, height=2, relief="raised", bd=5, bg="#D3D3D3", state=tk.DISABLED, command=lambda i=i: button_click(i)) for i in range(9)]
for i, button in enumerate(buttons):
    button.grid(row=i//3, column=i%3)

current_player = "X"
winner = False
label = tk.Label(root, text="", font=("Helvetica", 16))
label.grid(row=3, column=0, columnspan=3)

mode_var = tk.StringVar(value="Player vs Player")
mode_menu = tk.OptionMenu(root, mode_var, "Player vs Player", "Player vs Computer")
mode_menu.grid(row=4, column=0, columnspan=3)

root.after(500, welcome_animation)

root.mainloop()

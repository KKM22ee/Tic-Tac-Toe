import tkinter as tk
from functools import partial
import numpy as np

def check_winner(board):
    for row in board:
        if all(cell == row[0] and cell != "" for cell in row):
            return row[0]
    for col in range(3):
        if all(board[row][col] == board[0][col] and board[row][col] != "" for row in range(3)):
            return board[0][col]
    if all(board[i][i] == board[0][0] and board[i][i] != "" for i in range(3)):
        return board[0][0]
    if all(board[i][2 - i] == board[0][2] and board[i][2 - i] != "" for i in range(3)):
        return board[0][2]
    if all(board[row][col] != "" for row in range(3) for col in range(3)):
        return "Tie"
    return None

def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == "X":
        return -1
    elif winner == "O":
        return 1
    elif winner == "Tie":
        return 0
    
    best_score = -np.inf if is_maximizing else np.inf
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                board[row][col] = "O" if is_maximizing else "X"
                score = minimax(board, not is_maximizing)
                board[row][col] = ""
                best_score = max(score, best_score) if is_maximizing else min(score, best_score)
    return best_score

def best_move(board):
    best_score = -np.inf
    move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                board[row][col] = "O"
                score = minimax(board, False)
                board[row][col] = ""
                if score > best_score:
                    best_score = score
                    move = (row, col)
    return move

def click(row, col):
    if board[row][col] == "" and check_winner(board) is None:
        board[row][col] = "X"
        buttons[row][col].config(text="X")
        
        if check_winner(board) is None:
            ai_move = best_move(board)
            if ai_move:
                board[ai_move[0]][ai_move[1]] = "O"
                buttons[ai_move[0]][ai_move[1]].config(text="O")
                
        winner = check_winner(board)
        if winner:
            label.config(text=f"Winner: {winner}")

root = tk.Tk()
root.title("Tic-Tac-Toe AI")
board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]

for row in range(3):
    for col in range(3):
        buttons[row][col] = tk.Button(root, text="", font=("Arial", 24), height=2, width=5, command=partial(click, row, col))
        buttons[row][col].grid(row=row, column=col)

label = tk.Label(root, text="", font=("Arial", 14))
label.grid(row=3, column=0, columnspan=3)

root.mainloop()

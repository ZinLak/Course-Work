import tkinter as tk
from tkinter import messagebox
import math

class PetteiaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Игра Петтейя")

        self.board_size = 8
        self.cell_size = 60
        self.current_player = 2
        self.selected_piece = None
        
        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack()

        self.possible_moves = []

        tk.Label(self.menu_frame, text="Выберите режим игры:", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.menu_frame, text="Игра с другом", command=self.start_two_player_game, font=("Arial", 14)).pack(pady=5)
        tk.Button(self.menu_frame, text="Игра с компьютером", command=self.start_ai_game, font=("Arial", 14)).pack(pady=5)

        self.game_frame = tk.Frame(root)
        self.info_label = tk.Label(self.game_frame, font=("Arial", 14), anchor="w")

        window_width = self.board_size * self.cell_size
        window_height = self.board_size * self.cell_size + 50  # С учетом информации
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def start_two_player_game(self):
        self.is_ai_game = False
        self.start_game()

    def start_ai_game(self):
        self.is_ai_game = True
        self.current_player = 2
        self.start_game()

    def start_game(self):
        self.menu_frame.pack_forget()
        self.game_frame.pack()

        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.setup_board()

        self.canvas = tk.Canvas(self.game_frame, width=self.board_size * self.cell_size, height=self.board_size * self.cell_size)
        self.canvas.pack()
        self.info_label.pack(fill=tk.X)

        self.draw_board()
        self.update_turn_info()
        self.canvas.bind("<Button-1>", self.handle_click)

    def setup_board(self):
        for col in range(self.board_size):
            self.board[0][col] = 1  # Красные шашки
            self.board[self.board_size - 1][col] = 2  # Черные шашки

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                
                if self.board[row][col] == 1:
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="red")
                elif self.board[row][col] == 2:
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="black")
                
                if self.selected_piece == (row, col):
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", width=3)

                for r, c in self.possible_moves:
                    x1 = c * self.cell_size
                    y1 = r * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    self.canvas.create_oval(x1 + 15, y1 + 15, x2 - 15, y2 - 15, outline="blue", width=2)

    def handle_click(self, event):
        if self.is_ai_game and self.current_player == 1:
            return
        
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if self.select_piece(row, col):
                self.check_capture(row, col)
                self.switch_player()
                self.draw_board()
                self.update_turn_info()
                self.check_game_over()
                
                if self.is_ai_game and self.current_player == 1:
                    self.root.after(500, self.ai_move)
    
    def select_piece(self, row, col):
        if self.board[row][col] == self.current_player:
            self.selected_piece = (row, col)
            self.possible_moves = self.get_possible_moves(row, col)  # Вычисляем возможные ходы
            self.draw_board()
            return False
        elif self.selected_piece:
            start_row, start_col = self.selected_piece
            if (row, col) in self.possible_moves:  # Проверяем, входит ли ход в список возможных
                self.board[row][col] = self.board[start_row][start_col]
                self.board[start_row][start_col] = 0
                self.selected_piece = None
                self.possible_moves = []  # Очищаем возможные ходы после хода
                return True
        return False

    def get_possible_moves(self, row, col):
        moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.board_size and 0 <= nc < self.board_size and self.board[nr][nc] == 0:
                moves.append((nr, nc))
        return moves
    
    def is_valid_move(self, start_row, start_col, end_row, end_col):
        if self.board[end_row][end_col] != 0:
            return False
        if abs(start_row - end_row) + abs(start_col - end_col) != 1:
            return False
        return True
    
    def check_capture(self, row, col):
        opponent = 2 if self.current_player == 1 else 1
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for dr, dc in directions:
            r1, c1 = row + dr, col + dc
            r2, c2 = row + 2 * dr, col + 2 * dc

            if (0 <= r1 < self.board_size and 0 <= c1 < self.board_size and
                0 <= r2 < self.board_size and 0 <= c2 < self.board_size):
                if (self.board[r1][c1] == opponent and
                    self.board[r2][c2] == self.current_player):
                    self.board[r1][c1] = 0

    def switch_player(self):
        self.current_player = 1 if self.current_player == 2 else 2
    
    def update_turn_info(self):
        turn = "Красных" if self.current_player == 1 else "Чёрных"
        self.info_label.config(text=f"Ход: {turn}")
    
    def check_game_over(self):
        player1_pieces = sum(row.count(1) for row in self.board)
        player2_pieces = sum(row.count(2) for row in self.board)
        
        if player1_pieces == 0 or (player1_pieces > 0 and not self.has_valid_moves(1)):
            messagebox.showinfo("Игра окончена", "Чёрные выиграли!")
            self.root.quit()
        elif player2_pieces == 0 or (player2_pieces > 0 and not self.has_valid_moves(2)):
            messagebox.showinfo("Игра окончена", "Красные выиграли!")
            self.root.quit()
    
    def has_valid_moves(self, player):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == player:
                    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if (0 <= nr < self.board_size and 0 <= nc < self.board_size and
                            self.board[nr][nc] == 0):
                            return True
        return False



root = tk.Tk()
game = PetteiaGame(root)
root.mainloop()
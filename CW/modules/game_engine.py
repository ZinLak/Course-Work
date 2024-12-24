class PetteiaEngine:
    def __init__(self, board_size=8):
        self.board_size = board_size
        self.board = [[0] * board_size for _ in range(board_size)]
        self.current_player = 2
        self.selected_piece = None
        self.possible_moves = []

        self.setup_board()

    def setup_board(self):
        """Сбрасывает игровую доску в начальное состояние."""
        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        for col in range(self.board_size):
            self.board[0][col] = 1
            self.board[self.board_size - 1][col] = 2
        self.current_player = 2
        self.selected_piece = None
        self.possible_moves = []


    def select_piece(self, row, col):
        """Обрабатывает выбор шашки игроком."""
        if self.board[row][col] == self.current_player:
            self.selected_piece = (row, col)
            self.possible_moves = self.get_possible_moves(row, col)
            return False
        elif self.selected_piece:
            start_row, start_col = self.selected_piece
            if (row, col) in self.possible_moves:
                self.board[row][col] = self.board[start_row][start_col]
                self.board[start_row][start_col] = 0
                self.selected_piece = None
                self.possible_moves = []
                return True
        return False

    def get_possible_moves(self, row, col):
        """Возвращает список возможных ходов для выбранной шашки."""
        moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.board_size and 0 <= nc < self.board_size and self.board[nr][nc] == 0:
                moves.append((nr, nc))
        return moves

    def check_capture(self, row, col):
        """Проверяет и удаляет шашки противника, если они захвачены."""
        opponent = 2 if self.current_player == 1 else 1
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            r1, c1 = row + dr, col + dc
            r2, c2 = row + 2 * dr, col + 2 * dc
            if (0 <= r1 < self.board_size and 0 <= c1 < self.board_size and
                0 <= r2 < self.board_size and 0 <= c2 < self.board_size):
                if self.board[r1][c1] == opponent and self.board[r2][c2] == self.current_player:
                    self.board[r1][c1] = 0

    def switch_player(self):
        """Меняет текущего игрока."""
        self.current_player = 1 if self.current_player == 2 else 2

    def is_game_over(self):
        """Проверяет, завершена ли игра."""
        player1_pieces = sum(row.count(1) for row in self.board)
        player2_pieces = sum(row.count(2) for row in self.board)
        return player1_pieces == 0 or player2_pieces == 0 or not self.has_valid_moves(1) or not self.has_valid_moves(2)

    def has_valid_moves(self, player):
        """Проверяет, есть ли у игрока валидные ходы."""
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == player:
                    if self.get_possible_moves(row, col):
                        return True
        return False

    def evaluate_turn(self):
        """Возвращает информацию о текущем ходе."""
        return "Красных" if self.current_player == 1 else "Чёрных"

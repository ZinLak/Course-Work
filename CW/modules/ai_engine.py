import copy

class PetteiaAI:
    def __init__(self, depth=3):
        self.depth = depth  # Глубина поиска Minimax

    def find_best_move(self, engine):
        """Ищет лучший ход для бота."""
        best_value = float('-inf')
        best_move = None

        for move in self.generate_moves(engine.board, 1):
            new_board = self.make_move(copy.deepcopy(engine.board), move)
            value = self.minimax(new_board, self.depth - 1, False, float('-inf'), float('inf'))
            if value > best_value:
                best_value = value
                best_move = move

        return best_move

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        """Алгоритм Minimax с альфа-бета отсечением."""
        if depth == 0 or self.is_game_over(board):
            return self.evaluate_board(board)

        if is_maximizing:
            max_eval = float('-inf')
            for move in self.generate_moves(board, 1):
                new_board = self.make_move(copy.deepcopy(board), move)
                eval = self.minimax(new_board, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.generate_moves(board, 2):
                new_board = self.make_move(copy.deepcopy(board), move)
                eval = self.minimax(new_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def generate_moves(self, board, player):
        """Генерирует все возможные ходы для игрока."""
        moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == player:
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < len(board) and 0 <= nc < len(board[0]) and board[nr][nc] == 0:
                            moves.append((row, col, nr, nc))
        return moves

    def make_move(self, board, move):
        """Выполняет ход на доске."""
        start_row, start_col, end_row, end_col = move
        board[end_row][end_col] = board[start_row][start_col]
        board[start_row][start_col] = 0
        self.check_capture(board, end_row, end_col)
        return board

    def check_capture(self, board, row, col):
        """Проверяет и удаляет шашки противника, если они захвачены."""
        opponent = 2 if board[row][col] == 1 else 1  # Определяем противника
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            r1, c1 = row + dr, col + dc
            r2, c2 = row + 2 * dr, col + 2 * dc
            if (0 <= r1 < len(board) and 0 <= c1 < len(board[0]) and
                0 <= r2 < len(board) and 0 <= c2 < len(board[0])):
                if board[r1][c1] == opponent and board[r2][c2] == board[row][col]:
                    board[r1][c1] = 0  # Удаляем шашку противника

    def evaluate_board(self, board):
        """Оценивает текущее состояние доски."""
        red_pieces = sum(row.count(1) for row in board)
        black_pieces = sum(row.count(2) for row in board)
        return red_pieces - black_pieces  # Чем больше фишек у красных, тем лучше для бота

    def is_game_over(self, board):
        """Проверяет, завершена ли игра."""
        red_pieces = sum(row.count(1) for row in board)
        black_pieces = sum(row.count(2) for row in board)
        return red_pieces == 0 or black_pieces == 0

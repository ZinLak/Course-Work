import tkinter as tk
import time
from tkinter import font, messagebox
from registration import UserManager
from modules.game_engine import PetteiaEngine
from modules.ai_engine import PetteiaAI

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Игра Петтейя")

        WINDOW_WIDTH = 800
        WINDOW_HEIGHT = 900
        self.center_window(root, WINDOW_WIDTH, WINDOW_HEIGHT)

        self.root.resizable(False, False)

        self.title_font = font.Font(family="Helvetica", size=32, weight="bold", slant="italic")
        self.button_font = font.Font(family="Helvetica", size=14, weight="bold")

        self.logged_in_user = None
        self.user_manager = UserManager()

        self.current_frame = None

        self.ai = PetteiaAI(depth=3)

        self.in_game = False
        self.timer_running = False

        self.create_top_bar()
        self.show_main_menu()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        position_top = (screen_height / 2) - (height / 2)
        position_left = (screen_width / 2) - (width / 2)
        window.geometry(f"{width}x{height}+{int(position_left)}+{int(position_top)}")

    def clear_frame(self):
        """Удаляет текущий виджет."""
        if self.current_frame is not None:
            self.current_frame.destroy()

    def create_top_bar(self):
        """Создает верхнюю панель с кнопкой 'Профиль' и 'Выход'."""
        self.top_bar = tk.Frame(self.root, bg="white", height=50)
        self.top_bar.pack(fill=tk.X)

        self.profile_button = tk.Button(
            self.top_bar,
            text="Профиль",
            font=("Helvetica", 12, "bold"),
            bg="#ADD8E6",
            fg="#000000",
            width=10,
            command=self.show_profile,
        )
        self.profile_button.pack(side=tk.LEFT, padx=10)

        exit_button = tk.Button(
            self.top_bar,
            text="Выход",
            font=("Helvetica", 12, "bold"),
            bg="#FFB6C1",
            fg="#000000",
            width=10,
            command=self.exit_game,
        )
        exit_button.pack(side=tk.RIGHT, padx=10)

    def update_top_bar(self):
        """Обновляет текст кнопки 'Профиль' в зависимости от состояния пользователя."""
        if self.logged_in_user:
            self.profile_button.config(text=f"Профиль: {self.logged_in_user}")
        else:
            self.profile_button.config(text="Профиль")

    def clear_top_bar(self):
        """Удаляет текущую верхнюю панель"""
        if hasattr(self, "top_bar") and self.top_bar:
            self.top_bar.destroy()

    def create_top_bar_in_game(self):
        """Создает верхнюю панель для игрового интерфейса."""
        self.top_bar = tk.Frame(self.root, bg="white", height=50)
        self.top_bar.pack(fill=tk.X)

        leave_button = tk.Button(
            self.top_bar,
            text="Покинуть сессию",
            font=("Helvetica", 12, "bold"),
            bg="#FFB6C1",
            fg="#000000",
            width=15,
            command=self.confirm_leave_game,
        )
        leave_button.pack(side=tk.LEFT, padx=10)

        self.timer_label = tk.Label(
            self.top_bar,
            text="00:00",
            font=("Helvetica", 14, "bold"),
            bg="white",
        )
        self.timer_label.pack(side=tk.LEFT, expand=True)

    def start_timer(self, seconds):
        """Запускает таймер на заданное количество секунд."""
        self.timer_running = True
        self.start_time = time.time() - seconds
        self.update_session_timer()

    def update_session_timer(self):
        """Обновляет значение таймера."""
        if self.in_game and self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            self.timer_label.config(text=f"{minutes:02}:{seconds:02}")
            self.root.after(1000, self.update_session_timer)

    def stop_timer(self):
        self.timer_running = False

    def show_main_menu(self):
        """Отображение главного меню."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="white")
        self.current_frame.pack(expand=True, fill=tk.BOTH)

        title_label = tk.Label(
            self.current_frame,
            text="Игра Петтейя",
            font=self.title_font,
            bg="white",
            fg="#4B0082",
        )
        title_label.pack(pady=20)

        btn_computer = tk.Button(
            self.current_frame,
            text="Игра с компьютером",
            font=self.button_font,
            bg="#ADD8E6",
            fg="#000000",
            width=25,
            height=2,
            command=self.start_game_with_computer,
        )
        btn_computer.pack(pady=10)

        btn_friend = tk.Button(
            self.current_frame,
            text="Игра с другом",
            font=self.button_font,
            bg="#90EE90",
            fg="#000000",
            width=25,
            height=2,
            command=self.start_game_with_friend,
        )
        btn_friend.pack(pady=10)

        btn_rules = tk.Button(
            self.current_frame,
            text="Правила игры",
            font=self.button_font,
            bg="#FFD700",
            fg="#000000",
            width=25,
            height=2,
            command=self.show_rules,
        )
        btn_rules.pack(pady=10)

    def show_profile(self):
        """Отображает профиль или страницу входа/регистрации."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#ededed")
        self.current_frame.pack(expand=True, fill=tk.BOTH)

        if self.logged_in_user:
            profile_label = tk.Label(
                self.current_frame,
                text=f"Добро пожаловать, {self.logged_in_user}!",
                font=self.title_font,
                bg="#ededed",
                fg="#4B0082",
            )
            profile_label.pack(pady=20)

            logout_button = tk.Button(
                self.current_frame,
                text="Выйти из аккаунта",
                font=self.button_font,
                bg="#FFB6C1",
                fg="#000000",
                width=20,
                command=self.logout,
            )
            logout_button.pack(pady=10)
        else:
            tk.Label(self.current_frame, text="Имя пользователя:").pack()
            self.username_entry = tk.Entry(self.current_frame, width=30)
            self.username_entry.pack()

            tk.Label(self.current_frame, text="Пароль:").pack()
            self.password_entry = tk.Entry(self.current_frame, show="*", width=30)
            self.password_entry.pack()

            tk.Button(self.current_frame, text="Вход", command=self.login, width=20).pack(pady=5)
            tk.Button(self.current_frame, text="Регистрация", command=self.register, width=20).pack(pady=5)

            self.message_label = tk.Label(self.current_frame, text="")
            self.message_label.pack()

        btn_back = tk.Button(
            self.current_frame,
            text="Главное меню",
            font=self.button_font,
            bg="#FFB6C1",
            fg="#000000",
            width=15,
            height=1,
            command=self.show_main_menu,
        )
        btn_back.pack(pady=10)

    def login(self):
        """Обрабатывает вход пользователя."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_manager.authenticate_user(username, password):
            self.logged_in_user = username
            self.update_top_bar()
            self.show_profile()
        else:
            self.message_label.config(text="Ошибка входа!", fg="red")

    def register(self):
        """Обрабатывает регистрацию пользователя."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.user_manager.register_user(username, password)
            self.logged_in_user = username
            self.update_top_bar()
            self.show_profile()
        except ValueError as e:
            self.message_label.config(text=f"Ошибка: {str(e)}", fg="red")

    def logout(self):
        """Выход из аккаунта."""
        self.logged_in_user = None
        self.update_top_bar()
        self.show_profile()

    def clear_game_screen(self):
        if hasattr(self, 'game_gui') and self.game_gui:
            self.game_gui.destroy()
            self.game_gui = None

    def confirm_leave_game(self):
        if messagebox.askyesno('Вы действительно хотите покинуть игровую сессию?'):
            self.in_game = False
            self.clear_top_bar()
            self.create_top_bar()
            self.clear_game_screen()
            self.stop_timer()
            self.show_main_menu()

    def exit_game(self):
        """Выход из игры."""
        self.root.quit()

    def start_game_with_computer(self):
        """Начинаем игру с компьютером."""
        if not self.logged_in_user:
            messagebox.showerror("Вы не вошли в аккаунт","Вы должны войти в аккаунт, чтобы начать игру.")
            self.show_profile()
            return
        self.in_game=True
        self.clear_frame()
        self.clear_top_bar()
        self.create_top_bar_in_game()

        self.engine = PetteiaEngine()
        self.game_gui = GameGUI(self.root, self.engine, parent_app=self)

        self.start_timer(0)
        self.game_gui.canvas.bind("<Button-1>", self.handle_player_move)

    def handle_player_move(self, event):
        """Обрабатывает ход игрока и запускает ход бота."""
        col = event.x // self.game_gui.cell_size
        row = event.y // self.game_gui.cell_size

        if self.engine.select_piece(row, col):
            self.engine.check_capture(row, col)
            self.engine.switch_player()
            self.game_gui.draw_board()

            if self.engine.is_game_over():
                self.game_gui.show_game_over()
                return

            self.handle_ai_move()

    def handle_ai_move(self):
        """Ход бота."""
        best_move = self.ai.find_best_move(self.engine)
        if best_move:
            start_row, start_col, end_row, end_col = best_move
            self.engine.board[end_row][end_col] = self.engine.board[start_row][start_col]
            self.engine.board[start_row][start_col] = 0
            self.engine.check_capture(end_row, end_col)

        self.engine.switch_player()
        self.game_gui.draw_board()

        if self.engine.is_game_over():
            self.game_gui.show_game_over()

    def start_game_with_friend(self):
        """Начинаем игру с другом."""
        if not self.logged_in_user:
            messagebox.showerror("Вы не вошли в аккаунт","Вы должны войти в аккаунт, чтобы начать игру.")
            self.show_profile()
            return
        
        self.in_game=True
        self.clear_frame()
        self.clear_top_bar()
        self.create_top_bar_in_game()
        engine = PetteiaEngine()
        self.game_gui = GameGUI(self.root, engine, parent_app=self)
        
        self.start_timer(0)

    def show_rules(self):
        """Отображаем правила игры."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="white")
        self.current_frame.pack(expand=True, fill=tk.BOTH)

        rules_text = """
        Игра «Петтейя» — это стратегическая настольная игра для двух игроков. Она основана на исторических реконструкциях древнегреческих игр, адаптированных для современных условий. Ниже приводится описание правил, используемых в текущей версии игры.

        Игровое поле представляет собой квадратную доску размером 8x8 клеток. Каждая клетка может быть светлой или тёмной. На тёмных клетках располагаются шашки. Доска симметрична, что обеспечивает равные условия для обоих игроков.

       . - У каждого игрока по 8 шашек. 
        - Шашки распологаются на первой линии доски, ближайшей к игроку, заполняя весь ряд.
        - Первый игрок использует красные шашки, второй - черные

        1. Цель игры:  
        - Уничтожить или заблокировать все шашки противника.  
        - Проигрывает игрок, который больше не может совершить ход.  

        2. Ходы шашек:  
        - Шашка может перемещаться только на одну соседнюю свободную клетку.
        - Ход осуществляется по вертикали или горизонтали. Перемещение по диагонали запрещено.  

        3. Захват шашек противника:  
        - Захват осуществляется путём зажатия вражеской шашки между двумя своими.  
        - Например, если шашка противника находится между двумя шашками одного игрока, то она удаляется с доски.  
        - Зажатие считается только если оно образовалось после хода игрока. Если шашка сама оказывается между двумя вражескими — это не считается захватом.  

        4. Запрет ничейных ситуаций:  
        - Для предотвращения бесконечного перемещения одной шашки внутри "крепости", запрещается повторение позиции. Если ситуация повторяется, игрок обязан изменить расстановку.  

        5. Победа:  
        - Игра заканчивается, когда у одного из игроков не остаётся ни одной шашки, либо все его шашки заблокированы.

        Советы:
        - Старайтесь держать шашки кучно, чтобы они поддерживали друг друга и предотвращали захват.
        - Атакуйте слабые группы противника, чтобы быстро получить численное преимущество.
        - Используйте тактику "двойной угрозы", создавая ситуации, где шашка противника неизбежно будет захвачена.

        Игра требует внимательности, логического мышления и умения предугадывать действия соперника. Удачи!

        """
        rules_label = tk.Label(
            self.current_frame,
            text="Правила игры",
            font=self.title_font,
            bg="white",
            fg="#4B0082",
        )
        rules_label.pack(pady=10)

        text = tk.Text(
            self.current_frame, wrap=tk.WORD, font=("Helvetica", 12), bg="#F5F5F5"
        )
        text.insert(tk.END, rules_text)
        text.configure(state=tk.DISABLED)
        text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        btn_back = tk.Button(
            self.current_frame,
            text="Главное меню",
            font=self.button_font,
            bg="#FFB6C1",
            fg="#000000",
            width=15,
            height=1,
            command=self.show_main_menu,
        )
        btn_back.pack(pady=10)

class GameGUI:
    def __init__(self, root, engine, parent_app=None):
        self.root = root
        self.engine = engine
        self.parent_app = parent_app

        self.board_size = engine.board_size
        self.cell_size = 60

        self.game_frame = tk.Frame(root)
        self.game_frame.pack()

        self.labels_top_frame = tk.Frame(self.game_frame)
        self.labels_left_frame = tk.Frame(self.game_frame)
        self.labels_top_frame.pack(side=tk.TOP, fill=tk.X)
        self.labels_left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas = tk.Canvas(self.game_frame, width=self.board_size * self.cell_size,
                                height=self.board_size * self.cell_size)
        self.canvas.pack()

        self.info_label = tk.Label(self.game_frame, font=("Arial", 14), anchor="w")
        self.info_label.pack(fill=tk.X)

        self.draw_labels()
        self.draw_board()

        self.canvas.bind("<Button-1>", self.handle_click)
        self.update_turn_info()

    def destroy(self):
        self.canvas.destroy()
        self.info_label.destroy()
        self.game_frame.destroy()

    def draw_labels(self):
        """Рисует метки на поле."""
        for col in range(self.board_size):
            tk.Label(self.labels_top_frame, text=chr(ord('a') + col), font=("Arial", 12)).grid(row=0, column=col,padx=self.cell_size // 2 - 4)

        for row in range(self.board_size):
            tk.Label(self.labels_left_frame, text=str(row + 1), font=("Arial", 12)).grid(row=row, column=0, pady=self.cell_size // 2 - 12)

    def draw_board(self):
        """Рисует игровое поле."""
        self.canvas.delete("all")
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1, y1 = col * self.cell_size, row * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                piece = self.engine.board[row][col]
                if piece == 1:
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="red")
                elif piece == 2:
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="black")

                if self.engine.selected_piece == (row, col):
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", width=3)

    def handle_click(self, event):
        """Обрабатывает клик по доске."""
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if self.engine.select_piece(row, col):
                self.engine.check_capture(row, col)
                self.engine.switch_player()
                self.update_turn_info()
                if self.engine.is_game_over():
                    self.show_game_over()

            self.draw_board()

    def update_turn_info(self):
        """Обновляет информацию о текущем ходе."""
        self.info_label.config(text=f"Ход: {self.engine.evaluate_turn()}")

    def show_game_over(self):
        """Отображает сообщение об окончании игры."""
        if self.parent_app:
            self.parent_app.stop_timer()
        winner = "Красные" if self.engine.current_player == 2 else "Чёрные"
        if messagebox.askyesno("Игра окончена", f"Победитель: {winner}\n\nХотите начать заново?"):
            self.restart_game()
        else:
            self.exit_to_main_menu()

    def restart_game(self):
        """Перезапускает текущую игровую сессию."""
        if self.parent_app:
            self.parent_app.stop_timer()
            self.parent_app.start_timer(0)
        self.engine.setup_board()
        self.engine.current_player = 2
        self.draw_board()
        self.update_turn_info()

    def exit_to_main_menu(self):
        """Возвращает пользователя в главное меню."""
        if self.parent_app:
            self.parent_app.confirm_leave_game() 

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

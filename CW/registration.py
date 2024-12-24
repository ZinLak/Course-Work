import json
import bcrypt

class UserManager:
    def __init__(self, db_file="users.json"):
        self.db_file = db_file
        self.users = self.load_users()

    def load_users(self):
        """Загружает пользователей из базы данных."""
        try:
            with open(self.db_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_users(self):
        """Сохраняет пользователей в базу данных."""
        with open(self.db_file, "w") as file:
            json.dump(self.users, file, indent=4)

    def register_user(self, username, password):
        """Регистрирует нового пользователя."""
        if username in self.users:
            raise ValueError("Пользователь с таким именем уже существует.")
        
        # Хешируем пароль
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.users[username] = {
            "password": hashed_password.decode('utf-8'),
            "score": 0  # Можно хранить дополнительные данные, например, очки
        }
        self.save_users()
        return True

    def authenticate_user(self, username, password):
        """Аутентифицирует пользователя."""
        if username not in self.users:
            return False
        
        stored_password = self.users[username]["password"]
        return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))

    def update_score(self, username, score):
        """Обновляет очки пользователя."""
        if username in self.users:
            self.users[username]["score"] = score
            self.save_users()
        else:
            raise ValueError("Пользователь не найден.")

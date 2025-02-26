from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO
import redis
import bcrypt

# Инициализация Flask-приложения
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Ключ для сессий пользователей
socketio = SocketIO(app)  # Подключение WebSocket

# Подключение к базе данных Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

@app.route('/')
def home():
    """Home page: redirects users."""
    if "user" in session:
        return redirect(url_for("profile"))  # Если пользователь вошел, направить в профиль
    return redirect(url_for("login"))  # Иначе направить на страницу входа

@app.route('/login', methods=["GET", "POST"])
def login():
    """Login page."""
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].encode('utf-8')
        
        # Получение данных пользователя из Redis
        user_data = redis_client.hgetall(f"user:{username}")
        if user_data and bcrypt.checkpw(password, user_data.get("password").encode('utf-8')):
            session["user"] = username  # Сохранение имени пользователя в сессии
            return redirect(url_for("profile"))  # Перенаправление в профиль
        
        return "Invalid login or password!", 403  # Ошибка авторизации
    
    return render_template("login.html")  # Отображение страницы входа

@app.route('/register', methods=["GET", "POST"])
def register():
    """New user registration page."""
    if request.method == "POST":
        username = request.form["username"].strip()
        password = bcrypt.hashpw(request.form["password"].encode('utf-8'), bcrypt.gensalt())
        
        # Проверяем, занято ли имя пользователя
        all_users = redis_client.keys("user:*")
        existing_usernames = [redis_client.hget(user, "username") for user in all_users]
        if username in existing_usernames:
            return "User already exists or this Username is already taken!", 400
        
        # Сохранение нового пользователя в Redis
        redis_client.hset(f"user:{username}", "username", username)
        redis_client.hset(f"user:{username}", "password", password.decode('utf-8'))
        
        # Отправка уведомления через WebSocket о новом пользователе
        socketio.emit("new_user", {"user": username})
        return redirect(url_for("login"))  # Перенаправление на страницу входа
    
    return render_template("register.html")  # Отображение страницы регистрации

@app.route('/profile', methods=["GET", "POST"])
def profile():
    """User profile page."""
    if "user" not in session:
        return redirect(url_for("login"))  # Если не авторизован, отправить на вход
    
    username = session["user"]  # Получение имени пользователя
    user_data = redis_client.hgetall(f"user:{username}")
    
    if request.method == "POST":
        new_info = request.form["info"].strip()
        redis_client.hset(f"user:{username}", "info", new_info)  # Обновление информации в профиле
    
    return render_template("profile.html", name=username, info=user_data.get("info", ""))

@app.route('/logout')
def logout():
    """Logout."""
    session.pop("user", None)  # Удаление пользователя из сессии
    return redirect(url_for("login"))  # Перенаправление на страницу входа

if __name__ == "__main__":
    socketio.run(app, host="localhost", port=5000)  # Запуск сервера
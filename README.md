📍 Flask-Based Authentication with Redis

📎 Project Description
This project implements an authentication system using Flask and Redis. Additionally, it features WebSocket notifications that inform active users when new accounts are registered.

💻 Development Stack 
- Frontend: HTML, CSS
- Backend: Flask
- Database: Redis
- Password encryption: bcrypt
- WebSockets: Flask-SocketIO

📌 Task 1: Static Profile Page

✅ Implemented a static profile page using HTML + CSS.
✅ The page contains a heading, text, and an image.
✅ The design was chosen freely.
✅ The static page is served at the root ('/') and later redirected.
✅ Static resources (CSS, images) are properly served.
✅ Used `render_template()` for rendering.
✅ `/` redirects to `/login`, which further redirects to `/profile` after authentication.

📌 Task 2: Authentication System with Database

Basic Requirements:

✅ Application listens on `localhost:5000`.
✅ Login page is rendered at `http://localhost:5000/login`.
✅ Upon successful authentication, users are redirected to `/profile`.
✅ `/profile` is accessible only for authenticated users.
✅ User credentials are stored in Redis.

Advanced Requirements:

✅ Registration feature implemented (`/register`).
✅ Passwords are hashed using `bcrypt`.
✅ Logout functionality.
❌ Password change feature is missing.
❌ Profile picture updates are not available (default profile picture is used).
✅ Profile information can be updated.

Challenging Part:

✅ Implemented WebSocket notifications – active users receive messages when a new account is registered.

🚀 How to Run

1. Install Python and Dependencies
- Download and install Python: [Python Download](https://www.python.org/downloads/release/python-3132/).
- Open CMD as administrator and run:
  pip install flask flask-socketio redis bcrypt
  python.exe -m pip install --upgrade pip

2. Install and Run Redis
- Install Redis via Chocolatey:
  choco install redis
- Start the Redis server:
  redis-server

3. Start the Project
- Run the Flask application:
  python app.py
- Open the browser and go to: [http://localhost:5000](http://localhost:5000).
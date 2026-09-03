# Real-Time Chat & Notification Service

A real-time multi-room chat application built with **FastAPI, WebSockets, MongoDB, and JWT authentication**. Users can securely register and log in, join different chat rooms, exchange messages in real time, and receive join/leave notifications.

## 🚀 Features

* User registration and login
* Secure password hashing with bcrypt
* JWT-based authentication
* Real-time messaging using WebSockets
* Multiple chat rooms
* Join and leave notifications
* Persistent chat history using MongoDB
* REST API for retrieving chat history
* Simple web frontend using HTML, CSS, and JavaScript

## 🛠️ Tech Stack

**Backend**

* Python
* FastAPI
* WebSockets
* MongoDB
* Motor
* JWT
* bcrypt

**Frontend**

* HTML
* CSS
* JavaScript

## 📁 Project Structure

```text
realtime-chat/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── manager.py
│   ├── auth.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sahilkesark/Realtime-chat.git
cd Realtime-chat
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Start MongoDB

Make sure MongoDB is running locally on:

```text
mongodb://localhost:27017
```

### 5. Start the FastAPI server

```bash
cd backend
python -m uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## 💻 Running the Frontend

Open another terminal:

```bash
cd frontend
python3 -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

## 🧪 Testing the Application

1. Register a new user.
2. Log in using your credentials.
3. Select a chat room.
4. Click **Join Room**.
5. Open another browser window and create another account.
6. Join the same room.
7. Send messages and see them appear in real time.
8. Leave or close a connection to see the notification.
9. Rejoin the room to load previously stored messages.

## 🔌 API Endpoints

| Method    | Endpoint                    | Description                     |
| --------- | --------------------------- | ------------------------------- |
| GET       | `/`                         | Check if the service is running |
| POST      | `/register`                 | Register a new user             |
| POST      | `/login`                    | Authenticate a user             |
| GET       | `/rooms/{room_id}/messages` | Retrieve room message history   |
| WebSocket | `/ws/{room_id}`             | Real-time room communication    |

## 🔐 Authentication

The application uses **JWT tokens** for authentication.

Passwords are securely hashed using **bcrypt** before being stored in MongoDB.

WebSocket connections also require a valid JWT token.

## 📌 Future Improvements

* Online/offline user status
* Private one-to-one messaging
* Message timestamps in the UI
* Typing indicators
* Message read status
* File and image sharing
* Redis-based scaling for multiple backend instances

## 👨‍💻 Author

**Sahil N Kesarkar**

Computer Science & Engineering Graduate

GitHub: [sahilkesark](https://github.com/sahilkesark)

---

⭐ If you found this project useful, consider giving it a star!

# 🌦️ WeatherPro

A modern, feature-rich weather dashboard built with **Flask**, **SQLAlchemy**, and **PostgreSQL**, providing real-time weather information, air quality data, forecasts, user authentication, and a beautiful glassmorphism interface.

---

## 📸 Screenshots

> Add screenshots of your application here.

- Dashboard
- Login
- Register
- User Profile
- Dark Theme
- Light Theme

---

## ✨ Features

### 🔐 Authentication
- User Registration
- Secure Login & Logout
- Password Hashing
- Email Verification
- Session Management

### 🌤 Weather
- Real-time Weather
- Current Temperature
- Weather Description
- Feels Like Temperature
- Humidity
- Wind Speed
- Pressure
- Visibility
- Sunrise & Sunset
- UV Index
- Air Quality Index (AQI)

### 📅 Forecasts
- 5-Day Forecast
- Hourly Forecast
- Dynamic Weather Icons

### ⭐ User Features
- Save Favorite Cities
- Remove Favorites
- Search History
- User Profile
- Profile Management

### 🎨 UI
- Responsive Design
- Glassmorphism Interface
- Dark Theme
- Blue Theme
- Beautiful Animations
- Mobile Friendly

### ☁ Database
- PostgreSQL (Neon)
- SQLAlchemy ORM
- Flask-Migrate
- Persistent Cloud Storage

---

# 🛠 Tech Stack

## Backend

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- Flask-Mail
- SQLAlchemy
- PostgreSQL
- Gunicorn

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Font Awesome

## APIs

- OpenWeatherMap API
- Gmail SMTP

---

# 📂 Project Structure

```
WeatherPro
│
├── app
│   ├── auth
│   ├── weather
│   ├── models.py
│   ├── extensions.py
│   ├── templates
│   └── static
│
├── migrations
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/WeatherPro.git
```

Move into the project

```bash
cd WeatherPro
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
SECRET_KEY=

API_KEY=

DATABASE_URL=

MAIL_USERNAME=

MAIL_PASSWORD=

RESEND_API_KEY=
```

---

# 🗄 Database Migration

Initialize migrations

```bash
flask db init
```

Generate migration

```bash
flask db migrate -m "Initial migration"
```

Apply migration

```bash
flask db upgrade
```

---

# ▶ Running the Application

```bash
python run.py
```

The application will be available at

```
http://127.0.0.1:5000
```

---

# 📦 Deployment

This project is production-ready and can be deployed on platforms such as:

- Railway
- Render
- Fly.io
- PythonAnywhere

with a PostgreSQL database hosted on Neon.

---

# 🔮 Future Improvements

- Weather Maps
- Geolocation Support
- Severe Weather Alerts
- Weather Charts
- Multiple Languages
- Unit Conversion
- PWA Support
- Docker Support
- CI/CD Pipeline
- Admin Dashboard

---

# 👨‍💻 Author

**Chakradhar Yerrarbolu**

GitHub:
https://github.com/yourusername

LinkedIn:
https://linkedin.com/in/yourprofile

---

# 📄 License

This project is licensed under the MIT License.

---

⭐ If you found this project useful, consider giving it a star!

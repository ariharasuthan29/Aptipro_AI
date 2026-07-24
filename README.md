# AptiPro AI - Online Aptitude Preparation & Proctored Examination System

AptiPro AI is a comprehensive, production-grade Web Application built with **Django**, **Bootstrap 5**, **Chart.js**, and **OpenCV**. It provides automated daily practice drills, placement examination simulations, real-time proctoring security logs, and role-based student/admin dashboards.

---

## 🌐 Quick Access Links

* **Live Web Application**: [https://aptipro-ai.onrender.com/](https://aptipro-ai.onrender.com/)
* **User Login**: [https://aptipro-ai.onrender.com/](https://aptipro-ai.onrender.com/)
* **User Registration**: [https://aptipro-ai.onrender.com/register/](https://aptipro-ai.onrender.com/register/)
* **Local Development Server**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🌟 Key Features

### 🎓 Student Module
- **Dashboard & Performance Metrics**: Real-time score trends, category accuracy charts, streak counters, and rank points.
- **Daily Practice Drills**: Single-card pagination flow with option locking, instant explanation reveals, and 14 canonical aptitude categories.
- **Placement Exam Simulation**: 40-question randomized mock placement exams with automated time management.
- **AI Proctoring & Integrity Rules**: Fullscreen enforcement, tab-switch monitoring, and OpenCV webcam face presence verification.
- **Leaderboards & Profiles**: Real-time rankings, badges, and candidate profile management.

### 🛡️ Admin Management Console
- **Role-Based Authentication**: Isolated Admin Console with custom sidebars and navigation menus.
- **Question Bank Management**: Single question authoring and bulk Excel (`.xlsx`/`.csv`) dataset importer with automatic classifier.
- **Category & Exam Controls**: Manage 14 canonical categories and view complete exam session histories.
- **Security & Violation Audit Logs**: Inspect proctoring violation warnings and webcam snapshots.
- **System Settings**: Configurable exam durations, strike limits, and passing thresholds.

---

## 🏗️ Technology Stack

- **Backend**: Python 3.x, Django 5.x
- **Frontend**: HTML5, Vanilla CSS, JavaScript (ES6+), Bootstrap 5, Select2, Chart.js
- **Computer Vision & Proctoring**: OpenCV (`opencv-python`), NumPy
- **Database**: SQLite3 (Local development)
- **Data Import/Export**: `openpyxl`, `pandas`

---

## 🚀 Quick Start Guide

### 1. Clone Repository & Setup Environment
```bash
git clone https://github.com/ariharasuthan29/Aptipro_AI.git
cd Aptipro_AI
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations & Seed Data
```bash
python manage.py migrate
python manage.py seed_questions
```

### 5. Run Local Development Server
```bash
python manage.py runserver 8000
```

Access locally at `http://127.0.0.1:8000/`

---

## 🛡️ License & Copyright
Developed for AptiPro AI Placement Preparation System.

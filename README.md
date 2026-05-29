# 🏛️ Hall Allotment System

A web-based **Exam Hall Allotment System** built with **Python Flask** that automates the process of allocating students to examination halls. It manages departments, classes, students, halls, and exam schedules — all from a clean, responsive web interface.

---

## ✨ Features

- 🔐 **User Authentication** — Register, login, and logout with session management
- 🏢 **Department Management** — Add and manage departments
- 📚 **Class Management** — Create and edit classes under departments
- 👨‍🎓 **Student Management** — Add students individually or import from CSV
- 🏛️ **Hall Management** — Add exam halls with capacity; supports CSV import
- 📅 **Exam Scheduling** — Schedule exams for classes with date and time
- 📋 **Automatic Hall Allotment** — Automatically distributes students to halls based on capacity
- 📊 **Dashboard** — Overview of total halls, exams, students, and capacity
- 📥 **Excel Import** — Import student data from Excel (`.xlsx`) files

---

## 🛠️ Tech Stack

| Layer      | Technology          |
|------------|---------------------|
| Backend    | Python 3, Flask     |
| Frontend   | HTML, CSS, Jinja2   |
| Data Store | CSV files           |
| Auth       | Flask Sessions      |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/hall-allotment-system.git
   cd hall-allotment-system
   ```

2. **Create a virtual environment** *(recommended)*
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Linux/macOS
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://localhost:5000
   ```

---

## 📁 Project Structure

```
Hall Allotment System/
│
├── app.py               # Main Flask application & routes
├── data_manager.py      # Data access layer (CSV read/write)
├── import_excel.py      # Excel import utility
├── requirements.txt     # Python dependencies
│
├── Data/                # CSV data files (auto-generated)
│   ├── students.csv
│   ├── halls.csv
│   ├── classes.csv
│   ├── departments.csv
│   ├── exams.csv
│   ├── allotments.csv
│   └── users.csv
│
├── static/              # CSS and JavaScript assets
│   ├── css/
│   └── js/
│
└── templates/           # HTML Jinja2 templates
```

---

## 📋 Usage

1. **Register** a new admin account on the register page.
2. **Login** with your credentials.
3. Add **Departments** → **Classes** → **Students**.
4. Add **Halls** with their seating capacity.
5. Schedule an **Exam** for a class.
6. Click **Allot** to automatically assign students to halls.
7. View the **Allotment Sheet** grouped by hall.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> Built with ❤️ using Python Flask

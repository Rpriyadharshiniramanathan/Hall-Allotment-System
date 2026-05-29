# 🏛️ Hall Allotment System

A web-based exam hall allotment management system built with **Python Flask**. It automates the process of assigning students to examination halls based on availability and capacity — saving time and eliminating manual scheduling errors.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
- [Usage](#usage)
- [CSV Import Format](#csv-import-format)
- [Data Storage](#data-storage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- 🔐 **User Authentication** — Register and login with session-based access control
- 🏢 **Department Management** — Add and manage academic departments with cascade deletion
- 📚 **Class Management** — Organize classes under departments; edit or delete with full cascade support
- 👩‍🎓 **Student Management** — Add students individually or bulk-import via CSV file
- 🏛️ **Hall Management** — Add exam halls with capacity; bulk-import via CSV
- 📝 **Exam Scheduling** — Schedule exams with subject, date, and time slot per class
- ⚡ **Auto Allotment** — Smart algorithm that assigns students to halls based on availability and capacity
- 🔁 **Conflict Detection** — Prevents double-booking of halls using time-overlap checks
- 🧹 **Auto Cleanup** — Past exams and their allotments are automatically removed
- 📊 **Dashboard** — Overview of total halls, exams, students, and capacity at a glance
- 📄 **Allotment View** — View detailed seating arrangements grouped by hall for each exam

---

## 🛠️ Tech Stack

| Layer        | Technology              |
|-------------|--------------------------|
| Backend     | Python 3, Flask 2.3.3    |
| Frontend    | HTML5, CSS3, Jinja2      |
| Data Store  | CSV files (no DB needed) |
| Auth        | Flask Sessions           |

---

## 📁 Project Structure

```
Hall Allotment System/
├── app.py                  # Main Flask application & route definitions
├── data_manager.py         # All data access logic (CRUD operations)
├── import_excel.py         # Excel import utility
├── requirements.txt        # Python dependencies
├── Data/                   # CSV data files (auto-generated on first use)
│   ├── users.csv
│   ├── departments.csv
│   ├── classes.csv
│   ├── students.csv
│   ├── halls.csv
│   ├── exams.csv
│   └── allotments.csv
├── templates/              # Jinja2 HTML templates
│   ├── layout.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── departments.html
│   ├── classes.html
│   ├── edit_class.html
│   ├── students.html
│   ├── halls.html
│   ├── exams.html
│   └── allotment_view.html
└── static/                 # Static assets (CSS, JS, images)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rpriyadharshiniramanathan/Hall-Allotment-System.git
   cd Hall-Allotment-System
   ```

2. **Create a virtual environment** *(recommended)*
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

```bash
python app.py
```

The application will start at **http://127.0.0.1:5000** in debug mode.

---

## 📖 Usage

1. **Register** a new account or **Login** with existing credentials.
2. Navigate to **Departments** → Add your academic departments.
3. Navigate to **Classes** → Add classes and assign them to a department.
4. Navigate to **Students** → Add students individually or import them via CSV.
5. Navigate to **Halls** → Add exam halls with seating capacity.
6. Navigate to **Exams** → Schedule an exam (subject, date, time) for a class.
7. Click **Allot** next to an exam to automatically assign students to available halls.
8. Click **View** to see the full seating arrangement grouped by hall.

> **Note:** Past exams are automatically cleaned up on each dashboard and exam page load.

---

## 📥 CSV Import Format

### Students CSV

```csv
roll_number,name
CS001,Alice Johnson
CS002,Bob Smith
```

### Halls CSV

```csv
name,capacity
Hall A,50
Lab B,30
```

---

## 🗄️ Data Storage

All data is stored as **CSV files** inside the `Data/` directory — no database installation required. Files are created automatically when the application runs for the first time.

| File               | Contents                        |
|--------------------|---------------------------------|
| `users.csv`        | Registered user credentials     |
| `departments.csv`  | Department records               |
| `classes.csv`      | Class records with department FK |
| `students.csv`     | Student records with class FK    |
| `halls.csv`        | Hall names and capacities        |
| `exams.csv`        | Scheduled exam details           |
| `allotments.csv`   | Student-to-hall assignment records |

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">Made with ❤️ using Python & Flask</p>

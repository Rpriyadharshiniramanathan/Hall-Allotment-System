import csv
import os
import uuid
from datetime import datetime

BASE_DATA_DIR = os.path.join(os.path.dirname(__file__), 'Data')
USERS_FILE = os.path.join(BASE_DATA_DIR, 'users.csv')

def get_data_dir(username):
    return os.path.join(BASE_DATA_DIR, username)

def ensure_user_dir(username):
    user_dir = get_data_dir(username)
    os.makedirs(user_dir, exist_ok=True)

def get_file_path(username, filename):
    return os.path.join(get_data_dir(username), filename)

def read_csv(username, filename):
    filepath = get_file_path(username, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(username, filename, fieldnames, data):
    filepath = get_file_path(username, filename)
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def append_csv(username, filename, fieldnames, row):
    filepath = get_file_path(username, filename)
    file_exists = os.path.exists(filepath)
    with open(filepath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists or os.path.getsize(filepath) == 0:
            writer.writeheader()
        writer.writerow(row)

# --- Users (Auth) ---
def authenticate_user(username, password):
    os.makedirs(BASE_DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for u in reader:
            if u.get('username') == username and u.get('password') == password:
                return True
    return False

def add_user(username, password):
    os.makedirs(BASE_DATA_DIR, exist_ok=True)
    users = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            users = list(reader)
    for u in users:
        if u.get('username') == username:
            return False, "Username already exists"
    file_exists = os.path.exists(USERS_FILE)
    with open(USERS_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['username', 'password'])
        if not file_exists or os.path.getsize(USERS_FILE) == 0:
            writer.writeheader()
        writer.writerow({'username': username, 'password': password})
    # Create user's own data directory
    ensure_user_dir(username)
    return True, "User registered successfully"

# --- Departments ---
def get_departments(username):
    return read_csv(username, 'departments.csv')

def add_department(username, name):
    dept_id = str(uuid.uuid4())
    append_csv(username, 'departments.csv', ['id', 'name'], {'id': dept_id, 'name': name})
    return dept_id

def get_department(username, dept_id):
    for d in get_departments(username):
        if d['id'] == dept_id:
            return d
    return None

def delete_department(username, dept_id):
    depts = get_departments(username)
    updated_depts = [d for d in depts if d['id'] != dept_id]
    write_csv(username, 'departments.csv', ['id', 'name'], updated_depts)

    classes = get_classes(username)
    classes_to_delete = [c['id'] for c in classes if c['department_id'] == dept_id]
    updated_classes = [c for c in classes if c['department_id'] != dept_id]
    if len(classes) != len(updated_classes):
        write_csv(username, 'classes.csv', ['id', 'department_id', 'name'], updated_classes)

        students = get_students(username)
        updated_students = [s for s in students if s['class_id'] not in classes_to_delete]
        if len(students) != len(updated_students):
            write_csv(username, 'students.csv', ['id', 'roll_number', 'name', 'class_id'], updated_students)

# --- Classes ---
def get_classes(username):
    return read_csv(username, 'classes.csv')

def add_class(username, department_id, name):
    class_id = str(uuid.uuid4())
    append_csv(username, 'classes.csv', ['id', 'department_id', 'name'], {'id': class_id, 'department_id': department_id, 'name': name})
    return class_id

def get_class(username, class_id):
    for c in get_classes(username):
        if c['id'] == class_id:
            return c
    return None

def update_class(username, class_id, name, department_id):
    classes = get_classes(username)
    for c in classes:
        if c['id'] == class_id:
            c['name'] = name
            c['department_id'] = department_id
            break
    write_csv(username, 'classes.csv', ['id', 'department_id', 'name'], classes)

def delete_class(username, class_id):
    classes = get_classes(username)
    updated_classes = [c for c in classes if c['id'] != class_id]
    write_csv(username, 'classes.csv', ['id', 'department_id', 'name'], updated_classes)

    students = get_students(username)
    updated_students = [s for s in students if s['class_id'] != class_id]
    if len(students) != len(updated_students):
        write_csv(username, 'students.csv', ['id', 'roll_number', 'name', 'class_id'], updated_students)

# --- Students ---
def get_students(username):
    return read_csv(username, 'students.csv')

def add_student(username, roll_number, name, class_id):
    student_id = str(uuid.uuid4())
    append_csv(username, 'students.csv', ['id', 'roll_number', 'name', 'class_id'],
               {'id': student_id, 'roll_number': roll_number, 'name': name, 'class_id': class_id})
    return student_id

def get_students_by_class(username, class_id):
    return [s for s in get_students(username) if s['class_id'] == class_id]

def import_students_from_csv(username, file_stream, class_id):
    reader = csv.DictReader(file_stream)
    count = 0
    for row in reader:
        roll_number = row.get('roll_number', '').strip()
        name = row.get('name', '').strip()
        if roll_number and name:
            add_student(username, roll_number, name, class_id)
            count += 1
    return count

# --- Halls ---
def get_halls(username):
    return read_csv(username, 'halls.csv')

def add_hall(username, name, capacity):
    hall_id = str(uuid.uuid4())
    append_csv(username, 'halls.csv', ['id', 'name', 'capacity'], {'id': hall_id, 'name': name, 'capacity': capacity})
    return hall_id

def get_hall(username, hall_id):
    for h in get_halls(username):
        if h['id'] == hall_id:
            return h
    return None

def delete_hall(username, hall_id):
    halls = get_halls(username)
    updated_halls = [h for h in halls if h['id'] != hall_id]
    write_csv(username, 'halls.csv', ['id', 'name', 'capacity'], updated_halls)

def import_halls_from_csv(username, file_stream):
    reader = csv.DictReader(file_stream)
    count = 0
    for row in reader:
        name = row.get('name', '').strip()
        capacity = row.get('capacity', '').strip()
        if name and capacity and capacity.isdigit():
            add_hall(username, name, capacity)
            count += 1
    return count

# --- Exams ---
def get_exams(username):
    return read_csv(username, 'exams.csv')

def add_exam(username, class_id, subject, date, start_time, end_time):
    exam_id = str(uuid.uuid4())
    append_csv(username, 'exams.csv', ['id', 'class_id', 'subject', 'date', 'start_time', 'end_time'],
               {'id': exam_id, 'class_id': class_id, 'subject': subject, 'date': date,
                'start_time': start_time, 'end_time': end_time})
    return exam_id

def get_exam(username, exam_id):
    for e in get_exams(username):
        if e['id'] == exam_id:
            return e
    return None

def clean_old_exams(username):
    exams = get_exams(username)
    if not exams:
        return

    allotments = get_allotments(username)
    now = datetime.now()
    valid_exams = []
    deleted_exam_ids = set()

    for e in exams:
        try:
            exam_datetime_str = f"{e['date']} {e['end_time']}"
            exam_end_time = datetime.strptime(exam_datetime_str, "%Y-%m-%d %H:%M")
            if exam_end_time < now:
                deleted_exam_ids.add(e['id'])
            else:
                valid_exams.append(e)
        except ValueError:
            valid_exams.append(e)

    if deleted_exam_ids:
        write_csv(username, 'exams.csv', ['id', 'class_id', 'subject', 'date', 'start_time', 'end_time'], valid_exams)
        valid_allotments = [a for a in allotments if a['exam_id'] not in deleted_exam_ids]
        write_csv(username, 'allotments.csv', ['id', 'exam_id', 'hall_id', 'student_id'], valid_allotments)

# --- Allotments ---
def get_allotments(username):
    return read_csv(username, 'allotments.csv')

def get_allotments_for_exam(username, exam_id):
    return [a for a in get_allotments(username) if a['exam_id'] == exam_id]

def is_hall_available(username, hall_id, date, start_time, end_time, current_exam_id=None):
    exams = get_exams(username)
    allotments = get_allotments(username)

    fmt = '%H:%M'
    try:
        req_start = datetime.strptime(start_time, fmt)
        req_end = datetime.strptime(end_time, fmt)
    except ValueError:
        return False

    for exam in exams:
        if exam['id'] == current_exam_id:
            continue
        if exam['date'] == date:
            e_start = datetime.strptime(exam['start_time'], fmt)
            e_end = datetime.strptime(exam['end_time'], fmt)
            if (req_start < e_end and req_end > e_start):
                exam_allotments = [a for a in allotments if a['exam_id'] == exam['id']]
                if any(a['hall_id'] == hall_id for a in exam_allotments):
                    return False
    return True

def perform_allotment(username, exam_id):
    exam = get_exam(username, exam_id)
    if not exam:
        return False, "Exam not found"

    students = get_students_by_class(username, exam['class_id'])
    if not students:
        return False, "No students found for this class"

    halls = get_halls(username)
    available_halls = [h for h in halls if is_hall_available(
        username, h['id'], exam['date'], exam['start_time'], exam['end_time'], exam_id)]

    available_halls.sort(key=lambda x: int(x['capacity']), reverse=True)

    total_capacity = sum(int(h['capacity']) for h in available_halls)
    if total_capacity < len(students):
        return False, f"Not enough hall capacity. Needed: {len(students)}, Available: {total_capacity}"

    allotment_records = []
    student_idx = 0

    for hall in available_halls:
        capacity = int(hall['capacity'])
        students_to_allocate = min(capacity, len(students) - student_idx)
        for i in range(students_to_allocate):
            student = students[student_idx]
            allotment_records.append({
                'id': str(uuid.uuid4()),
                'exam_id': exam_id,
                'hall_id': hall['id'],
                'student_id': student['id']
            })
            student_idx += 1
        if student_idx >= len(students):
            break

    for record in allotment_records:
        append_csv(username, 'allotments.csv', ['id', 'exam_id', 'hall_id', 'student_id'], record)

    return True, f"Successfully allocated {len(students)} students across {len(set(a['hall_id'] for a in allotment_records))} halls."

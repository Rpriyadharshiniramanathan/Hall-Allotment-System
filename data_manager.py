import csv
import os
import uuid
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def get_file_path(filename):
    return os.path.join(DATA_DIR, filename)

def read_csv(filename):
    filepath = get_file_path(filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(filename, fieldnames, data):
    filepath = get_file_path(filename)
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def append_csv(filename, fieldnames, row):
    filepath = get_file_path(filename)
    file_exists = os.path.exists(filepath)
    with open(filepath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists or os.path.getsize(filepath) == 0:
            writer.writeheader()
        writer.writerow(row)

# --- Users (Auth) ---
def authenticate_user(username, password):
    users = read_csv('users.csv')
    for u in users:
        if u.get('username') == username and u.get('password') == password:
            return True
    return False

def add_user(username, password):
    users = read_csv('users.csv')
    for u in users:
        if u.get('username') == username:
            return False, "Username already exists"
    append_csv('users.csv', ['username', 'password'], {'username': username, 'password': password})
    return True, "User registered successfully"

# --- Departments ---
def get_departments():
    return read_csv('departments.csv')

def add_department(name):
    dept_id = str(uuid.uuid4())
    append_csv('departments.csv', ['id', 'name'], {'id': dept_id, 'name': name})
    return dept_id

def get_department(dept_id):
    for d in get_departments():
        if d['id'] == dept_id:
            return d
    return None

def delete_department(dept_id):
    depts = get_departments()
    updated_depts = [d for d in depts if d['id'] != dept_id]
    write_csv('departments.csv', ['id', 'name'], updated_depts)
    
    # Cascade delete classes
    classes = get_classes()
    classes_to_delete = [c['id'] for c in classes if c['department_id'] == dept_id]
    updated_classes = [c for c in classes if c['department_id'] != dept_id]
    if len(classes) != len(updated_classes):
        write_csv('classes.csv', ['id', 'department_id', 'name'], updated_classes)
        
        # Cascade delete students of those classes
        students = get_students()
        updated_students = [s for s in students if s['class_id'] not in classes_to_delete]
        if len(students) != len(updated_students):
            write_csv('students.csv', ['id', 'roll_number', 'name', 'class_id'], updated_students)

# --- Classes ---
def get_classes():
    return read_csv('classes.csv')

def add_class(department_id, name):
    class_id = str(uuid.uuid4())
    append_csv('classes.csv', ['id', 'department_id', 'name'], {'id': class_id, 'department_id': department_id, 'name': name})
    return class_id

def get_class(class_id):
    for c in get_classes():
        if c['id'] == class_id:
            return c
    return None

def update_class(class_id, name, department_id):
    classes = get_classes()
    for c in classes:
        if c['id'] == class_id:
            c['name'] = name
            c['department_id'] = department_id
            break
    write_csv('classes.csv', ['id', 'department_id', 'name'], classes)

def delete_class(class_id):
    classes = get_classes()
    updated_classes = [c for c in classes if c['id'] != class_id]
    write_csv('classes.csv', ['id', 'department_id', 'name'], updated_classes)
    
    # Also delete associated students
    students = get_students()
    updated_students = [s for s in students if s['class_id'] != class_id]
    if len(students) != len(updated_students):
        write_csv('students.csv', ['id', 'roll_number', 'name', 'class_id'], updated_students)

# --- Students ---
def get_students():
    return read_csv('students.csv')

def add_student(roll_number, name, class_id):
    student_id = str(uuid.uuid4())
    append_csv('students.csv', ['id', 'roll_number', 'name', 'class_id'], {'id': student_id, 'roll_number': roll_number, 'name': name, 'class_id': class_id})
    return student_id

def get_students_by_class(class_id):
    return [s for s in get_students() if s['class_id'] == class_id]

def import_students_from_csv(file_stream, class_id):
    reader = csv.DictReader(file_stream)
    count = 0
    for row in reader:
        # Expecting at least 'roll_number' and 'name' columns in the uploaded CSV
        roll_number = row.get('roll_number', '').strip()
        name = row.get('name', '').strip()
        
        if roll_number and name:
            add_student(roll_number, name, class_id)
            count += 1
    return count

# --- Halls ---
def get_halls():
    return read_csv('halls.csv')

def add_hall(name, capacity):
    hall_id = str(uuid.uuid4())
    append_csv('halls.csv', ['id', 'name', 'capacity'], {'id': hall_id, 'name': name, 'capacity': capacity})
    return hall_id

def get_hall(hall_id):
    for h in get_halls():
        if h['id'] == hall_id:
            return h
    return None

def delete_hall(hall_id):
    halls = get_halls()
    updated_halls = [h for h in halls if h['id'] != hall_id]
    write_csv('halls.csv', ['id', 'name', 'capacity'], updated_halls)

def import_halls_from_csv(file_stream):
    reader = csv.DictReader(file_stream)
    count = 0
    for row in reader:
        name = row.get('name', '').strip()
        capacity = row.get('capacity', '').strip()
        
        if name and capacity and capacity.isdigit():
            add_hall(name, capacity)
            count += 1
    return count

# --- Exams ---
def get_exams():
    return read_csv('exams.csv')

def add_exam(class_id, subject, date, start_time, end_time):
    exam_id = str(uuid.uuid4())
    append_csv('exams.csv', ['id', 'class_id', 'subject', 'date', 'start_time', 'end_time'], 
               {'id': exam_id, 'class_id': class_id, 'subject': subject, 'date': date, 'start_time': start_time, 'end_time': end_time})
    return exam_id

def get_exam(exam_id):
    for e in get_exams():
        if e['id'] == exam_id:
            return e
    return None

def clean_old_exams():
    exams = get_exams()
    if not exams:
        return
        
    allotments = get_allotments()
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
        write_csv('exams.csv', ['id', 'class_id', 'subject', 'date', 'start_time', 'end_time'], valid_exams)
        valid_allotments = [a for a in allotments if a['exam_id'] not in deleted_exam_ids]
        write_csv('allotments.csv', ['id', 'exam_id', 'hall_id', 'student_id'], valid_allotments)

# --- Allotments ---
def get_allotments():
    return read_csv('allotments.csv')

def get_allotments_for_exam(exam_id):
    return [a for a in get_allotments() if a['exam_id'] == exam_id]

def is_hall_available(hall_id, date, start_time, end_time, current_exam_id=None):
    exams = get_exams()
    allotments = get_allotments()
    
    # Format times for comparison
    fmt = '%H:%M'
    try:
        req_start = datetime.strptime(start_time, fmt)
        req_end = datetime.strptime(end_time, fmt)
    except ValueError:
        return False # Invalid time format
    
    # Find all exams that are assigned to this hall
    for exam in exams:
        if exam['id'] == current_exam_id:
            continue # skip checking against itself if we were doing modifications
            
        if exam['date'] == date:
            # Check time overlap
            e_start = datetime.strptime(exam['start_time'], fmt)
            e_end = datetime.strptime(exam['end_time'], fmt)
            
            if (req_start < e_end and req_end > e_start):
                # Times overlap. Check if this hall is used in that exam.
                exam_allotments = [a for a in allotments if a['exam_id'] == exam['id']]
                if any(a['hall_id'] == hall_id for a in exam_allotments):
                    return False # Hall is in use
    return True

def perform_allotment(exam_id):
    """
    Core algorithm: Assign students of an exam to available halls.
    Returns (True, message) on success, (False, error_message) on failure.
    """
    exam = get_exam(exam_id)
    if not exam:
        return False, "Exam not found"
        
    students = get_students_by_class(exam['class_id'])
    if not students:
        return False, "No students found for this class"
        
    halls = get_halls()
    # Filter available halls for this date and time
    available_halls = [h for h in halls if is_hall_available(h['id'], exam['date'], exam['start_time'], exam['end_time'], exam_id)]
    
    # Sort halls by capacity (descending) to optimize filling
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
            
    # Save allotments
    for record in allotment_records:
        append_csv('allotments.csv', ['id', 'exam_id', 'hall_id', 'student_id'], record)
        
    return True, f"Successfully allocated {len(students)} students across {len(set(a['hall_id'] for a in allotment_records))} halls."

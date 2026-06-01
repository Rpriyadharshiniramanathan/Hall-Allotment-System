from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import data_manager

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_exam_hall_allotment'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def current_user():
    return session.get('username')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if data_manager.authenticate_user(username, password):
            session['logged_in'] = True
            session['username'] = username
            flash('Successfully logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and password cannot be empty.', 'danger')
        else:
            success, msg = data_manager.add_user(username, password)
            if success:
                flash('Registration successful! You can now login.', 'success')
                return redirect(url_for('login'))
            else:
                flash(msg, 'danger')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    user = current_user()
    data_manager.clean_old_exams(user)
    halls = data_manager.get_halls(user)
    exams = data_manager.get_exams(user)
    students = data_manager.get_students(user)

    total_capacity = sum(int(h['capacity']) for h in halls)

    return render_template('dashboard.html',
                           total_halls=len(halls),
                           total_exams=len(exams),
                           total_students=len(students),
                           total_capacity=total_capacity)

@app.route('/departments', methods=['GET', 'POST'])
@login_required
def departments():
    user = current_user()
    if request.method == 'POST':
        name = request.form['name']
        data_manager.add_department(user, name)
        flash('Department added successfully!', 'success')
        return redirect(url_for('departments'))

    depts = data_manager.get_departments(user)
    return render_template('departments.html', departments=depts)

@app.route('/delete_department/<dept_id>')
@login_required
def delete_department(dept_id):
    data_manager.delete_department(current_user(), dept_id)
    flash('Department, its classes, and students deleted successfully!', 'success')
    return redirect(url_for('departments'))

@app.route('/classes', methods=['GET', 'POST'])
@login_required
def classes():
    user = current_user()
    if request.method == 'POST':
        name = request.form['name']
        department_id = request.form['department_id']
        data_manager.add_class(user, department_id, name)
        flash('Class added successfully!', 'success')
        return redirect(url_for('classes'))

    cls = data_manager.get_classes(user)
    depts = data_manager.get_departments(user)

    dept_map = {d['id']: d['name'] for d in depts}
    for c in cls:
        c['department_name'] = dept_map.get(c['department_id'], 'Unknown')

    return render_template('classes.html', classes=cls, departments=depts)

@app.route('/edit_class/<class_id>', methods=['GET', 'POST'])
@login_required
def edit_class(class_id):
    user = current_user()
    cls = data_manager.get_class(user, class_id)
    if not cls:
        flash('Class not found', 'danger')
        return redirect(url_for('classes'))

    if request.method == 'POST':
        name = request.form['name']
        department_id = request.form['department_id']
        data_manager.update_class(user, class_id, name, department_id)
        flash('Class updated successfully!', 'success')
        return redirect(url_for('classes'))

    depts = data_manager.get_departments(user)
    return render_template('edit_class.html', current_class=cls, departments=depts)

@app.route('/delete_class/<class_id>')
@login_required
def delete_class(class_id):
    data_manager.delete_class(current_user(), class_id)
    flash('Class and its students deleted successfully!', 'success')
    return redirect(url_for('classes'))

@app.route('/students', methods=['GET', 'POST'])
@login_required
def students():
    user = current_user()
    if request.method == 'POST':
        if 'csv_file' in request.files:
            file = request.files['csv_file']
            class_id = request.form['csv_class_id']
            if file.filename == '':
                flash('No selected file', 'danger')
            elif not file.filename.endswith('.csv'):
                flash('Please upload a valid CSV file', 'danger')
            else:
                import io
                file_stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                count = data_manager.import_students_from_csv(user, file_stream, class_id)
                flash(f'Successfully imported {count} students!', 'success')
        else:
            name = request.form['name']
            roll_number = request.form['roll_number']
            class_id = request.form['class_id']
            data_manager.add_student(user, roll_number, name, class_id)
            flash('Student added successfully!', 'success')

        return redirect(url_for('students'))

    studs = data_manager.get_students(user)
    cls = data_manager.get_classes(user)

    cls_map = {c['id']: c['name'] for c in cls}
    for s in studs:
        s['class_name'] = cls_map.get(s['class_id'], 'Unknown')

    return render_template('students.html', students=studs, classes=cls)

@app.route('/halls', methods=['GET', 'POST'])
@login_required
def halls():
    user = current_user()
    if request.method == 'POST':
        if 'csv_file' in request.files:
            file = request.files['csv_file']
            if file.filename == '':
                flash('No selected file', 'danger')
            elif not file.filename.endswith('.csv'):
                flash('Please upload a valid CSV file', 'danger')
            else:
                import io
                file_stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                count = data_manager.import_halls_from_csv(user, file_stream)
                flash(f'Successfully imported {count} halls!', 'success')
        else:
            name = request.form['name']
            capacity = request.form['capacity']
            data_manager.add_hall(user, name, capacity)
            flash('Hall added successfully!', 'success')
        return redirect(url_for('halls'))

    h = data_manager.get_halls(user)
    return render_template('halls.html', halls=h)

@app.route('/delete_hall/<hall_id>')
@login_required
def delete_hall(hall_id):
    data_manager.delete_hall(current_user(), hall_id)
    flash('Hall deleted successfully!', 'success')
    return redirect(url_for('halls'))

@app.route('/exams', methods=['GET', 'POST'])
@login_required
def exams():
    user = current_user()
    data_manager.clean_old_exams(user)
    if request.method == 'POST':
        class_id = request.form['class_id']
        subject = request.form['subject']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        data_manager.add_exam(user, class_id, subject, date, start_time, end_time)
        flash('Exam scheduled successfully!', 'success')
        return redirect(url_for('exams'))

    exs = data_manager.get_exams(user)
    cls = data_manager.get_classes(user)
    allots = data_manager.get_allotments(user)

    cls_map = {c['id']: c['name'] for c in cls}

    allot_map = {}
    for a in allots:
        allot_map[a['exam_id']] = True

    for e in exs:
        e['class_name'] = cls_map.get(e['class_id'], 'Unknown')
        e['is_allotted'] = e['id'] in allot_map

    return render_template('exams.html', exams=exs, classes=cls)

@app.route('/allot/<exam_id>')
@login_required
def do_allotment(exam_id):
    success, message = data_manager.perform_allotment(current_user(), exam_id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    return redirect(url_for('exams'))

@app.route('/allotment/<exam_id>')
@login_required
def view_allotment(exam_id):
    user = current_user()
    exam = data_manager.get_exam(user, exam_id)
    if not exam:
        flash('Exam not found!', 'danger')
        return redirect(url_for('exams'))

    cls = data_manager.get_class(user, exam['class_id'])
    exam['class_name'] = cls['name'] if cls else 'Unknown'

    allots = data_manager.get_allotments_for_exam(user, exam_id)
    halls = data_manager.get_halls(user)
    students = data_manager.get_students(user)

    hall_map = {h['id']: h['name'] for h in halls}
    student_map = {s['id']: s for s in students}

    allocations_by_hall = {}
    for a in allots:
        hall_id = a['hall_id']
        if hall_id not in allocations_by_hall:
            allocations_by_hall[hall_id] = {
                'hall_name': hall_map.get(hall_id, 'Unknown Hall'),
                'students': []
            }
        student = student_map.get(a['student_id'])
        if student:
            allocations_by_hall[hall_id]['students'].append(student)

    return render_template('allotment_view.html', exam=exam, allocations=allocations_by_hall)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

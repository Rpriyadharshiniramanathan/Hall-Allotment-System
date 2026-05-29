import openpyxl
import os
import data_manager

def import_excel_data():
    filepath = os.path.join(data_manager.DATA_DIR, 'Stu.details.xlsx')
    if not os.path.exists(filepath):
        print("Excel file not found!")
        return

    print("Loading workbook...")
    wb = openpyxl.load_workbook(filepath)
    sheet = wb.active
    
    # Get existing departments and classes to avoid duplicates
    depts = {d['name']: d['id'] for d in data_manager.get_departments()}
    classes = {c['name']: c['id'] for c in data_manager.get_classes()}
    
    rows = list(sheet.iter_rows(values_only=True))
    headers = rows[0]
    
    # Try to find indices
    try:
        name_idx = headers.index('Student Name')
        dept_idx = headers.index('Department')
        degree_idx = headers.index('Degree')
    except ValueError as e:
        print("Required headers not found:", e)
        return

    print("Importing students...")
    student_count = 0
    for idx, row in enumerate(rows[1:], start=1):
        if not row[name_idx]:
            continue
            
        name = str(row[name_idx]).strip()
        dept_name = str(row[dept_idx]).strip()
        degree = str(row[degree_idx]).strip()
        
        # 1. Handle Department
        if dept_name not in depts:
            dept_id = data_manager.add_department(dept_name)
            depts[dept_name] = dept_id
        else:
            dept_id = depts[dept_name]
            
        # 2. Handle Class
        class_name = f"{degree} - {dept_name}"
        if class_name not in classes:
            class_id = data_manager.add_class(dept_id, class_name)
            classes[class_name] = class_id
        else:
            class_id = classes[class_name]
            
        # 3. Handle Student (generate mock roll number)
        roll_number = f"R{idx:04d}"
        
        data_manager.add_student(roll_number, name, class_id)
        student_count += 1

    print(f"Successfully imported {student_count} students!")

if __name__ == '__main__':
    import_excel_data()

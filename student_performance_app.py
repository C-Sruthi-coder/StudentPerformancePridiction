import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# Oracle connection
from database import get_connection


# ============================================================
# CONSTANTS
# ============================================================

SUBJECTS = ["Python", "Java", "DBMS", "OS", "DMS"]
SECTIONS = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]


# ============================================================
# ORACLE DATABASE FUNCTIONS
# ============================================================

def get_sections():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT section_name
        FROM sections
        ORDER BY section_name
    """)

    sections = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return sections


def get_students(section_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.student_id,
            s.roll_no,
            s.student_name
        FROM students s
        JOIN sections sec
            ON s.section_id = sec.section_id
        WHERE sec.section_name = :section_name
        ORDER BY s.roll_no
    """, section_name=section_name)

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return students


def get_student_data(roll_no):
    """
    Get one student's complete marks and attendance
    directly from Oracle.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.roll_no,
            s.student_name,
            sec.section_name,

            MAX(
                CASE
                    WHEN sub.subject_name = 'Python'
                    THEN m.marks
                END
            ) AS python_marks,

            MAX(
                CASE
                    WHEN sub.subject_name = 'Java'
                    THEN m.marks
                END
            ) AS java_marks,

            MAX(
                CASE
                    WHEN sub.subject_name = 'DBMS'
                    THEN m.marks
                END
            ) AS dbms_marks,

            MAX(
                CASE
                    WHEN sub.subject_name = 'OS'
                    THEN m.marks
                END
            ) AS os_marks,

            MAX(
                CASE
                    WHEN sub.subject_name = 'DMS'
                    THEN m.marks
                END
            ) AS dms_marks,

            MAX(
                CASE
                    WHEN sub.subject_name = 'Python'
                    THEN a.attendance_percentage
                END
            ) AS python_att,

            MAX(
                CASE
                    WHEN sub.subject_name = 'Java'
                    THEN a.attendance_percentage
                END
            ) AS java_att,

            MAX(
                CASE
                    WHEN sub.subject_name = 'DBMS'
                    THEN a.attendance_percentage
                END
            ) AS dbms_att,

            MAX(
                CASE
                    WHEN sub.subject_name = 'OS'
                    THEN a.attendance_percentage
                END
            ) AS os_att,

            MAX(
                CASE
                    WHEN sub.subject_name = 'DMS'
                    THEN a.attendance_percentage
                END
            ) AS dms_att

        FROM students s

        JOIN sections sec
            ON s.section_id = sec.section_id

        CROSS JOIN subjects sub

        LEFT JOIN marks m
            ON m.student_id = s.student_id
            AND m.subject_id = sub.subject_id

        LEFT JOIN attendance a
            ON a.student_id = s.student_id
            AND a.subject_id = sub.subject_id

        WHERE s.roll_no = :roll_no

        GROUP BY
            s.roll_no,
            s.student_name,
            sec.section_name
    """, roll_no=roll_no)

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        return None

    columns = [
        "RollNo",
        "Name",
        "Section",

        "Python",
        "Java",
        "DBMS",
        "OS",
        "DMS",

        "Python_Att",
        "Java_Att",
        "DBMS_Att",
        "OS_Att",
        "DMS_Att"
    ]

    return dict(zip(columns, row))


def get_section_records(section_name):
    """
    Get all students in a section with their marks
    and attendance from Oracle.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.roll_no,
            s.student_name,

            MAX(
                CASE
                    WHEN sub.subject_name = 'Python'
                    THEN m.marks
                END
            ) AS python_marks,

            MAX(
                CASE
                    WHEN sub.subject_name = 'Java'
                    THEN m.marks
                END
            ) AS java_marks,

            MAX(
                CASE
                    WHEN sub.subject_name = 'DBMS'
                    THEN m.marks
                END
            ) AS dbms_marks,

            MAX(
                CASE
                    WHEN sub.subject_name = 'OS'
                    THEN m.marks
                END
            ) AS os_marks,

            MAX(
                CASE
                    WHEN sub.subject_name = 'DMS'
                    THEN m.marks
                END
            ) AS dms_marks,

            MAX(
                CASE
                    WHEN sub.subject_name = 'Python'
                    THEN a.attendance_percentage
                END
            ) AS python_att,

            MAX(
                CASE
                    WHEN sub.subject_name = 'Java'
                    THEN a.attendance_percentage
                END
            ) AS java_att,

            MAX(
                CASE
                    WHEN sub.subject_name = 'DBMS'
                    THEN a.attendance_percentage
                END
            ) AS dbms_att,

            MAX(
                CASE
                    WHEN sub.subject_name = 'OS'
                    THEN a.attendance_percentage
                END
            ) AS os_att,

            MAX(
                CASE
                    WHEN sub.subject_name = 'DMS'
                    THEN a.attendance_percentage
                END
            ) AS dms_att

        FROM students s

        JOIN sections sec
            ON s.section_id = sec.section_id

        CROSS JOIN subjects sub

        LEFT JOIN marks m
            ON m.student_id = s.student_id
            AND m.subject_id = sub.subject_id

        LEFT JOIN attendance a
            ON a.student_id = s.student_id
            AND a.subject_id = sub.subject_id

        WHERE sec.section_name = :section_name

        GROUP BY
            s.roll_no,
            s.student_name

        ORDER BY s.roll_no
    """, section_name=section_name)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


# ============================================================
# PERFORMANCE CATEGORY
# ============================================================

def get_performance(score):

    if score >= 80:
        return "Excellent"

    elif score >= 70:
        return "Good"

    elif score >= 60:
        return "Average"

    else:
        return "Needs Improvement"


# ============================================================
# GET SELECTED STUDENT
# ============================================================

def get_student():

    roll_no = roll_var.get().strip()

    if roll_no == "":
        messagebox.showwarning(
            "Selection Required",
            "Please select a student."
        )
        return None

    try:

        student = get_student_data(roll_no)

    except Exception as e:

        messagebox.showerror(
            "Oracle Error",
            f"Could not read student data.\n\n{e}"
        )

        return None

    if student is None:

        messagebox.showerror(
            "Error",
            "Student not found in Oracle."
        )

        return None

    return student


# ============================================================
# CHECK COMPLETE DATA
# ============================================================

def get_complete_values(student):

    values = []

    # Subject marks

    for subject in SUBJECTS:

        value = student[subject]

        if value is None:
            return None

        values.append(float(value))

    # Attendance

    for subject in SUBJECTS:

        value = student[subject + "_Att"]

        if value is None:
            return None

        values.append(float(value))

    return np.array(values, dtype=float)


# ============================================================
# LOAD STUDENTS
# ============================================================

def load_students(event=None):

    section = section_var.get()

    if section == "":
        return

    try:

        students = get_students(section)

    except Exception as e:

        messagebox.showerror(
            "Oracle Error",
            f"Could not load students.\n\n{e}"
        )

        return

    global student_map

    student_map = {}

    student_display = []

    for student_id, roll_no, name in students:

        display = f"{roll_no} - {name}"

        student_display.append(display)

        student_map[display] = str(roll_no)

    student_dropdown["values"] = student_display

    if student_display:

        student_dropdown.current(0)

        roll_var.set(
            student_map[student_display[0]]
        )

    else:

        student_dropdown.set("")

        roll_var.set("")

    output.delete("1.0", tk.END)

    output.insert(
        tk.END,
        f"Section {section} loaded.\n\n"
        f"Students in section: {len(students)}\n\n"
        "Select a student and choose a performance option."
    )


# ============================================================
# STUDENT SELECTION
# ============================================================

def student_selected(event=None):

    selected = student_display_var.get()

    if selected in student_map:

        roll_var.set(
            student_map[selected]
        )


# ============================================================
# REFRESH
# ============================================================

def refresh_students():

    load_students()


# ============================================================
# STUDIES PERFORMANCE
# ============================================================

def show_studies():

    student = get_student()

    if student is None:
        return

    marks = [
        student[subject]
        for subject in SUBJECTS
    ]

    if any(value is None for value in marks):

        messagebox.showwarning(
            "Incomplete Data",
            "Faculty must enter all five subject marks "
            "before showing Studies Performance."
        )

        return

    marks = np.array(
        marks,
        dtype=float
    )

    average = np.mean(marks)

    subjects = dict(
        zip(SUBJECTS, marks)
    )

    strongest = max(
        subjects,
        key=subjects.get
    )

    weakest = min(
        subjects,
        key=subjects.get
    )

    output.delete(
        "1.0",
        tk.END
    )

    output.insert(
        tk.END,
        "STUDIES PERFORMANCE\n"
    )

    output.insert(
        tk.END,
        "============================\n\n"
    )

    output.insert(
        tk.END,
        f"Student Name : {student['Name']}\n"
    )

    output.insert(
        tk.END,
        f"Roll Number  : {student['RollNo']}\n"
    )

    output.insert(
        tk.END,
        f"Section      : {student['Section']}\n\n"
    )

    for subject in SUBJECTS:

        output.insert(
            tk.END,
            f"{subject:<8}: "
            f"{float(student[subject]):.2f}\n"
        )

    output.insert(
        tk.END,
        f"\nStudy Average     : {average:.2f}\n"
    )

    output.insert(
        tk.END,
        f"Strongest Subject : {strongest}\n"
    )

    output.insert(
        tk.END,
        f"Weakest Subject   : {weakest}\n"
    )

    output.insert(
        tk.END,
        f"Performance       : "
        f"{get_performance(average)}\n"
    )


# ============================================================
# ATTENDANCE PERFORMANCE
# ============================================================

def show_attendance():

    student = get_student()

    if student is None:
        return

    attendance = [
        student[subject + "_Att"]
        for subject in SUBJECTS
    ]

    if any(value is None for value in attendance):

        messagebox.showwarning(
            "Incomplete Data",
            "Faculty must enter attendance for all five "
            "subjects before showing Attendance Performance."
        )

        return

    attendance = np.array(
        attendance,
        dtype=float
    )

    average = np.mean(attendance)

    attendance_data = dict(
        zip(SUBJECTS, attendance)
    )

    lowest = min(
        attendance_data,
        key=attendance_data.get
    )

    output.delete(
        "1.0",
        tk.END
    )

    output.insert(
        tk.END,
        "ATTENDANCE PERFORMANCE\n"
    )

    output.insert(
        tk.END,
        "============================\n\n"
    )

    output.insert(
        tk.END,
        f"Student Name : {student['Name']}\n"
    )

    output.insert(
        tk.END,
        f"Roll Number  : {student['RollNo']}\n"
    )

    output.insert(
        tk.END,
        f"Section      : {student['Section']}\n\n"
    )

    for subject in SUBJECTS:

        output.insert(
            tk.END,
            f"{subject:<8}: "
            f"{float(student[subject + '_Att']):.2f}%\n"
        )

    output.insert(
        tk.END,
        f"\nAttendance Average : {average:.2f}%\n"
    )

    output.insert(
        tk.END,
        f"Lowest Attendance  : {lowest}\n"
    )

    output.insert(
        tk.END,
        f"Category           : "
        f"{get_performance(average)}\n"
    )


# ============================================================
# OVERALL PERFORMANCE
# ============================================================

def show_overall():

    student = get_student()

    if student is None:
        return

    values = get_complete_values(student)

    if values is None:

        messagebox.showwarning(
            "Incomplete Data",
            "All subject marks and attendance must be "
            "entered before calculating Overall Performance."
        )

        return

    study_average = np.mean(
        values[:5]
    )

    attendance_average = np.mean(
        values[5:]
    )

    overall_score = (
        study_average * 0.70
        + attendance_average * 0.30
    )

    output.delete(
        "1.0",
        tk.END
    )

    output.insert(
        tk.END,
        "OVERALL PERFORMANCE\n"
    )

    output.insert(
        tk.END,
        "============================\n\n"
    )

    output.insert(
        tk.END,
        f"Student Name : {student['Name']}\n"
    )

    output.insert(
        tk.END,
        f"Roll Number  : {student['RollNo']}\n"
    )

    output.insert(
        tk.END,
        f"Section      : {student['Section']}\n\n"
    )

    output.insert(
        tk.END,
        f"Study Average      : "
        f"{study_average:.2f}\n"
    )

    output.insert(
        tk.END,
        f"Attendance Average : "
        f"{attendance_average:.2f}%\n\n"
    )

    output.insert(
        tk.END,
        f"Overall Score : "
        f"{overall_score:.2f}/100\n"
    )

    output.insert(
        tk.END,
        f"Performance  : "
        f"{get_performance(overall_score)}\n"
    )


# ============================================================
# PERFORMANCE PREDICTION
# ============================================================

def predict_performance():

    student = get_student()

    if student is None:
        return

    selected_values = get_complete_values(
        student
    )

    if selected_values is None:

        messagebox.showwarning(
            "Incomplete Data",
            "All subject marks and attendance must "
            "be entered before prediction."
        )

        return

    section = student["Section"]

    rows = get_section_records(
        section
    )

    X = []
    y = []

    for row in rows:

        values = list(
            row[2:]
        )

        if any(
            value is None
            for value in values
        ):
            continue

        values = np.array(
            values,
            dtype=float
        )

        study_average = np.mean(
            values[:5]
        )

        attendance_average = np.mean(
            values[5:]
        )

        target = (
            study_average * 0.70
            + attendance_average * 0.30
        )

        X.append(values)
        y.append(target)

    if len(X) < 2:

        messagebox.showwarning(
            "Not Enough Data",
            "At least two students with complete "
            "marks and attendance are required "
            "for the prediction model."
        )

        return

    X = np.array(
        X,
        dtype=float
    )

    y = np.array(
        y,
        dtype=float
    )

    X_bias = np.column_stack(
        (
            np.ones(len(X)),
            X
        )
    )

    coefficients = np.linalg.lstsq(
        X_bias,
        y,
        rcond=None
    )[0]

    student_input = np.insert(
        selected_values,
        0,
        1
    )

    predicted_score = float(
        student_input @ coefficients
    )

    predicted_score = max(
        0,
        min(
            100,
            predicted_score
        )
    )

    train_predictions = (
        X_bias @ coefficients
    )

    mae = float(
        np.mean(
            np.abs(
                y - train_predictions
            )
        )
    )

    output.delete(
        "1.0",
        tk.END
    )

    output.insert(
        tk.END,
        "PERFORMANCE PREDICTION\n"
    )

    output.insert(
        tk.END,
        "============================\n\n"
    )

    output.insert(
        tk.END,
        f"Student Name : {student['Name']}\n"
    )

    output.insert(
        tk.END,
        f"Roll Number  : {student['RollNo']}\n"
    )

    output.insert(
        tk.END,
        f"Section      : {student['Section']}\n\n"
    )

    output.insert(
        tk.END,
        f"Predicted Final Marks : "
        f"{predicted_score:.2f}/100\n"
    )

    output.insert(
        tk.END,
        f"Performance Category  : "
        f"{get_performance(predicted_score)}\n\n"
    )

    output.insert(
        tk.END,
        "MACHINE LEARNING MODEL\n"
    )

    output.insert(
        tk.END,
        "----------------------------\n"
    )

    output.insert(
        tk.END,
        "Algorithm : Multiple Linear Regression\n"
    )

    output.insert(
        tk.END,
        "Features  : Subject Marks + Attendance\n"
    )

    output.insert(
        tk.END,
        f"Training Students : {len(X)}\n"
    )

    output.insert(
        tk.END,
        f"Model MAE : {mae:.2f} marks\n\n"
    )

    output.insert(
        tk.END,
        "Note: This is a project demo prediction "
        "based on Oracle-entered data."
    )


# ============================================================
# CLASS COMPARISON
# ============================================================

def class_comparison():

    student = get_student()

    if student is None:
        return

    section = student["Section"]

    rows = get_section_records(
        section
    )

    complete_records = []

    for row in rows:

        values = list(
            row[2:]
        )

        if any(
            value is None
            for value in values
        ):
            continue

        values = np.array(
            values,
            dtype=float
        )

        study_average = np.mean(
            values[:5]
        )

        attendance_average = np.mean(
            values[5:]
        )

        overall = (
            study_average * 0.70
            + attendance_average * 0.30
        )

        complete_records.append(
            (
                str(row[0]),
                str(row[1]),
                overall
            )
        )

    if not complete_records:

        messagebox.showwarning(
            "Incomplete Data",
            "No students in this section have "
            "complete marks and attendance data."
        )

        return

    selected_score = None

    for roll, name, score in complete_records:

        if roll == str(student["RollNo"]):

            selected_score = score

            break

    if selected_score is None:

        messagebox.showwarning(
            "Incomplete Data",
            "The selected student's marks and "
            "attendance are not complete."
        )

        return

    scores = [
        record[2]
        for record in complete_records
    ]

    class_average = float(
        np.mean(scores)
    )

    highest = float(
        np.max(scores)
    )

    lowest = float(
        np.min(scores)
    )

    difference = (
        selected_score
        - class_average
    )

    if difference > 0:

        comparison = "Above Class Average"

    elif difference < 0:

        comparison = "Below Class Average"

    else:

        comparison = "Equal to Class Average"

    output.delete(
        "1.0",
        tk.END
    )

    output.insert(
        tk.END,
        "CLASS COMPARISON\n"
    )

    output.insert(
        tk.END,
        "============================\n\n"
    )

    output.insert(
        tk.END,
        f"Student Name : {student['Name']}\n"
    )

    output.insert(
        tk.END,
        f"Roll Number  : {student['RollNo']}\n"
    )

    output.insert(
        tk.END,
        f"Section      : {section}\n\n"
    )

    output.insert(
        tk.END,
        f"Student Overall Score : "
        f"{selected_score:.2f}/100\n"
    )

    output.insert(
        tk.END,
        f"Class Average         : "
        f"{class_average:.2f}/100\n"
    )

    output.insert(
        tk.END,
        f"Difference            : "
        f"{difference:+.2f} marks\n\n"
    )

    output.insert(
        tk.END,
        f"Comparison : "
        f"{comparison}\n\n"
    )

    output.insert(
        tk.END,
        "CLASS INFORMATION\n"
    )

    output.insert(
        tk.END,
        "----------------------------\n"
    )

    output.insert(
        tk.END,
        f"Students with complete data : "
        f"{len(complete_records)}\n"
    )

    output.insert(
        tk.END,
        f"Highest Score : {highest:.2f}\n"
    )

    output.insert(
        tk.END,
        f"Lowest Score  : {lowest:.2f}\n"
    )


# ============================================================
# EXIT
# ============================================================

def exit_application():

    root.destroy()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Student Performance Prediction System"
)

root.geometry(
    "900x760"
)

root.resizable(
    False,
    False
)


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    root,
    text="STUDENT PERFORMANCE PREDICTION SYSTEM",
    font=("Arial", 20, "bold")
)

title_label.pack(
    pady=(18, 5)
)


subtitle_label = tk.Label(
    root,
    text="Python Programming Lab | Oracle Database",
    font=("Arial", 11)
)

subtitle_label.pack(
    pady=(0, 12)
)


# ============================================================
# SECTION + STUDENT SELECTION
# ============================================================

selection_frame = tk.Frame(
    root
)

selection_frame.pack(
    pady=5
)


tk.Label(
    selection_frame,
    text="Section:",
    font=("Arial", 12)
).grid(
    row=0,
    column=0,
    padx=8,
    pady=5
)


section_var = tk.StringVar()


section_dropdown = ttk.Combobox(
    selection_frame,
    textvariable=section_var,
    values=SECTIONS,
    state="readonly",
    width=12
)

section_dropdown.grid(
    row=0,
    column=1,
    padx=8,
    pady=5
)

section_dropdown.bind(
    "<<ComboboxSelected>>",
    load_students
)


tk.Label(
    selection_frame,
    text="Student:",
    font=("Arial", 12)
).grid(
    row=0,
    column=2,
    padx=8,
    pady=5
)


student_display_var = tk.StringVar()


student_dropdown = ttk.Combobox(
    selection_frame,
    textvariable=student_display_var,
    state="readonly",
    width=32
)

student_dropdown.grid(
    row=0,
    column=3,
    padx=8,
    pady=5
)

student_dropdown.bind(
    "<<ComboboxSelected>>",
    student_selected
)


refresh_button = tk.Button(
    selection_frame,
    text="Refresh Students",
    command=refresh_students,
    width=16
)

refresh_button.grid(
    row=0,
    column=4,
    padx=8,
    pady=5
)


# ============================================================
# INTERNAL VARIABLES
# ============================================================

roll_var = tk.StringVar()

student_map = {}


# ============================================================
# OUTPUT AREA
# ============================================================

output = tk.Text(
    root,
    height=23,
    width=95,
    font=("Consolas", 11)
)

output.pack(
    pady=15
)


# ============================================================
# BUTTONS
# ============================================================

button_frame = tk.Frame(
    root
)

button_frame.pack(
    pady=5
)


tk.Button(
    button_frame,
    text="Studies Performance",
    command=show_studies,
    width=21
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)


tk.Button(
    button_frame,
    text="Attendance Performance",
    command=show_attendance,
    width=21
).grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


tk.Button(
    button_frame,
    text="Overall Performance",
    command=show_overall,
    width=21
).grid(
    row=0,
    column=2,
    padx=5,
    pady=5
)


tk.Button(
    button_frame,
    text="Predict Performance",
    command=predict_performance,
    width=21
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)


tk.Button(
    button_frame,
    text="Class Comparison",
    command=class_comparison,
    width=21
).grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


tk.Button(
    button_frame,
    text="Exit",
    command=exit_application,
    width=21
).grid(
    row=1,
    column=2,
    padx=5,
    pady=5
)


# ============================================================
# START APPLICATION
# ============================================================

try:

    available_sections = get_sections()

    if available_sections:

        section_dropdown["values"] = (
            available_sections
        )

        section_dropdown.current(0)

        section_var.set(
            available_sections[0]
        )

        load_students()

except Exception as e:

    messagebox.showerror(
        "Oracle Connection Error",
        "Could not load sections from Oracle.\n\n"
        f"{e}"
    )


root.mainloop()
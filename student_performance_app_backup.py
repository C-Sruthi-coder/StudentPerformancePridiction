import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np


# ============================================================
# LOAD CSV FILE
# ============================================================

try:
    df = pd.read_csv("student_performance.csv")

except FileNotFoundError:
    print("ERROR: student_performance.csv not found.")
    print("Make sure both files are in the same folder:")
    print("1. student_performance_app.py")
    print("2. student_performance.csv")
    exit()


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "RollNo",
    "Name",
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

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:

    print("ERROR: Missing columns in CSV:")
    print(missing_columns)
    exit()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("Student Performance Prediction System")

root.geometry("1100x750")

root.configure(bg="#f2f4f7")


# ============================================================
# TITLE
# ============================================================

title = tk.Label(
    root,
    text="STUDENT PERFORMANCE PREDICTION SYSTEM",
    font=("Arial", 24, "bold"),
    bg="#f2f4f7"
)

title.pack(pady=20)


# ============================================================
# STUDENT SELECTION FRAME
# ============================================================

selection_frame = tk.Frame(
    root,
    bg="#f2f4f7"
)

selection_frame.pack(pady=10)


roll_label = tk.Label(
    selection_frame,
    text="Select Roll Number:",
    font=("Arial", 13, "bold"),
    bg="#f2f4f7"
)

roll_label.grid(
    row=0,
    column=0,
    padx=10
)


# Convert RollNo to string

roll_numbers = df["RollNo"].astype(str).tolist()


roll_box = ttk.Combobox(
    selection_frame,
    values=roll_numbers,
    width=25,
    state="readonly",
    font=("Arial", 12)
)

roll_box.grid(
    row=0,
    column=1,
    padx=10
)


# ============================================================
# STUDENT NAME
# ============================================================

student_name_label = tk.Label(
    root,
    text="Student Name: -",
    font=("Arial", 17, "bold"),
    bg="#f2f4f7"
)

student_name_label.pack(pady=10)


# ============================================================
# OUTPUT AREA
# ============================================================

output_frame = tk.Frame(
    root,
    bg="white",
    bd=2,
    relief="groove"
)

output_frame.pack(
    padx=40,
    pady=15,
    fill="both",
    expand=True
)


output_text = tk.Text(
    output_frame,
    font=("Consolas", 13),
    bg="white",
    fg="black",
    wrap="word"
)

output_text.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# ============================================================
# FUNCTION: GET SELECTED STUDENT
# ============================================================

def get_student():

    roll = roll_box.get()

    if roll == "":

        messagebox.showwarning(
            "Selection Required",
            "Please select a roll number first."
        )

        return None

    student = df[
        df["RollNo"].astype(str) == roll
    ]

    if student.empty:

        messagebox.showerror(
            "Error",
            "Student not found."
        )

        return None

    return student.iloc[0]


# ============================================================
# FUNCTION: PERFORMANCE CATEGORY
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
# STUDIES PERFORMANCE
# ============================================================

def show_studies():

    student = get_student()

    if student is None:
        return

    student_name_label.config(
        text=f"Student Name: {student['Name']}"
    )

    subjects = {

        "Python": float(student["Python"]),

        "Java": float(student["Java"]),

        "DBMS": float(student["DBMS"]),

        "OS": float(student["OS"]),

        "DMS": float(student["DMS"])
    }


    marks = list(subjects.values())

    average = np.mean(marks)

    strongest = max(
        subjects,
        key=subjects.get
    )

    weakest = min(
        subjects,
        key=subjects.get
    )

    performance = get_performance(
        average
    )


    output_text.delete(
        "1.0",
        tk.END
    )


    output_text.insert(
        tk.END,
        "================================================\n"
    )

    output_text.insert(
        tk.END,
        "             STUDIES PERFORMANCE\n"
    )

    output_text.insert(
        tk.END,
        "================================================\n\n"
    )


    output_text.insert(
        tk.END,
        f"Roll Number : {student['RollNo']}\n"
    )

    output_text.insert(
        tk.END,
        f"Student     : {student['Name']}\n\n"
    )


    output_text.insert(
        tk.END,
        "SUBJECT-WISE MARKS\n"
    )

    output_text.insert(
        tk.END,
        "------------------------------------------------\n"
    )


    for subject, mark in subjects.items():

        output_text.insert(
            tk.END,
            f"{subject:<15} : {mark:.2f}%\n"
        )


    output_text.insert(
        tk.END,
        "\n------------------------------------------------\n"
    )

    output_text.insert(
        tk.END,
        f"Average Marks       : {average:.2f}%\n"
    )

    output_text.insert(
        tk.END,
        f"Strongest Subject   : {strongest}\n"
    )

    output_text.insert(
        tk.END,
        f"Weakest Subject     : {weakest}\n"
    )

    output_text.insert(
        tk.END,
        f"Studies Performance : {performance}\n"
    )



# ============================================================
# ATTENDANCE PERFORMANCE
# ============================================================

def show_attendance():

    student = get_student()

    if student is None:
        return

    student_name_label.config(
        text=f"Student Name: {student['Name']}"
    )


    attendance = {

        "Python": float(student["Python_Att"]),

        "Java": float(student["Java_Att"]),

        "DBMS": float(student["DBMS_Att"]),

        "OS": float(student["OS_Att"]),

        "DMS": float(student["DMS_Att"])
    }


    values = list(
        attendance.values()
    )

    average = np.mean(values)

    lowest = min(
        attendance,
        key=attendance.get
    )

    performance = get_performance(
        average
    )


    output_text.delete(
        "1.0",
        tk.END
    )


    output_text.insert(
        tk.END,
        "================================================\n"
    )

    output_text.insert(
        tk.END,
        "           ATTENDANCE PERFORMANCE\n"
    )

    output_text.insert(
        tk.END,
        "================================================\n\n"
    )


    output_text.insert(
        tk.END,
        f"Roll Number : {student['RollNo']}\n"
    )

    output_text.insert(
        tk.END,
        f"Student     : {student['Name']}\n\n"
    )


    output_text.insert(
        tk.END,
        "SUBJECT-WISE ATTENDANCE\n"
    )

    output_text.insert(
        tk.END,
        "------------------------------------------------\n"
    )


    for subject, att in attendance.items():

        output_text.insert(
            tk.END,
            f"{subject:<15} : {att:.2f}%\n"
        )


    output_text.insert(
        tk.END,
        "\n------------------------------------------------\n"
    )

    output_text.insert(
        tk.END,
        f"Average Attendance      : {average:.2f}%\n"
    )

    output_text.insert(
        tk.END,
        f"Lowest Attendance       : {lowest}\n"
    )

    output_text.insert(
        tk.END,
        f"Attendance Performance  : {performance}\n"
    )



# ============================================================
# OVERALL PERFORMANCE
# ============================================================

def show_overall():

    student = get_student()

    if student is None:
        return

    student_name_label.config(
        text=f"Student Name: {student['Name']}"
    )


    # -------------------------
    # STUDIES
    # -------------------------

    study_marks = [

        float(student["Python"]),

        float(student["Java"]),

        float(student["DBMS"]),

        float(student["OS"]),

        float(student["DMS"])
    ]


    study_average = np.mean(
        study_marks
    )


    # -------------------------
    # ATTENDANCE
    # -------------------------

    attendance_values = [

        float(student["Python_Att"]),

        float(student["Java_Att"]),

        float(student["DBMS_Att"]),

        float(student["OS_Att"]),

        float(student["DMS_Att"])
    ]


    attendance_average = np.mean(
        attendance_values
    )


    # -------------------------
    # WEIGHTED SCORE
    # -------------------------

    overall_score = (

        study_average * 0.70

        +

        attendance_average * 0.30
    )


    performance = get_performance(
        overall_score
    )


    output_text.delete(
        "1.0",
        tk.END
    )


    output_text.insert(
        tk.END,
        "================================================\n"
    )

    output_text.insert(
        tk.END,
        "             OVERALL PERFORMANCE\n"
    )

    output_text.insert(
        tk.END,
        "================================================\n\n"
    )


    output_text.insert(
        tk.END,
        f"Roll Number          : {student['RollNo']}\n"
    )

    output_text.insert(
        tk.END,
        f"Student              : {student['Name']}\n\n"
    )


    output_text.insert(
        tk.END,
        f"Studies Average      : {study_average:.2f}%\n"
    )

    output_text.insert(
        tk.END,
        f"Attendance Average   : {attendance_average:.2f}%\n\n"
    )


    output_text.insert(
        tk.END,
        "Studies Weight       : 70%\n"
    )

    output_text.insert(
        tk.END,
        "Attendance Weight    : 30%\n\n"
    )


    output_text.insert(
        tk.END,
        "------------------------------------------------\n"
    )


    output_text.insert(
        tk.END,
        f"Overall Score        : {overall_score:.2f}%\n"
    )

    output_text.insert(
        tk.END,
        f"Overall Performance  : {performance}\n"
    )


    output_text.insert(
        tk.END,
        "------------------------------------------------\n\n"
    )


    # -------------------------
    # ANALYSIS
    # -------------------------

    output_text.insert(
        tk.END,
        "ANALYSIS\n"
    )

    output_text.insert(
        tk.END,
        "------------------------------------------------\n"
    )


    if performance == "Excellent":

        message = (
            "The student is performing very well "
            "in studies and attendance."
        )

    elif performance == "Good":

        message = (
            "The student is performing well. "
            "Improving weaker subjects can increase "
            "the overall performance."
        )

    elif performance == "Average":

        message = (
            "The student needs more focus on studies "
            "and regular attendance."
        )

    else:

        message = (
            "The student needs significant improvement "
            "in studies and attendance."
        )


    output_text.insert(
        tk.END,
        message
    )



# ============================================================
# PREDICT PERFORMANCE
# ============================================================

def predict_performance():

    student = get_student()

    if student is None:
        return


    # -------------------------
    # SUBJECT MARKS
    # -------------------------

    study_marks = np.array([

        float(student["Python"]),

        float(student["Java"]),

        float(student["DBMS"]),

        float(student["OS"]),

        float(student["DMS"])
    ])


    # -------------------------
    # ATTENDANCE
    # -------------------------

    attendance = np.array([

        float(student["Python_Att"]),

        float(student["Java_Att"]),

        float(student["DBMS_Att"]),

        float(student["OS_Att"]),

        float(student["DMS_Att"])
    ])


    study_average = np.mean(
        study_marks
    )


    attendance_average = np.mean(
        attendance
    )


    # -------------------------
    # PREDICTION FORMULA
    # -------------------------

    predicted_score = (

        study_average * 0.70

        +

        attendance_average * 0.30
    )


    prediction = get_performance(
        predicted_score
    )


    output_text.delete(
        "1.0",
        tk.END
    )


    output_text.insert(
        tk.END,
        "================================================\n"
    )

    output_text.insert(
        tk.END,
        "           STUDENT PERFORMANCE PREDICTION\n"
    )

    output_text.insert(
        tk.END,
        "================================================\n\n"
    )


    output_text.insert(
        tk.END,
        f"Roll Number          : {student['RollNo']}\n"
    )

    output_text.insert(
        tk.END,
        f"Student              : {student['Name']}\n\n"
    )


    output_text.insert(
        tk.END,
        f"Study Performance    : {study_average:.2f}%\n"
    )

    output_text.insert(
        tk.END,
        f"Attendance           : {attendance_average:.2f}%\n\n"
    )


    output_text.insert(
        tk.END,
        "Prediction Calculation\n"
    )

    output_text.insert(
        tk.END,
        "------------------------------------------------\n"
    )

    output_text.insert(
        tk.END,
        "Studies       × 70%\n"
    )

    output_text.insert(
        tk.END,
        "Attendance    × 30%\n\n"
    )


    output_text.insert(
        tk.END,
        f"Predicted Score      : {predicted_score:.2f}%\n"
    )

    output_text.insert(
        tk.END,
        f"Predicted Performance: {prediction}\n"
    )


    output_text.insert(
        tk.END,
        "\n------------------------------------------------\n"
    )


    # -------------------------
    # RECOMMENDATION
    # -------------------------

    weakest_index = np.argmin(
        study_marks
    )

    subjects = [
        "Python",
        "Java",
        "DBMS",
        "OS",
        "DMS"
    ]

    weakest_subject = subjects[
        weakest_index
    ]


    output_text.insert(
        tk.END,
        "\nRECOMMENDATION\n"
    )

    output_text.insert(
        tk.END,
        "------------------------------------------------\n"
    )

    output_text.insert(
        tk.END,
        f"Focus more on {weakest_subject} "
        f"to improve overall performance."
    )



# ============================================================
# BUTTON FRAME
# ============================================================

button_frame = tk.Frame(
    root,
    bg="#f2f4f7"
)

button_frame.pack(
    pady=15
)


# ============================================================
# STUDIES BUTTON
# ============================================================

studies_button = tk.Button(
    button_frame,
    text="Studies Performance",
    font=("Arial", 12, "bold"),
    width=20,
    command=show_studies
)

studies_button.grid(
    row=0,
    column=0,
    padx=7,
    pady=5
)


# ============================================================
# ATTENDANCE BUTTON
# ============================================================

attendance_button = tk.Button(
    button_frame,
    text="Attendance Performance",
    font=("Arial", 12, "bold"),
    width=20,
    command=show_attendance
)

attendance_button.grid(
    row=0,
    column=1,
    padx=7,
    pady=5
)


# ============================================================
# OVERALL BUTTON
# ============================================================

overall_button = tk.Button(
    button_frame,
    text="Overall Performance",
    font=("Arial", 12, "bold"),
    width=20,
    command=show_overall
)

overall_button.grid(
    row=0,
    column=2,
    padx=7,
    pady=5
)


# ============================================================
# PREDICTION BUTTON
# ============================================================

predict_button = tk.Button(
    button_frame,
    text="Predict Performance",
    font=("Arial", 12, "bold"),
    width=20,
    command=predict_performance
)

predict_button.grid(
    row=0,
    column=3,
    padx=7,
    pady=5
)


# ============================================================
# EXIT BUTTON
# ============================================================

exit_button = tk.Button(
    button_frame,
    text="Exit",
    font=("Arial", 12, "bold"),
    width=10,
    command=root.destroy
)

exit_button.grid(
    row=1,
    column=1,
    columnspan=2,
    pady=10
)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()
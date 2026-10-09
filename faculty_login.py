import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection


# =========================================================
# FACULTY LOGIN
# =========================================================

def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username == "" or password == "":
        messagebox.showwarning(
            "Login",
            "Please enter username and password."
        )
        return

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT faculty_id, faculty_name
            FROM faculty
            WHERE username = :username
            AND password = :password
        """

        cursor.execute(
            query,
            username=username,
            password=password
        )

        faculty = cursor.fetchone()

        cursor.close()
        connection.close()

        if faculty:
            faculty_id = faculty[0]
            faculty_name = faculty[1]

            root.withdraw()

            open_dashboard(
                faculty_id,
                faculty_name
            )

        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# FACULTY DASHBOARD
# =========================================================

def open_dashboard(faculty_id, faculty_name):

    dashboard = tk.Toplevel(root)

    dashboard.title(
        "Faculty Dashboard - Student Performance System"
    )

    dashboard.geometry("1100x700")

    dashboard.protocol(
        "WM_DELETE_WINDOW",
        lambda: close_dashboard(dashboard)
    )

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    title = tk.Label(
        dashboard,
        text="STUDENT PERFORMANCE SYSTEM",
        font=("Arial", 22, "bold")
    )

    title.pack(pady=(20, 5))

    faculty_label = tk.Label(
        dashboard,
        text=f"Faculty: {faculty_name}",
        font=("Arial", 12)
    )

    faculty_label.pack(pady=(0, 15))

    # -----------------------------------------------------
    # SELECTION FRAME
    # -----------------------------------------------------

    selection_frame = tk.Frame(
        dashboard,
        bd=2,
        relief="groove"
    )

    selection_frame.pack(
        fill="x",
        padx=20,
        pady=10
    )

    # SECTION

    tk.Label(
        selection_frame,
        text="Section:",
        font=("Arial", 11, "bold")
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=15
    )

    section_combo = ttk.Combobox(
        selection_frame,
        values=[
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I"
        ],
        state="readonly",
        width=15
    )

    section_combo.grid(
        row=0,
        column=1,
        padx=10
    )

    section_combo.set("B")

    # SUBJECT

    tk.Label(
        selection_frame,
        text="Subject:",
        font=("Arial", 11, "bold")
    ).grid(
        row=0,
        column=2,
        padx=10
    )

    subject_combo = ttk.Combobox(
        selection_frame,
        values=[
            "Python",
            "Java",
            "DBMS",
            "OS",
            "DMS"
        ],
        state="readonly",
        width=15
    )

    subject_combo.grid(
        row=0,
        column=3,
        padx=10
    )

    subject_combo.set("Python")

    # LOAD BUTTON

    load_button = tk.Button(
        selection_frame,
        text="LOAD STUDENTS",
        width=18,
        command=lambda: load_students(
            section_combo,
            subject_combo,
            tree
        )
    )

    load_button.grid(
        row=0,
        column=4,
        padx=20
    )

    # -----------------------------------------------------
    # STUDENT TABLE
    # -----------------------------------------------------

    table_frame = tk.Frame(dashboard)

    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    columns = (
        "roll_no",
        "student_name",
        "marks",
        "attendance"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=18
    )

    tree.heading(
        "roll_no",
        text="Roll Number"
    )

    tree.heading(
        "student_name",
        text="Student Name"
    )

    tree.heading(
        "marks",
        text="Marks"
    )

    tree.heading(
        "attendance",
        text="Attendance %"
    )

    tree.column(
        "roll_no",
        width=150
    )

    tree.column(
        "student_name",
        width=350
    )

    tree.column(
        "marks",
        width=100,
        anchor="center"
    )

    tree.column(
        "attendance",
        width=130,
        anchor="center"
    )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # -----------------------------------------------------
    # ENTRY FRAME
    # -----------------------------------------------------

    entry_frame = tk.Frame(
        dashboard,
        bd=2,
        relief="groove"
    )

    entry_frame.pack(
        fill="x",
        padx=20,
        pady=10
    )

    instruction_label = tk.Label(
        entry_frame,
        text="Select a student from the table",
        font=("Arial", 10, "bold")
    )

    instruction_label.grid(
        row=0,
        column=0,
        columnspan=4,
        pady=8
    )

    # MARKS

    tk.Label(
        entry_frame,
        text="Marks (0-100):"
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )

    marks_entry = tk.Entry(
        entry_frame,
        width=15
    )

    marks_entry.grid(
        row=1,
        column=1
    )

    # ATTENDANCE

    tk.Label(
        entry_frame,
        text="Attendance (0-100):"
    ).grid(
        row=1,
        column=2,
        padx=10
    )

    attendance_entry = tk.Entry(
        entry_frame,
        width=15
    )

    attendance_entry.grid(
        row=1,
        column=3
    )

    # SAVE BUTTON

    save_button = tk.Button(
        entry_frame,
        text="SAVE MARKS & ATTENDANCE",
        width=25,
        command=lambda: save_student_data(
            tree,
            marks_entry,
            attendance_entry,
            subject_combo
        )
    )

    save_button.grid(
        row=2,
        column=0,
        columnspan=4,
        pady=12
    )

    # -----------------------------------------------------
    # ENTER KEY SUPPORT
    # -----------------------------------------------------

    marks_entry.bind(
        "<Return>",
        lambda event: save_student_data(
            tree,
            marks_entry,
            attendance_entry,
            subject_combo
        )
    )

    attendance_entry.bind(
        "<Return>",
        lambda event: save_student_data(
            tree,
            marks_entry,
            attendance_entry,
            subject_combo
        )
    )

    # -----------------------------------------------------
    # TABLE SELECTION
    # -----------------------------------------------------

    tree.bind(
        "<<TreeviewSelect>>",
        lambda event: select_student(
            tree,
            marks_entry,
            attendance_entry
        )
    )

    # -----------------------------------------------------
    # LOGOUT
    # -----------------------------------------------------

    logout_button = tk.Button(
        dashboard,
        text="LOGOUT",
        width=15,
        command=lambda: close_dashboard(dashboard)
    )

    logout_button.pack(
        pady=10
    )


# =========================================================
# LOAD STUDENTS
# =========================================================

def load_students(
    section_combo,
    subject_combo,
    tree
):

    section = section_combo.get()
    subject = subject_combo.get()

    if not section or not subject:

        messagebox.showwarning(
            "Selection",
            "Please select section and subject."
        )

        return

    # Clear previous data

    for item in tree.get_children():
        tree.delete(item)

    try:

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                s.roll_no,
                s.student_name,
                m.marks,
                a.attendance_percentage
            FROM students s

            JOIN sections sec
                ON s.section_id = sec.section_id

            LEFT JOIN subjects sub
                ON sub.subject_name = :subject_name

            LEFT JOIN marks m
                ON m.student_id = s.student_id
                AND m.subject_id = sub.subject_id

            LEFT JOIN attendance a
                ON a.student_id = s.student_id
                AND a.subject_id = sub.subject_id

            WHERE sec.section_name = :section_name

            ORDER BY s.roll_no
        """

        cursor.execute(
            query,
            section_name=section,
            subject_name=subject
        )

        rows = cursor.fetchall()

        for row in rows:

            roll_no = row[0]
            student_name = row[1]

            if row[2] is None:
                marks = ""
            else:
                marks = row[2]

            if row[3] is None:
                attendance = ""
            else:
                attendance = row[3]

            tree.insert(
                "",
                "end",
                values=(
                    roll_no,
                    student_name,
                    marks,
                    attendance
                )
            )

        cursor.close()
        connection.close()

        if len(rows) == 0:

            messagebox.showwarning(
                "No Students",
                f"No students found in Section {section}."
            )

        else:

            messagebox.showinfo(
                "Students Loaded",
                f"{len(rows)} students loaded.\n\n"
                f"Section: {section}\n"
                f"Subject: {subject}"
            )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# SELECT STUDENT
# =========================================================

def select_student(
    tree,
    marks_entry,
    attendance_entry
):

    selected = tree.selection()

    if not selected:
        return

    values = tree.item(
        selected[0],
        "values"
    )

    # Clear entries

    marks_entry.delete(
        0,
        tk.END
    )

    attendance_entry.delete(
        0,
        tk.END
    )

    # Existing marks

    if values[2] != "":
        marks_entry.insert(
            0,
            values[2]
        )

    # Existing attendance

    if values[3] != "":
        attendance_entry.insert(
            0,
            values[3]
        )

    # Automatically focus marks

    marks_entry.focus_set()


# =========================================================
# SAVE MARKS AND ATTENDANCE
# =========================================================

def save_student_data(
    tree,
    marks_entry,
    attendance_entry,
    subject_combo
):

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "Student",
            "Please select a student first."
        )

        return

    values = tree.item(
        selected[0],
        "values"
    )

    roll_no = values[0]
    student_name = values[1]

    marks_text = marks_entry.get().strip()
    attendance_text = attendance_entry.get().strip()

    # -----------------------------------------------------
    # Check empty values
    # -----------------------------------------------------

    if marks_text == "":

        messagebox.showwarning(
            "Marks",
            "Please enter marks."
        )

        marks_entry.focus_set()

        return

    if attendance_text == "":

        messagebox.showwarning(
            "Attendance",
            "Please enter attendance."
        )

        attendance_entry.focus_set()

        return

    # -----------------------------------------------------
    # Convert to numbers
    # -----------------------------------------------------

    try:

        marks = float(marks_text)
        attendance = float(attendance_text)

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Marks and attendance must be numbers."
        )

        return

    # -----------------------------------------------------
    # Validate marks
    # -----------------------------------------------------

    if marks < 0 or marks > 100:

        messagebox.showerror(
            "Invalid Marks",
            "Marks must be between 0 and 100."
        )

        marks_entry.focus_set()

        return

    # -----------------------------------------------------
    # Validate attendance
    # -----------------------------------------------------

    if attendance < 0 or attendance > 100:

        messagebox.showerror(
            "Invalid Attendance",
            "Attendance must be between 0 and 100."
        )

        attendance_entry.focus_set()

        return

    subject = subject_combo.get()

    if subject == "":

        messagebox.showwarning(
            "Subject",
            "Please select a subject."
        )

        return

    try:

        connection = get_connection()
        cursor = connection.cursor()

        # -------------------------------------------------
        # Get Student ID
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT student_id
            FROM students
            WHERE roll_no = :roll_no
            """,
            roll_no=roll_no
        )

        student = cursor.fetchone()

        if student is None:

            cursor.close()
            connection.close()

            messagebox.showerror(
                "Error",
                "Student not found in database."
            )

            return

        student_id = student[0]

        # -------------------------------------------------
        # Get Subject ID
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT subject_id
            FROM subjects
            WHERE subject_name = :subject_name
            """,
            subject_name=subject
        )

        subject_row = cursor.fetchone()

        if subject_row is None:

            cursor.close()
            connection.close()

            messagebox.showerror(
                "Error",
                "Subject not found in database."
            )

            return

        subject_id = subject_row[0]

        # -------------------------------------------------
        # MARKS
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM marks
            WHERE student_id = :student_id
            AND subject_id = :subject_id
            """,
            student_id=student_id,
            subject_id=subject_id
        )

        marks_exists = cursor.fetchone()[0]

        if marks_exists > 0:

            cursor.execute(
                """
                UPDATE marks
                SET marks = :marks,
                    entered_date = SYSDATE
                WHERE student_id = :student_id
                AND subject_id = :subject_id
                """,
                marks=marks,
                student_id=student_id,
                subject_id=subject_id
            )

        else:

            cursor.execute(
                """
                INSERT INTO marks
                (
                    student_id,
                    subject_id,
                    marks
                )
                VALUES
                (
                    :student_id,
                    :subject_id,
                    :marks
                )
                """,
                student_id=student_id,
                subject_id=subject_id,
                marks=marks
            )

        # -------------------------------------------------
        # ATTENDANCE
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM attendance
            WHERE student_id = :student_id
            AND subject_id = :subject_id
            """,
            student_id=student_id,
            subject_id=subject_id
        )

        attendance_exists = cursor.fetchone()[0]

        if attendance_exists > 0:

            cursor.execute(
                """
                UPDATE attendance
                SET attendance_percentage = :attendance,
                    entered_date = SYSDATE
                WHERE student_id = :student_id
                AND subject_id = :subject_id
                """,
                attendance=attendance,
                student_id=student_id,
                subject_id=subject_id
            )

        else:

            cursor.execute(
                """
                INSERT INTO attendance
                (
                    student_id,
                    subject_id,
                    attendance_percentage
                )
                VALUES
                (
                    :student_id,
                    :subject_id,
                    :attendance
                )
                """,
                student_id=student_id,
                subject_id=subject_id,
                attendance=attendance
            )

        # -------------------------------------------------
        # COMMIT
        # -------------------------------------------------

        connection.commit()

        cursor.close()
        connection.close()

        # -------------------------------------------------
        # UPDATE TABLE
        # -------------------------------------------------

        tree.item(
            selected[0],
            values=(
                roll_no,
                student_name,
                marks,
                attendance
            )
        )

        # -------------------------------------------------
        # SUCCESS MESSAGE
        # -------------------------------------------------

        messagebox.showinfo(
            "Saved Successfully",
            f"Student: {student_name}\n"
            f"Roll No: {roll_no}\n"
            f"Subject: {subject}\n\n"
            f"Marks: {marks}\n"
            f"Attendance: {attendance}%\n\n"
            f"Data saved to Oracle database."
        )

        # Clear entries

        marks_entry.delete(
            0,
            tk.END
        )

        attendance_entry.delete(
            0,
            tk.END
        )

        # Keep focus on table

        tree.focus(
            selected[0]
        )

        tree.selection_set(
            selected[0]
        )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Could not save data.\n\n{e}"
        )


# =========================================================
# CLOSE DASHBOARD
# =========================================================

def close_dashboard(dashboard):

    dashboard.destroy()

    root.deiconify()

    username_entry.focus_set()


# =========================================================
# LOGIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Faculty Login - Student Performance System"
)

root.geometry(
    "500x400"
)

root.resizable(
    False,
    False
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

tk.Label(
    root,
    text="STUDENT PERFORMANCE SYSTEM",
    font=("Arial", 20, "bold")
).pack(
    pady=(45, 10)
)


tk.Label(
    root,
    text="Faculty Login",
    font=("Arial", 14)
).pack(
    pady=10
)


# ---------------------------------------------------------
# USERNAME
# ---------------------------------------------------------

tk.Label(
    root,
    text="Username"
).pack(
    pady=(15, 5)
)


username_entry = tk.Entry(
    root,
    width=30
)

username_entry.pack()


# ---------------------------------------------------------
# PASSWORD
# ---------------------------------------------------------

tk.Label(
    root,
    text="Password"
).pack(
    pady=(15, 5)
)


password_entry = tk.Entry(
    root,
    width=30,
    show="*"
)

password_entry.pack()


# ---------------------------------------------------------
# LOGIN BUTTON
# ---------------------------------------------------------

tk.Button(
    root,
    text="LOGIN",
    width=18,
    command=login
).pack(
    pady=30
)


# Press Enter on password to login

password_entry.bind(
    "<Return>",
    lambda event: login()
)


# ---------------------------------------------------------
# START APPLICATION
# ---------------------------------------------------------

root.mainloop()
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font as tkfont
from email.message import EmailMessage
import smtplib
from random import randint
import sqlite3


# Database class to handle DB operations
class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

        # Create tables if they don't exist
        self.cur.execute('''CREATE TABLE IF NOT EXISTS student (
            Student_ID INTEGER PRIMARY KEY,
            Name TEXT,
            Department TEXT
        )''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS attendance (
             No INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT,
            Module TEXT,
            Department TEXT,
            Student_ID INTEGER,
            Status TEXT,
            FOREIGN KEY(Student_ID) REFERENCES student(Student_ID)
        )''')
        self.con.commit()

    def add_student(self, student_id, name, department):
        self.cur.execute("INSERT INTO student VALUES (?, ?, ?)", (student_id, name, department))
        self.con.commit()

    def mark_attendance(self, date, module, department, status, student_id):
        self.cur.execute("INSERT INTO attendance (Date, Module, Department, Status, Student_ID) VALUES (?, ?, ?, ?, ?)",
                         (date, module, department, status, student_id))
        self.con.commit()

    def get_students_by_department(self, department):
        self.cur.execute("SELECT Student_ID, Name FROM student WHERE Department = ?", (department,))
        return self.cur.fetchall()

    def display_students(self):
        self.cur.execute("SELECT * FROM student")
        return self.cur.fetchall()

    def display_attendance(self):
        self.cur.execute("SELECT * FROM attendance")
        return self.cur.fetchall()


# Function to send verification code to admin email
def send_verification_code(email):
    code = randint(1000, 9999)  # Generate a 4-digit random code

    # Create email message
    msg = EmailMessage()
    msg.set_content(f"Your verification code is {code}.")
    msg['Subject'] = 'Admin Verification Code'
    msg['From'] = 'baushan235@gmail.com@gmail.com'
    msg['To'] = 'baushan235@gmail.com'

    # Set up the SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('baushan235@gmail.com', 'miha wxzw idjb murz')
        server.send_message(msg)

    return code


# Main Application Class for the GUI
class AttendanceApp:
    def __init__(self, root):
        self.db = Database('attendance.db')
        self.root = root
        self.root.title("Student Attendance Management")
        self.root.geometry("900x600")
        self.root.configure(bg="#2c3e50")
        # self.root.resizable(False, False)

        self.student_id = tk.StringVar()
        self.name = tk.StringVar()
        self.department = tk.StringVar()

        self.main_font = tkfont.Font(family='Helvetica', size=14)

        # Initialize Admin Login View
        self.home_frame = tk.Frame(self.root, bg="#2c3e50")
        self.home_frame.pack(fill="both", expand=True)

        # Title
        self.create_title()

        # Admin Login Button
        self.create_button(self.home_frame, "Admin Login", self.admin_login, 18, "#16a085", "#1abc9c")

    def create_title(self):
        tk.Label(self.home_frame, text="Student Attendance Management", font=('Helvetica', 20, 'bold'), bg="#2c3e50",
                 fg="white").pack(pady=40)

    def create_button(self, parent, text, command, font_size, bg_color, fg_color):
        button = tk.Button(parent, text=text, font=('Helvetica', font_size), bg=bg_color, fg=fg_color, relief="flat",
                           width=20, height=2, command=command)
        button.pack(pady=10)

    # Admin Login Function with Verification
    def admin_login(self):
        self.clear_frame()

        login_frame = tk.Frame(self.root, bg="#ecf0f1")
        login_frame.pack(fill="both", expand=True)

        # Title
        tk.Label(login_frame, text="Admin Login", font=('Helvetica', 20, 'bold'), bg="#ecf0f1", fg="#34495e").pack(
            pady=20)

        # Verification code prompt
        tk.Label(login_frame, text="Enter verification code sent to your email:", font=self.main_font, bg="#ecf0f1",
                 fg="#34495e").pack(pady=10)

        self.code_entry = tk.Entry(login_frame, font=self.main_font)
        self.code_entry.pack(pady=10, ipady=5)

        # Send verification code
        self.verification_code = send_verification_code('admin_email@example.com')

        self.create_button(login_frame, "Submit", self.verify_admin, 16, "#16a085", "#1abc9c")

    def verify_admin(self):
        entered_code = self.code_entry.get()
        if entered_code == str(self.verification_code):
            self.admin_panel()
        else:
            messagebox.showerror("Error", "Incorrect verification code!")

    # Admin Panel Navigation
    def admin_panel(self):
        self.clear_frame()

        panel_frame = tk.Frame(self.root, bg="#34495e")
        panel_frame.pack(fill="both", expand=True)

        tk.Label(panel_frame, text="Admin Panel", font=('Helvetica', 20, 'bold'), bg="#34495e", fg="white").pack(
            pady=30)

        self.create_button(panel_frame, "Add Student", self.add_student_view, 16, "#e74c3c", "#fff")
        self.create_button(panel_frame, "Mark Attendance", self.mark_attendance_view, 16, "#2980b9", "#fff")
        self.create_button(panel_frame, "View Attendance Records", self.view_attendance_records, 16, "#f39c12", "#fff")

    # Add Student View
    def add_student_view(self):
        self.clear_frame()

        add_student_frame = tk.Frame(self.root, bg="#ecf0f1")
        add_student_frame.pack(fill="both", expand=True)

        tk.Label(add_student_frame, text="Add Student", font=('Helvetica', 20, 'bold'), bg="#ecf0f1",
                 fg="#34495e").pack(pady=20)

        tk.Label(add_student_frame, text="Student ID:", font=self.main_font, bg="#ecf0f1", fg="#34495e").pack(pady=5)
        self.student_id_entry = tk.Entry(add_student_frame, font=self.main_font)
        self.student_id_entry.pack(pady=5)

        tk.Label(add_student_frame, text="Name:", font=self.main_font, bg="#ecf0f1", fg="#34495e").pack(pady=5)
        self.name_entry = tk.Entry(add_student_frame, font=self.main_font)
        self.name_entry.pack(pady=5)

        tk.Label(add_student_frame, text="Department:", font=self.main_font, bg="#ecf0f1", fg="#34495e").pack(pady=5)
        departments = ["TCT", "FDT", "TV-PO", "TV-PR", "ECT", "Fashion", "Cosmo"]
        self.department_menu = ttk.Combobox(add_student_frame, values=departments, font=self.main_font)
        self.department_menu.pack(pady=5)

        self.create_button(add_student_frame, "Add Student", self.add_student, 16, "#16a085", "#fff")

    def add_student(self):
        student_id = self.student_id_entry.get()
        name = self.name_entry.get()
        department = self.department_menu.get()
        if student_id and name and department:
            self.db.add_student(student_id, name, department)
            messagebox.showinfo("Success", "Student added successfully")
        else:
            messagebox.showerror("Error", "All fields are required!")

    # Mark Attendance View
    def mark_attendance_view(self):
        self.clear_frame()

        mark_attendance_frame = tk.Frame(self.root, bg="#ecf0f1")
        mark_attendance_frame.pack(fill="both", expand=True)

        tk.Label(mark_attendance_frame, text="Mark Attendance", font=('Helvetica', 20, 'bold'), bg="#ecf0f1",
                 fg="#34495e").pack(pady=20)

        tk.Label(mark_attendance_frame, text="Date (YYYY-MM-DD):", font=self.main_font, bg="#ecf0f1",
                 fg="#34495e").pack(pady=5)
        self.date_entry = tk.Entry(mark_attendance_frame, font=self.main_font)
        self.date_entry.pack(pady=5)

        tk.Label(mark_attendance_frame, text="Module:", font=self.main_font, bg="#ecf0f1", fg="#34495e").pack(pady=5)
        self.module_entry = tk.Entry(mark_attendance_frame, font=self.main_font)
        self.module_entry.pack(pady=5)

        tk.Label(mark_attendance_frame, text="Student ID:", font=self.main_font, bg="#ecf0f1", fg="#34495e").pack(
            pady=5)
        self.student_id_attendance_entry = tk.Entry(mark_attendance_frame, font=self.main_font)
        self.student_id_attendance_entry.pack(pady=5)

        tk.Label(mark_attendance_frame, text="Status:", font=self.main_font, bg="#ecf0f1", fg="#34495e").pack(pady=5)
        status_options = ["Present", "Absent"]
        self.status_menu = ttk.Combobox(mark_attendance_frame, values=status_options, font=self.main_font)
        self.status_menu.pack(pady=5)

        self.create_button(mark_attendance_frame, "Mark Attendance", self.mark_attendance, 16, "#16a085", "#fff")

    def mark_attendance(self):
        date = self.date_entry.get()
        module = self.module_entry.get()
        student_id = self.student_id_attendance_entry.get()
        status = self.status_menu.get()

        if date and module and student_id and status:
            self.db.mark_attendance(date, module, status, student_id)
            messagebox.showinfo("Success", "Attendance marked successfully")
        else:
            messagebox.showerror("Error", "All fields are required!")

    # View Attendance Records
    def view_attendance_records(self):
        self.clear_frame()

        records_frame = tk.Frame(self.root, bg="#ecf0f1")
        records_frame.pack(fill="both", expand=True)

        tk.Label(records_frame, text="Attendance Records", font=('Helvetica', 20, 'bold'), bg="#ecf0f1",
                 fg="#34495e").pack(pady=20)

        attendance_records = self.db.display_attendance()
        columns = ("No", "Date", "Module", "Department", "Student_ID", "Status")
        tree = ttk.Treeview(records_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        for record in attendance_records:
            tree.insert("", "end", values=record)

        tree.pack(pady=20)

    # Clear the frame content
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()

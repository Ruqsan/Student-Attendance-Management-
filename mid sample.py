# pip install tk smtplib sqlite3
import smtplib
import sqlite3
from email.message import EmailMessage
from random import randint

# Database class
class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

        # Create table for student details
        self.cur.execute('''CREATE TABLE IF NOT EXISTS student (
            Student_ID INTEGER PRIMARY KEY,
            Name TEXT,
            Department TEXT
        )''')

        # Create table for attendance
        self.cur.execute('''CREATE TABLE IF NOT EXISTS attendance (
            No INTEGER PRIMARY KEY AUTOINCREMENT,
            Date INTEGER,
            Module TEXT,
            Department TEXT,
            Student_ID INTEGER,
            FOREIGN KEY(Student_ID) REFERENCES student(Student_ID)
        )''')
        self.con.commit()

    # Add student to the database
    def add_student(self, student_id, name, department):
        self.cur.execute("INSERT INTO student VALUES (?, ?, ?)", (student_id, name, department))
        self.con.commit()

    # Update attendance in the database
    def mark_attendance(self, Date, Module, Department,Student_ID):
        self.cur.execute("INSERT INTO attendance (Date, Module, Department,Student_ID) VALUES (?, ?, ?,?)",
                         (Date, Module, Department,Student_ID))
        return self.con.commit()

    # Fetch student attendance
    def fetch_attendance(self, Student_ID):
        self.cur.execute("SELECT Module, Date FROM attendance WHERE Student_ID = ?", (Student_ID,))
        return self.cur.fetchall()

    # Get student list by department for marking attendance
    def get_students_by_department(self, department):
        self.cur.execute("SELECT Student_ID, Name FROM student WHERE Department = ?", (department,))
        return self.cur.fetchall()

# Function to send verification code to admin's email
def send_verification_code(email):
    code = randint(1000, 9999)  # Generate a 4-digit random code

    # Send the code to a fixed email using SMTP
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

import tkinter as tk
from tkinter import messagebox


class AttendanceApp:
    def __init__(self, root):
        self.db = Database('attendance.db')

        self.root = root
        self.root.title("Student Attendance Management")

        # Home page with Admin and Student buttons
        self.home_frame = tk.Frame(self.root)
        self.home_frame.pack()

        tk.Label(self.home_frame, text="Student Attendance Management", font=('Arial', 18)).pack(pady=20)
        tk.Button(self.home_frame, text="Admin", width=20, command=self.admin_login).pack(pady=10)
        tk.Button(self.home_frame, text="Student", width=20, command=self.student_portal).pack(pady=10)

    # Admin Login (Protected by email verification)
    def admin_login(self):
        self.clear_frame()

        tk.Label(self.root, text="Admin Login", font=('Arial', 18)).pack(pady=20)
        tk.Label(self.root, text="Enter verification code sent to your email:").pack(pady=5)

        self.code_entry = tk.Entry(self.root)
        self.code_entry.pack(pady=5)

        # Send verification code
        self.verification_code = send_verification_code('admin_email@example.com')

        tk.Button(self.root, text="Submit", command=self.verify_admin).pack(pady=10)

    def verify_admin(self):
        entered_code = self.code_entry.get()

        if entered_code == str(self.verification_code):
            self.admin_panel()
        else:
            messagebox.showerror("Error", "Incorrect verification code!")

    # Admin Panel
    def admin_panel(self):
        self.clear_frame()
        tk.Label(self.root, text="Admin Panel", font=('Arial', 18)).pack(pady=20)
        tk.Button(self.root, text="Add Info", width=20, command=self.add_info).pack(pady=10)
        tk.Button(self.root, text="Attendance", width=20, command=self.attendance_frame).pack(pady=10)
        # Add Student Section
    def add_info(self):
        self.clear_frame()
        tk.Label( self.root, text="Add Student").pack(pady=5)
        tk.Label(self.root, text="Student ID").pack(pady=2)
        self.student_id_entry = tk.Entry(self.root)
        self.student_id_entry.pack(pady=2)

        tk.Label(self.root, text="Name").pack(pady=2)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=2)

        tk.Label(self.root, text="Department").pack(pady=2)
        # var = tk.StringVar(self.root)
        # var.set('Select the department')
        # self.attendance_dept__entry = tk.OptionMenu(self.root,var, "TCT", "FDT", "TV-PO", "TV-PR", "ECT", "FDT", "COSMO", "EM")
        # self.attendance_dept_entry = tk.Entry(self.root)
        # self.attendance_dept_entry.pack(pady=2)
        options = ["TCT", "FDT", "TV-PO", "TV-PR", "ECT", "FDT", "COSMO", "EM"]
        self.Selected_opt = tk.StringVar()
        self.Selected_opt.set(self.root)
        self.attendance_dept_entry = tk.OptionMenu(self.root, self.Selected_opt, *options)
        self.attendance_dept_entry.pack(pady=2)

        tk.Button(self.root, text="Add Student", command=self.add_student).pack(pady=10)
    # def show
        # Mark Attendance Section
    def attendance_frame(self):
        self.clear_frame()
        tk.Label(self.root, text="Mark Attendance").pack(pady=20)
        tk.Label(self.root, text="Date (YYYY-MM-DD):").pack(pady=2)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.pack(pady=2)

        tk.Label(self.root, text="Module:").pack(pady=2)
        self.module_entry = tk.Entry(self.root)
        self.module_entry.pack(pady=2)

        tk.Label(self.root, text="Department:").pack(pady=2)
        # self.attendance_dept_entry = tk.Entry(self.root)
        # self.attendance_dept_entry = tk.OptionMenu(self.root,"TCT","FDT","TV-PO","TV-PR","ECT","FDT","COSMO","EM")

        # self.attendance_dept_entry.pack(pady=2)
        options = ["TCT", "FDT", "TV-PO", "TV-PR", "ECT", "FDT", "COSMO", "EM"]
        self.Selected_opt = tk.StringVar()
        self.Selected_opt.set(self.root)
        self.attendance_dept_entry = tk.OptionMenu(self.root, self.Selected_opt, *options)
        self.attendance_dept_entry.pack(pady=2)
        tk.Button(self.root, text="Load Students", command=self.load_students).pack(pady=10)
        tk.Button(self.root, text="Mark", command=self.mark_attendance).pack(pady=10)

    # Load Students for Attendance
    def load_students(self):
        # department = self.attendance_dept_entry.get()
        # department =self.department_entry = tk.OptionMenu(self.root,var,"TCT","FDT","TV-PO","TV-PR","ECT","FDT","COSMO","EM")
        department = self.Selected_opt.get()
        students = self.db.get_students_by_department(department)

    #     for student in students:
    #         student_id, name = student
    #         var = tk.IntVar()
    #         tk.Checkbutton(self.root, text=f"{name} ({student_id})", variable=var).pack(anchor='w')
        self.student_checkboxes = []  # Clear previous checkboxes

        for student in students:
            Student_ID, name = student
            var = tk.IntVar()
            tk.Checkbutton(self.root, text=f"{name} ({Student_ID})", variable=var).pack(anchor='w')

    # Store the student information and checkbox variable for later use
            self.student_checkboxes.append((student, var))
    # def mark_attendance(self):
    #     try :
    #         date = self.date_entry.get()
    #         module = self.module_entry.get()
    #         department = self.department_entry.get()
    #
    #         if date and module and department:
    #             self.db.mark_attendance(date, module, department)
    #             messagebox.showinfo("Success", "Attendance added successfully")
    #         else:
    #             messagebox.showerror("Error", "All fields are required!")
    #     except sqlite3.IntegrityError:
    #          messagebox.showerror("Error","Incorrect Information")
    def mark_attendance(self):
        try:
            date = self.date_entry.get()
            module = self.module_entry.get()
            department = self.Selected_opt.get()
            # Student_ID =  self.student_checkboxes.append((student_id))
            Student_id = self.student_checkboxes
            if date and module and department and Student_id:
                for student, checkbox_var in self.student_checkboxes :
                    # Check if the checkbox is selected (checked)
                    if checkbox_var.get() == 1:
                        Student_id,name = student  # Unpack the student details
                        # Insert attendance record into the database for each selected student
                        self.db.mark_attendance(date, module, department,Student_id)

                messagebox.showinfo("Success", "Attendance added successfully")
            else:
                messagebox.showerror("Error", "All fields are required!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Incorrect Information")


    # Add Student Function
    def add_student(self):
        try :
            student_id = self.student_id_entry.get()
            name = self.name_entry.get()
            department = self.Selected_opt.get()

            if student_id and name and department:
                self.db.add_student(student_id, name, department)
                messagebox.showinfo("Success", "Student added successfully")
            else:
                messagebox.showerror("Error", "All fields are required!")
        except sqlite3.IntegrityError:
             messagebox.showerror("Error","Student_Id already Exists")
    # Student Portal
    def student_portal(self):
        self.clear_frame()

        tk.Label(self.root, text="Student Portal", font=('Arial', 18)).pack(pady=20)
        tk.Label(self.root, text="Enter Student ID").pack(pady=5)
        self.student_id_entry = tk.Entry(self.root)
        self.student_id_entry.pack(pady=5)

        tk.Button(self.root, text="View Attendance", command=self.view_attendance).pack(pady=10)

    # View Attendance
    def view_attendance(self):
        student_id = self.student_id_entry.get()
        attendance_records = self.db.fetch_attendance(student_id)

        if attendance_records:
            output = ""
            for record in attendance_records:
                output += f"Module: {record[0]}, Date: {record[1]}"
            messagebox.showinfo("Attendance", output)
        else:
            messagebox.showerror("Error", "No records found")

    # Utility to clear frames
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()

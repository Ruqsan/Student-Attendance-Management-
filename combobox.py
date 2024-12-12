import tkinter as tk
from tkinter import messagebox, Tk
from tkinter import ttk
import smtplib
import sqlite3
from email.message import EmailMessage
from random import randint
from db import Database
from PIL import ImageTk,Image,ImageFilter
from tkinter import Label
from tkcalendar import Calendar
from datetime import datetime, timedelta
# Database class
class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

        # Create table for student details
        self.cur.execute('''CREATE TABLE IF NOT EXISTS student (
            Student_ID STRING PRIMARY KEY,
            Name TEXT,
            Department TEXT
        )''')

        # Create table for attendance
        self.cur.execute('''CREATE TABLE IF NOT EXISTS attendance (
            Date INTEGER,
            Module TEXT,
            Department TEXT,
            Student_ID STRING,
            Status TEXT,
            FOREIGN KEY(Student_ID) REFERENCES student(Student_ID)
        )''')
        self.con.commit()

    # Add student to the database
    def add_student(self, student_id, name, department):
        self.cur.execute("INSERT INTO student VALUES (?, ?, ?)", (student_id, name, department))
        self.con.commit()

    # Update attendance in the database
    def mark_attendance(self, date, module, department, status, student_id):
        self.cur.execute("INSERT INTO attendance (Date, Module, Department,Status,Student_ID) VALUES (?, ?, ?,?,?)",
                         (date, module, department, status, student_id))
        return self.con.commit()

    # Fetch student attendance
    def fetch_attendance(self, Student_ID):
        self.cur.execute("SELECT Module, Date FROM attendance WHERE Student_ID = ?", (Student_ID,))
        return self.cur.fetchall()

    # Get student list by department for marking attendance
    def get_students_by_department(self, department):
        self.cur.execute("SELECT Student_ID, Name FROM student WHERE Department = ?", (department,))
        return self.cur.fetchall()

    # Get all the student details
    def display_St(self):
        self.cur.execute("SELECT * FROM student")
        rows = self.cur.fetchall()
        return rows

    # Get all the attendance details
    def display_att(self):
        self.cur.execute("SELECT * FROM attendance")
        lines = self.cur.fetchall()
        return lines

    # Delete records
    def remove(self):
        self.cur.execute("DELETE  FROM student WHERE Student_ID=?", (Student_ID,))
        records = self.cur.fetchone()
        return records

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


class AttendanceApp():
    def __init__(self, root):
        self.db = Database('attendance.db')
        super().__init__()
        self.con = sqlite3.connect('attendance.db')
        self.cur = self.con.cursor()
        self.root = root
        self.student_id = tk.StringVar()
        self.name = tk.StringVar()
        self.department = tk.StringVar()
        self.root.title("Student Attendance Management")
        self.root.geometry("1920x1080")
        # self.root.attributes("-alpha", 1)
        # self.root.attributes("-transparentcolor", "blue")
        # self.root.attributes("-topmost", True)  # Keep on top
        self.apply_background(self.root)
        # self.apply_background(
        #     file_path=r"C:/Users/Ruqsan/Downloads/wp9764031-login-page-wallpapers.jpg",
        #     position=(0, 0),
        #     size=(1920, 1080)
        # )
        # Label(self.root,image=(bg:=ImageTk.PhotoImage(Image.open(r"C:/Users/Ruqsan/Desktop/110832.jpg").resize((500,500))))).place(relwidth=1, relheight=1)
        self.tv = ttk.Treeview(self.root)
        # # Home page with Admin button
        # self.home_frame = tk.Frame(self.root,relief="solid")
        # self.home_frame.config(bg="#2c2e6b",bd=0)
        # self.home_frame.place(x=300,y=125,width =700,height=400)
        self.home_frame = tk.Frame(self.root, relief="raised")
        # self.home_frame.config(bg="#314965", bd=0)
        # Load the background image
        self.bg1_image = Image.open("C:/Users/Ruqsan/Desktop/Temporary files/line.jpg")  # Replace with your image path
        self.bg1_image = self.bg1_image.resize((700, 400))
        self.bg1_photo = ImageTk.PhotoImage(self.bg1_image)

        # Create a Label to hold the image
        self.bg1_label = tk.Label(self.home_frame, image=self.bg1_photo)
        self.bg1_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.home_frame.place(x=300, y=125, width=700, height=400)
        # # Middle vertical separator
        # separator = ttk.Separator(self.home_frame, orient="vertical")
        # separator.place(x=300, y=0, relheight=1)

        # # Create a transparent toplevel window
        # transparent_frame = tk.Toplevel(self.root,bd=3)
        # transparent_frame.geometry("700x400+275+175")
        # transparent_frame.overrideredirect(True)  # Remove window decorations
        # transparent_frame.attributes("-transparentcolor", "white")  # Set white as transparent
        # transparent_frame.attributes("-topmost", True)  # Keep on top
        #
        # canvas = tk.Canvas(transparent_frame, bg="white", highlightthickness=0)
        # canvas.pack(fill="both", expand=True)
        #
        # label = tk.Label(canvas, text="", bg="white")
        # label.place(relx=0.5, rely=0.5, anchor="center")


        # Load the image using Pillow
        image_path = "C:/Users/Ruqsan/Desktop/Temporary files/4182997.png"  # Replace with your image path
        self.image = Image.open(image_path)
        self.image = self.image.resize((250, 300))  # Resize the image (optional)
        self.tk_image = ImageTk.PhotoImage(self.image)
        # Middle vertical separator
        separator = ttk.Separator(self.home_frame, orient="vertical")
        separator.place(x=330, y=0, relheight=1)
        # Create a label to display the image
        self.label = tk.Label(self.home_frame, image=self.tk_image,relief ="raised")
        self.label.place(x=40,y=45)
        tk.Label(self.home_frame, text="Student Attendance Management", font=('Times New Roman', 18),fg="white",bg="#224980").place(x=360,y=100)
        self.create_button(self.home_frame, "Admin Login", self.admin_login, 18, "#224980", "#1abc9c").place(x=449,y=165)

    # def apply_background(self, file_path, position=(0, 0), size=(1920, 1080)):
    #     """
    #     Assigns a background image to the window.
    #
    #     :param file_path: str - Path to the image file.
    #     :param position: tuple - (x, y) position to place the image in the window.
    #     :param size: tuple - (width, height) of the resized image.
    #     """
    #     # Open the image file
    #     self.bg_image = Image.open(file_path)
    #
    #     # Resize the image to the specified size
    #     self.bg_image = self.bg_image.resize(size)
    #
    #     # Convert the image to a Tkinter-compatible PhotoImage
    #     self.bg_photo = ImageTk.PhotoImage(self.bg_image)
    #
    #     # Create a label to hold the background image
    #     self.bg_label = tk.Label(self.root, image=self.bg_photo)
    #
    #     # Position the label using place()
    #     self.bg_label.place(relwidth=1, relheight=1)
    #
    #     # Keep a reference to avoid garbage collection
    #     self.bg_label.image = self.bg_photo
    def apply_background(self, window):
        self.bg_image = Image.open(r"C:/Users/Ruqsan/Desktop/Temporary files/blur.jpg")
        self.bg_image = self.bg_image.resize((1920, 1080))  # Resize image to fit window
        # Apply a blur filter using Pillow
        # self.blurred_image = self.bg_image.filter(ImageFilter.GaussianBlur(radius=100))  # Adjust radius for blur intensity
        # Convert the image to a Tkinter-compatible format
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a label to hold the background image
        self.bg_label = tk.Label(self.root, image=self.bg_photo,relief="sunken")
        self.bg_label.place(relwidth=1, relheight=1)


    # def apply_background2(self, window):
    #     self.bg_image = Image.open(r"C:/Users/Ruqsan/Desktop/Temporary files/bg2.png")
    #     self.bg_image = self.bg_image.resize((1920, 1080))  # Resize image to fit window
    #
    #     # Convert the image to a Tkinter-compatible format
    #     self.bg_photo = ImageTk.PhotoImage(self.bg_image)
    #
    #     # Create a label to hold the background image
    #     self.bg_label = tk.Label(self.root, image=self.bg_photo)
    #     self.bg_label.place(relwidth=1, relheight=1)

    def add_image(self, path,*,size,position):
        """
        Adds an image to a Tkinter root or frame.

        Parameters:
            root (tk.Widget): The parent widget (e.g., root or frame).
            path (str): Path to the image file.
            size (tuple, optional): Size of the image as (width, height). Default is None (no resizing).
            position (tuple): Position to place the image as (x, y). Default is (0, 0).

        Returns:
            tk.Label: The Label widget containing the image.
        """
        try:
            # Open the image
            img = Image.open(path)
            # Resize the image if size is provided
            if size:
                img = img.resize(size)
            # Convert the image to a PhotoImage
            self.photo = ImageTk.PhotoImage(img)
            # Create a label to hold the image
            self.label = tk.Label(self.home_frame, image=self.photo)
            self.label.image = self.photo  # Keep a reference to avoid garbage collection
            # Place the label at the specified position
            self.label.place(x=position[0], y=position[1])
            return self.label
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def create_button(self, parent, text, command, font_size, bg_color, fg_color):
        button = tk.Button(parent, text=text, font=('Helvetica', font_size), bg=bg_color, fg=fg_color,
                               relief="ridge",
                               width=11, height=1, command=command)
        return button
    def create_button1(self, parent, text, command, font_size, bg_color, fg_color,width):
        button = tk.Button(parent, text=text, font=('Helvetica', font_size), bg=bg_color, fg=fg_color,
                            relief="ridge",
                            width=11, height=1, command=command)
        return button
        # Admin Login (Protected by email verification)
    def admin_login(self):
        self.clear_frame()
        # self.apply_background2
        self.apply_background(self.root)
        self.root.title("Admin Login")
        self.home_frame = tk.Frame(self.root,relief= "raised")
        # Load the background image
        self.bg1_image = Image.open("C:/Users/Ruqsan/Desktop/Temporary files/line.jpg")  # Replace with your image path
        self.bg1_image = self.bg1_image.resize((700, 400))
        self.bg1_photo = ImageTk.PhotoImage(self.bg1_image)

        # Create a Label to hold the image
        self.bg1_label = tk.Label(self.home_frame, image=self.bg1_photo)
        self.bg1_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.home_frame.place(x=300, y=125, width=700, height=400)
        # Middle vertical separator
        separator = ttk.Separator(self.home_frame, orient="vertical")
        separator.place(x=300, y=0, relheight=1)
        tk.Label(self.home_frame, text="Admin Login", font=('Times New Roman', 18),fg="white",bg="#224980",relief="ridge").place(x=417,y=78)
        tk.Label(self.home_frame, text="Enter verification code sent to your email:",font=('Times New Roman', 16),fg="white",bg="#224980",relief="ridge").place(x=324,y=128)
        # Add an image with specified parameters
        self.add_image("C:/Users/Ruqsan/Downloads/DALL·E 2024-12-07 15.26.57 - A futuristic scene featuring a group of sleek, high-tech Autobots with a central board that prominently displays the words 'Admin Only' in glowing fut.jpg",size=(220,300),position=(42,50))

        self.code_entry = tk.Entry(self.home_frame,width=11,              # Width in characters
    font=("Helvetica", 14), # Font and size
    bg="#1e1846",         # Background color
    fg="Cyan",          # Text color
    bd=5,                   # Border width
    relief="sunken")
        self.code_entry.place(x=417,y=168)

            # Send verification code
        self.verification_code = send_verification_code('admin_email@example.com')
        self.create_button(self.home_frame, "Submit", self.verify_admin, 18, "#224980", "#1abc9c").place(x=400,y=208)
        # # Load the image using Pillow
        # image_path = "C:/Users/Ruqsan/Desktop/Temporary files/personnage-cybersecurite.png"  # Replace with your image path
        # self.image = Image.open(image_path)
        # self.image = self.image.resize((450,450))  # Resize the image (optional)
        # self.tk_image = ImageTk.PhotoImage(self.image)
        #
        # # Create a label to display the image
        # self.label = tk.Label(self.root, image=self.tk_image, relief="raised")
        # self.label.place(x=180, y=95)
        # self.display_image(r"C:/Users/Ruqsan/Desktop/Temporary files/code.jpg", image_position=(580,110),size=(75, 75))


    def verify_admin(self):
        entered_code = self.code_entry.get()

        if entered_code == str(self.verification_code):
            self.admin_panel(self.root)
        else:
            messagebox.showerror("Error", "Incorrect verification code!")

    # Admin Panel
    def admin_panel(self,root):
        self.clear_frame()
        # self.apply_background(self.admin_panel)
        self.root.title("Admin Panel")
        self.apply_background(self.admin_panel)
        self.home_frame = tk.Frame(self.root)
        # Load the background image
        self.bg1_image = Image.open("C:/Users/Ruqsan/Desktop/Temporary files/line.jpg")  # Replace with your image path
        self.bg1_image = self.bg1_image.resize((700, 400))
        self.bg1_photo = ImageTk.PhotoImage(self.bg1_image)

        # Create a Label to hold the image
        self.bg1_label = tk.Label(self.home_frame, image=self.bg1_photo)
        self.bg1_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.home_frame.place(x=300, y=125, width=700, height=400)
        # Middle vertical separator
        separator = ttk.Separator(self.home_frame, orient="vertical")
        separator.place(x=300, y=0, relheight=1)
        self.home_frame.config(bg="#567790",bd=0)
        self.home_frame.place(x=300, y=125)
        tk.Label(self.home_frame, text="Admin Panel", font=('Times New Roman', 18),fg="white",bg="#224980").place(x=470,y=50)
        # tk.Button(self.home_frame, text="Add Info", width=20, command=self.add_info).pack(pady=10)
        self.create_button(self.home_frame, "Add Info", self.add_info, 18, "#224980", "#1abc9c").place(x=450,y=170)
        # tk.Button(self.root, text="Attendance", width=20, command=self.attendance_frame).pack(pady=10)
        self.create_button(self.home_frame, "Attendance", self.attendance_frame, 18, "#224980", "#1abc9c").place(x=450,y=290)
        self.add_image("C:/Users/Ruqsan/Desktop/Temporary files/lobby.png",size=(220,300),position=(42,50))
        self.add_image("C:/Users/Ruqsan/Desktop/Temporary files/add_student.png",size=(30,30),position=(379,180))
        self.add_image("C:/Users/Ruqsan/Desktop/Temporary files/attendance.jpg",size=(30,30),position=(379,300))

    def add_info(self):
        self.clear_frame()
        self.root.title("Add Info")
        self.apply_background(self.add_info)
        self.home_frame = tk.Frame(self.root)
        # Load the background image
        self.bg1_image = Image.open("C:/Users/Ruqsan/Desktop/Temporary files/line.jpg")  # Replace with your image path
        self.bg1_image = self.bg1_image.resize((800, 520))
        self.bg1_photo = ImageTk.PhotoImage(self.bg1_image)

        # Create a Label to hold the image
        self.bg1_label = tk.Label(self.home_frame, image=self.bg1_photo)
        self.bg1_label.place(x=0, y=0)
        # Middle vertical separator
        separator = ttk.Separator(self.home_frame, orient="vertical")
        separator.place(x=400, y=0, relheight=1)
        self.home_frame.config(bg="#567790", bd=1)
        self.home_frame.place(x=260, y=80, width=800, height=520)



        # tk.Label(self.home_frame, text="Add Student",font=('Times New Roman', 24),fg="white",bg="#224980").pack(pady=2)
        tk.Label(self.home_frame, text="ID",font=('Times New Roman', 18),fg="white",bg="#224980").place(x=20,y=270)
        self.student_id_entry = tk.Entry(self.home_frame,width=26,font=("Helvetica", 12),bg="#0f1340",fg="Cyan",bd=5,relief="sunken")
        self.student_id_entry.insert(0,"Eg:RT/TCT/21/15")
        self.student_id_entry.place(x=140,y=270)
        tk.Label(self.home_frame, text="Name",font=('Times New Roman', 18),fg="white",bg="#224980").place(x=20,y=340)
        self.name_entry = tk.Entry(self.home_frame,width=26,              # Width in characters
    font=("Helvetica", 12), # Font and size
    bg="#0f1340",         # Background color
    fg="Cyan",          # Text color
    bd=5,                   # Border width
    relief="sunken")
        self.name_entry.insert(0, "Eg:ABC DIAS")
        self.name_entry.place(x=140,y=340)
        tk.Label(self.home_frame, text="Department",font=('Times New Roman', 18),fg="white",bg="#224980").place(x=20,y=410)
        # self.attendance_dept_entry = tk.Entry(self.root)
# add image
        self.add_image("C:/Users/Ruqsan/Downloads/design-01jej5y9nr-1733635890.jpg",size=(190,190),position=(110,35))

        self.Selected_opt = tk.StringVar(self.home_frame)
        self.Selected_opt.set("Select a department")
        options = ["TCT", "FDT", "TV-PO", "TV-PR", "ECT", "FASHION", "COSMO", "EM"]
        self.attendance_dept_entry = tk.OptionMenu(self.home_frame, self.Selected_opt, *options)
        self.attendance_dept_entry.place(x=230,y=410)
        # customize option menu
        # Customize the button of the OptionMenu
        self.attendance_dept_entry.config(bg="#0f1340", fg="white", font=("Times New Roman", 12), relief="groove",width=14)

        # Access the Menu inside OptionMenu for customization
        self.menu = tk.OptionMenu(self.home_frame,self.Selected_opt, *options)
        self.menu.config(bg="lightyellow", fg="black", font=("Times New roman", 10))
        # tk.Button(self.root, text="Add Student", command=self.check).pack(pady=10)
        self.create_button1(self.home_frame, "Add Student", self.check, 15,  "#224980", "#1abc9c",7).place(x=130,y=470)

        # tk.Button(self.root, text="Show Entries", command=self.display_S).pack(pady=10)
        self.create_button1(self.home_frame, "Show Entries", self.display_S, 15, "#224980", "#1abc9c",7).place(x=450,y=45)

        # tk.Button(self.root, text="Delete", command=self.delete_record).pack(pady=10)
        self.create_button1(self.home_frame, "Delete", self.delete_record, 15,  "#224980", "red",7).place(x=630, y=45)

        tk.Button(self.root, text="Attendance", width=11, command=self.attendance_frame,font =('Helvetica',18), bg="#224980", fg= "black").place(x=16, y=33)
        # self.create_button(self.root, "Attendance", self.attendance_frame, 18, "#16a085", "#1abc9c").place(x=16, y=33)


    def display_S(self):

        tree_frame = tk.Frame(self.root)
        tree_frame.place(x=725, y=200, width=280, height=370)
        self.tv = ttk.Treeview(tree_frame, column=(1, 2, 3),height=20)

        for item in self.tv.get_children():
            self.tv.delete(item)
        # self.cur.execute('SELECT * FROM student ')
        # self.cur.fetchall()
        for row in self.db.display_St():
            self.tv.insert("", 'end', values=row)

        self.tv.heading("1", text="Student_ID")
        self.tv.column("1", width=80)
        self.tv.heading("2", text="Name")
        self.tv.column("2", width=120)
        self.tv.heading("3", text="Department")
        self.tv.column("3", width=80)
        self.tv['show'] = 'headings'
        self.tv.pack()
        self.tv.bind("<ButtonRelease-1>", self.get_data)

    def get_data(self, event=None):
        # Get the selected row
        selected_row = self.tv.focus()
        data = self.tv.item(selected_row)
        global row
        row = data["values"]
        print(row)

    def delete_record(self):
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame = ttk.Treeview(self.tree_frame, column=(1, 2, 3))
        self.tree_frame.place(x=160, y=330, width=1000, height=500)

        selected = self.tv.selection()
        if selected:
            item_id = selected[0]
            student_id = self.tv.item(item_id, 'values')[0]
            confirm = messagebox.askyesno("Delete",
                                          f"Are you sure you want to delete record with Student_ID{student_id}?")
            if confirm:
                try:
                    self.cur.execute("DELETE FROM student WHERE Student_ID=?", (student_id,))
                    self.con.commit()
                    self.tree_frame.delete(item_id)
                except Exception as e:
                    messagebox.showerror("Deleted", f"Record{student_id} deleted successfully:{e}")

                    # self.display_S()
        else:
            messagebox.showwarning("Selected Record", "Please select a record to delete")

    def check(self):
        self.root = root
        # self.clear_frame()
        self.check = tk.Tk()
        self.check.title("Check Window")
        self.check.geometry("200x100+650+330")
        self.label = tk.Label(self.check, text="Pls Check Student Details", font=('Times New Roman', 18)).pack(pady=20)

        # Submit button to trigger final submission
        self.submit_button = tk.Button(self.check, text="Submit", command=self.add_student)
        self.submit_button.pack(pady=5)

    # Mark Attendance Section
    def attendance_frame(self):
        self.clear_frame()
        self.apply_background(self.attendance_frame)
        self.root.title("Attendance Frame")
        self.home_frame = tk.Frame(self.root)
        # Load the background image
        self.bg1_image = Image.open("C:/Users/Ruqsan/Desktop/Temporary files/line.jpg")  # Replace with your image path
        self.bg1_image = self.bg1_image.resize((800, 520))
        self.bg1_photo = ImageTk.PhotoImage(self.bg1_image)

        # Create a Label to hold the image
        self.bg1_label = tk.Label(self.home_frame, image=self.bg1_photo)
        self.bg1_label.place(x=0, y=0)
        # Middle vertical separator
        separator = ttk.Separator(self.home_frame, orient="vertical")
        separator.place(x=400, y=0, relheight=1)
        self.home_frame.config(bg="#567790", bd=1)
        self.home_frame.place(x=260, y=80, width=800, height=520)
        # tk.Label(self.home_frame, text="Mark Attendance",fg="white",bg="#224980").pack(pady=20)
        self.add_image("C:/Users/Ruqsan/Downloads/freepik-export-20241209174155WCgT.jpeg",size=(190,190),position=(100,35))
        tk.Label(self.home_frame, text="Date",font=('Times New Roman', 18),fg="white",bg="#224980").place(x=45,y=270)
        self.create_button1(self.home_frame, "Select Date", self.show_date, 15, "#224980", "#1abc9c", 7).place(x=200, y=270)

        tk.Label(self.home_frame, text="Module",fg="white",bg="#224980",font=('Times New Roman', 18)).place(x=45,y=350)
        self.module_entry = tk.Entry(self.home_frame,width=13,              # Width in characters
        font=("Helvetica", 13), # Font and size
        bg="#0f1340",         # Background color
        fg="Cyan",          # Text color
        bd=5,                   # Border width
        relief="sunken")
        self.module_entry.insert(0,"Eg:I64T001M22")
        self.module_entry.place(x=200,y=350)

        tk.Label(self.home_frame, text="Department",fg="white",bg="#224980",font=('Times New Roman', 18)).place(x=45,y=430)
        options = ["TCT", "FDT", "TV-PO", "TV-PR", "ECT", "FDT", "COSMO", "EM"]
        self.Selected_opt = tk.StringVar(self.home_frame)
        self.Selected_opt.set("Select A Department")
        self.attendance_dept_entry = tk.OptionMenu(self.home_frame, self.Selected_opt, *options)
        self.attendance_dept_entry.config(bg="#224980", fg="#1abc9c", font=("Times New Roman", 9), relief="groove",width=16,height=1)
        self.attendance_dept_entry.place(x=200,y=430)


        self.create_button1(self.home_frame, "Load Students", self.load_students, 15, "#224980", "#1abc9c", 7).place(x=450, y=45)
        self.create_button1(self.home_frame, "Mark", self.mark_attendance, 15, "#224980", "#0f143a", 7).place(x=630, y=45)
        tk.Button(self.root, text="Add Info",width =11, command=self.add_info,bg="#224980", fg= "black",font =('Times New Roman',18)).place(x=16, y=33)
        self.create_button1(self.home_frame, "Show Entries", self.display_att, 15, "#224980", "#1abc9c", 7).place(x=450, y=110)
        self.create_button1(self.home_frame, "Delete", self.delete_att, 15, "#224980", "red", 7).place(x=630, y=110)

    def show_date(self):
     # Create the main window
        root = tk.Tk()
        root.title("Tkinter Calendar Example")
        root.geometry("200x350+120+230")
         # Create a Calendar widget

        self.cal = Calendar(root, selectmode="day", year=2024, month=12, day=8)
        self.cal.pack(pady=20)
        # Add a button to show the selected date
        btn_show = tk.Button(root, text="Get Selected Date", command=self.cursor,bg="#224980", fg= "#1abc9c",font =('Times New Roman',14))
        btn_show.pack(pady=10)
    # def show_date(self):
    #     # Create the main window
    #     root = tk.Tk()
    #     root.title("Select Date")
    #     # Create a Label to act as a container
    #     label_container1 = tk.Label(root, bg="lightblue", relief="solid", bd=2)
    #     label_container1.pack(padx=20, pady=20)


    def cursor(self):
        self.selected_date = self.cal.get_date()
        messagebox.showinfo("Selected Date", f"You selected: {self.selected_date}")




    def display_att(self):

        # root_1 = tk.Tk()
        # root_1.geometry("365x230+230+80")
        # root_1.title("Attendance Entries")
        tree_frame = tk.Frame(self.home_frame)
        tree_frame.place(x=420, y=175, width=365, height=230)
        self.tv = ttk.Treeview(tree_frame, column=(1, 2, 3, 4, 5, 6))

        for item in self.tv.get_children():
            self.tv.delete(item)
        # self.cur.execute('SELECT * FROM student ')
        # self.cur.fetchall()
        for row in self.db.display_att():
            self.tv.insert("", 'end', values=row)

        self.tv.heading("1", text="NO")
        self.tv.column("1", width=30)
        self.tv.heading("2", text="Date")
        self.tv.column("2", width=70)
        self.tv.heading("3", text="Module")
        self.tv.column("3", width=60)
        self.tv.heading("4", text="Department")
        self.tv.column("4", width=80)
        self.tv.heading("5", text="Student_ID")
        self.tv.column("5", width=65)
        self.tv.heading("6", text="Status")
        self.tv.column("6", width=50)
        self.tv['show'] = 'headings'
        self.tv.pack()
        self.tv.bind("<ButtonRelease-1>", self.get_data)

    def get_data(self, event=None):
        # Get the selected row
        selected_row = self.tv.focus()
        data = self.tv.item(selected_row)
        global row
        row = data["values"]
        print(row)

    def delete_att(self):
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame = ttk.Treeview(self.tree_frame, column=(1, 2, 3, 4, 5, 6))
        self.tree_frame.place(x=-150, y=380, width=1500, height=500)

        selected = self.tv.selection()
        if selected:
            item_id = selected[0]
            NO = self.tv.item(item_id, 'values')[0]
            confirm = messagebox.askyesno("Delete",
                                          f"Are you sure you want to delete record with NO {NO}?")
            if confirm:
                try:
                    self.cur.execute("DELETE FROM attendance WHERE NO=?", (NO,))
                    self.con.commit()
                    self.tree_frame.delete(item_id)
                except Exception as e:
                    messagebox.showerror("Deleted", f"Record{NO} deleted successfully:{e}")

                    # self.display_S()
        else:
            messagebox.showwarning("Selected Record", "Please select a record to delete")

    def load_students(self):
        department = self.Selected_opt.get()
        students = self.db.get_students_by_department(department)

        # Create a new window
        new_window = tk.Toplevel(self.home_frame)
        new_window.title("Students List")
        new_window.geometry("500x600")  # Set the size of the new window
        new_window.configure(bg="#3b216b")  # Set background color

        self.student_checkboxes = []  # Clear previous checkboxes

        y_offset = 20  # Initial y-coordinate for the first student
        for student in students:
            Student_ID, name = student
            var = tk.IntVar()

            # Store the student information and checkbox variable for later use
            self.student_checkboxes.append((student, var))

            # Create a frame for each student
            student_frame = tk.Frame(new_window, bd=2, relief="ridge")
            student_frame.place(x=20, y=y_offset, width=460, height=50)
            # Create a Checkbutton inside the frame
            tk.Checkbutton(
                student_frame,
                text=f"{name} ({Student_ID})",
                variable=var,
                bg="white",
                fg="#224980",
                font=("Times New Roman", 12)
            ).pack(anchor="w", padx=5, pady=5)

            # Increment y_offset to stack the subsequent frames
            y_offset += 60  # Adjust spacing between frames

    def mark_attendance(self):
        try:
            date = self.selected_date
            module = self.module_entry.get()
            department = self.Selected_opt.get()
            status = "Present" if self.student_checkboxes else "Absent"

            Student_id = self.student_checkboxes
            if date and module and department and Student_id:
                for student, checkbox_var in self.student_checkboxes:
                    # Check if the checkbox is selected (checked)
                    if checkbox_var.get() == 1:
                        status = "Present"
                    else:
                        status = "Absent"
                    Student_id, name = student  # Unpack the student details
                    # Insert attendance record into the database for each selected student
                    self.db.mark_attendance(date, module, department, status, Student_id)

                messagebox.showinfo("Success", "Attendance added successfully")
            else:
                messagebox.showerror("Error", "All fields are required!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Incorrect Information")

    # Add Student Function
    def add_student(self):
        try:
            student_id = self.student_id_entry.get()
            name = self.name_entry.get()
            # department = self.attendance_dept_entry.get()
            department = self.Selected_opt.get()
            if student_id and name and department:
                self.db.add_student(student_id, name, department)
                messagebox.showinfo("Success", "Student added successfully")
            else:
                messagebox.showerror("Error", "All fields are required!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Student_Id already Exists")

    # Utility to clear frames
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Main Application
if __name__ == "__main__":
    root: Tk = tk.Tk()
    app = AttendanceApp(root)
try:
    root.mainloop()
except KeyboardInterrupt:
    print("Program Interrupted")

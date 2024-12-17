import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import Calendar
from tkinter import ttk

# Function to load data from an SQLite database file
def load_data_from_db(db_path, table_name='attendance'):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    try:
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y', errors='coerce')  # Parse dates
        df['Status'] = df['Status'].str.strip().str.title()  # Normalize Status column
    except Exception as e:
        messagebox.showerror("Error", f"Failed to parse data: {e}")
    conn.close()
    return df

# Function for student attendance analysis by date range
def attendance_by_student(df, student_id, start_date, end_date):
    start_date = pd.to_datetime(start_date, errors='coerce')
    end_date = pd.to_datetime(end_date, errors='coerce')

    if pd.isnull(start_date) or pd.isnull(end_date):
        messagebox.showerror("Error", "Invalid date format!")
        return None

    student_data = df[(df['Student_ID'] == student_id) &
                      (df['Date'] >= start_date) & (df['Date'] <= end_date)]

    if student_data.empty:
        messagebox.showinfo("No Data", "No records found for the specified student and date range.")
        return None

    status_count = student_data['Status'].value_counts()
    present = status_count.get('Present', 0)
    absent = status_count.get('Absent', 0)
    total_days = present + absent
    attendance_percentage = (present / total_days) * 100 if total_days > 0 else 0
    return {
        'Present': present,
        'Absent': absent,
        'Total_Days': total_days,
        'Attendance_Percentage': attendance_percentage,
        'Entries': student_data[['Date', 'Status']]
    }

# Function for module-based attendance analysis by student ID
def attendance_by_module(df, student_id, module_name):
    student_module_data = df[(df['Student_ID'] == student_id) & (df['Module'] == module_name)]
    if student_module_data.empty:
        messagebox.showinfo("No Data", "No records found for the specified student and module.")
        return None

    status_count = student_module_data['Status'].value_counts()
    present = status_count.get('Present', 0)
    absent = status_count.get('Absent', 0)
    total_days = present + absent
    attendance_percentage = (present / total_days) * 100 if total_days > 0 else 0
    return {
        'Module': module_name,
        'Present': present,
        'Absent': absent,
        'Total_Days': total_days,
        'Attendance_Percentage': attendance_percentage,
        'Entries': student_module_data[['Date', 'Status']]
    }

# Load database function
def load_database():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Database files", "*.db")])
    if file_path:
        try:
            df = load_data_from_db(file_path)
            messagebox.showinfo("Success", "Database loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load database: {e}")

# Student Analysis button action
def perform_student_analysis():
    student_id = student_id_entry.get().strip()
    start_date = cal_start.get_date()  # Calendar widget start date
    end_date = cal_end.get_date()      # Calendar widget end date
    result = attendance_by_student(df, student_id, start_date, end_date)
    if result:
        display_text.delete(1.0, tk.END)
        display_text.insert(tk.END, f"Present: {result['Present']}\n")
        display_text.insert(tk.END, f"Absent: {result['Absent']}\n")
        display_text.insert(tk.END, f"Total Days: {result['Total_Days']}\n")
        display_text.insert(tk.END, f"Attendance Percentage: {result['Attendance_Percentage']:.2f}%\n")
        display_text.insert(tk.END, f"Entries:\n{result['Entries']}\n")

# Module-Based Analysis button action
def perform_module_analysis():
    student_id = module_student_id_entry.get().strip()
    module_name = module_name_entry.get()
    result = attendance_by_module(df, student_id, module_name)
    if result:
        display_text.delete(1.0, tk.END)
        display_text.insert(tk.END, f"Module: {result['Module']}\n")
        display_text.insert(tk.END, f"Present: {result['Present']}\n")
        display_text.insert(tk.END, f"Absent: {result['Absent']}\n")
        display_text.insert(tk.END, f"Total Days: {result['Total_Days']}\n")
        display_text.insert(tk.END, f"Attendance Percentage: {result['Attendance_Percentage']:.2f}%\n")
        display_text.insert(tk.END, f"Entries:\n{result['Entries']}\n")

# Main GUI setup
root = tk.Tk()
root.title("Attendance Analysis Tool")
root.geometry("700x600")

# Database Load Button
load_button = tk.Button(root, text="Load Database", command=load_database)
load_button.pack(pady=10)

# Student Analysis Frame
student_frame = tk.Frame(root)
student_frame.pack(pady=5)
tk.Label(student_frame, text="Student ID:").grid(row=0, column=0)
student_id_entry = tk.Entry(student_frame, width=20)
student_id_entry.grid(row=0, column=1)

tk.Label(student_frame, text="Start Date:").grid(row=0, column=2)
cal_start = Calendar(student_frame, selectmode='day', date_pattern='yyyy-mm-dd')
cal_start.grid(row=0, column=3, padx=5)

tk.Label(student_frame, text="End Date:").grid(row=0, column=4)
cal_end = Calendar(student_frame, selectmode='day', date_pattern='yyyy-mm-dd')
cal_end.grid(row=0, column=5, padx=5)

student_button = tk.Button(student_frame, text="Student Analysis", command=perform_student_analysis)
student_button.grid(row=0, column=6, padx=5)

# Module-Based Analysis Frame
module_frame = tk.Frame(root)
module_frame.pack(pady=5)
tk.Label(module_frame, text="Student ID:").grid(row=0, column=0)
module_student_id_entry = tk.Entry(module_frame, width=20)
module_student_id_entry.grid(row=0, column=1)
tk.Label(module_frame, text="Module Name:").grid(row=0, column=2)
module_name_entry = tk.Entry(module_frame, width=15)
module_name_entry.grid(row=0, column=3)
module_button = tk.Button(module_frame, text="Module Analysis", command=perform_module_analysis)
module_button.grid(row=0, column=4, padx=5)

# Display Area for Results
display_text = tk.Text(root, height=20, width=80)
display_text.pack(pady=10)

root.mainloop()

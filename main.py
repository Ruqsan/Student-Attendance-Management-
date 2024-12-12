import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Attendance Analysis")
        self.root.geometry("600x400")

        # Title
        title_label = tk.Label(root, text="Student Attendance Analysis", font=("Arial", 16))
        title_label.pack(pady=10)

        # Load File Button
        load_button = tk.Button(root, text="Load Attendance Database", command=self.load_file)
        load_button.pack(pady=10)

        # Table for displaying the report
        self.tree = ttk.Treeview(root, columns=(
        "Student ID", "Total Days", "Days Present", "Days Absent", "Absent Percentage"), show="headings")
        self.tree.heading("Student ID", text="Student ID")
        self.tree.heading("Total Days", text="Total Days")
        self.tree.heading("Days Present", text="Days Present")
        self.tree.heading("Days Absent", text="Days Absent")
        self.tree.heading("Absent Percentage", text="Absent %")
        self.tree.pack(fill="both", expand=True)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("SQLite Database Files", "*.db")])
        if not file_path:
            return

        try:
            # Connect to SQLite database
            conn = sqlite3.connect(file_path)
            query = "SELECT * FROM attendance"
            attendance_data = pd.read_sql_query(query, conn)
            conn.close()

            # Generate the report
            report = attendance_data.groupby("Student_ID").apply(
                lambda x: pd.Series({
                    "Total Days": len(x),
                    "Days Present": (x["Status"] == "Present").sum(),
                    "Days Absent": (x["Status"] == "Absent").sum(),
                })
            ).reset_index()

            # Calculate absent percentage
            report["Absent Percentage"] = (report["Days Absent"] / report["Total Days"]) * 100

            # Clear any previous data in the table
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert the report data into the table
            for _, row in report.iterrows():
                self.tree.insert("", "end", values=(
                row["Student_ID"], row["Total Days"], row["Days Present"], row["Days Absent"],
                f"{row['Absent Percentage']:.2f}"))

            # Inform the user
            messagebox.showinfo("Success", "Attendance data loaded successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load database. Error: {e}")


# Initialize the GUI application
root = tk.Tk()
app = AttendanceApp(root)
root.mainloop()
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2

def run_query(query, parameters=()):
    conn = psycopg2.connect(dbname="studentdb", user="postgres", password="ayush1", host="localhost", port="5432")
    cur = conn.cursor()
    query_result = None
    try:
        cur.execute(query, parameters)
        if query.lower().startswith("select"):
            query_result = cur.fetchall()
        conn.commit()
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        cur.close()
        conn.close()
    return query_result

def refresh_treeview():
    for item in tree.get_children():
        tree.delete(item)
    records = run_query("SELECT * FROM students;")
    for record in records:
        tree.insert('', END, values=record)

def create_table():
    query = "CREATE TABLE IF NOT EXISTS students(student_id SERIAL PRIMARY KEY, name TEXT, address TEXT, age INT, number TEXT);"
    run_query(query)
    messagebox.showinfo("Information", "Table created successfully.")
    refresh_treeview()

def insert_data():
    query = "INSERT INTO students(name, address, age, number) VALUES (%s, %s, %s, %s)"
    parameters = (name_entry.get(), address_entry.get(), age_entry.get(), number_entry.get())
    run_query(query, parameters)
    messagebox.showinfo("Information", "Data inserted successfully.")
    refresh_treeview()

def update_data():
    selected_item = tree.selection()[0]
    student_id = tree.item(selected_item)['values'][0]
    query = "UPDATE students SET name = %s, address = %s, age = %s, number = %s WHERE student_id = %s"
    parameters = (name_entry.get(), address_entry.get(), age_entry.get(), number_entry.get(), student_id)
    run_query(query, parameters)
    messagebox.showinfo("Information", "Data updated successfully.")
    refresh_treeview()

def delete_data():
    selected_item = tree.selection()[0]
    student_id = tree.item(selected_item)['values'][0]
    query = "DELETE FROM students WHERE student_id = %s"
    parameters = (student_id,)
    run_query(query, parameters)
    messagebox.showinfo("Information", "Data deleted successfully.")
    refresh_treeview()

# ========== UI SETUP ==========
root = Tk()
root.title("Student Management System")
root.geometry("700x500")
root.configure(bg="#f0f4f7")

style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview", 
                background="#f7fafc", 
                foreground="black", 
                rowheight=25, 
                fieldbackground="#f7fafc", 
                font=("Segoe UI", 10))
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

style.configure("TButton", font=("Segoe UI", 9, "bold"), padding=5)
style.configure("TLabel", font=("Segoe UI", 10))

frame = LabelFrame(root, text="Student Data", padx=10, pady=10, bg="#e2e8f0", font=("Segoe UI", 10, "bold"))
frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

Label(frame, text="Name:", bg="#e2e8f0").grid(row=0, column=0, pady=2, sticky="w")
name_entry = Entry(frame, font=("Segoe UI", 10))
name_entry.grid(row=0, column=1, pady=2, sticky="ew")

Label(frame, text="Address:", bg="#e2e8f0").grid(row=1, column=0, pady=2, sticky="w")
address_entry = Entry(frame, font=("Segoe UI", 10))
address_entry.grid(row=1, column=1, pady=2, sticky="ew")

Label(frame, text="Age:", bg="#e2e8f0").grid(row=2, column=0, pady=2, sticky="w")
age_entry = Entry(frame, font=("Segoe UI", 10))
age_entry.grid(row=2, column=1, pady=2, sticky="ew")

Label(frame, text="Phone Number:", bg="#e2e8f0").grid(row=3, column=0, pady=2, sticky="w")
number_entry = Entry(frame, font=("Segoe UI", 10))
number_entry.grid(row=3, column=1, pady=2, sticky="ew")

frame.columnconfigure(1, weight=1)

button_frame = Frame(root, bg="#f0f4f7")
button_frame.grid(row=1, column=0, pady=5, sticky="ew")

ttk.Button(button_frame, text="Create Table", command=create_table).grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="Insert Data", command=insert_data).grid(row=0, column=1, padx=5)
ttk.Button(button_frame, text="Update Data", command=update_data).grid(row=0, column=2, padx=5)
ttk.Button(button_frame, text="Delete Data", command=delete_data).grid(row=0, column=3, padx=5)

tree_frame = Frame(root, bg="#f0f4f7")
tree_frame.grid(row=2, column=0, pady=10, sticky="nsew")
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse")
tree.pack(fill=BOTH, expand=True)

tree_scroll.config(command=tree.yview)

tree['columns'] = ("student_id", "name", "address", "age", "number")
tree.column("#0", width=0, stretch=NO)
tree.column("student_id", anchor=CENTER, width=80)
tree.column("name", anchor=W, width=140)
tree.column("address", anchor=W, width=140)
tree.column("age", anchor=CENTER, width=50)
tree.column("number", anchor=W, width=120)

tree.heading("student_id", text="ID", anchor=CENTER)
tree.heading("name", text="Name", anchor=CENTER)
tree.heading("address", text="Address", anchor=CENTER)
tree.heading("age", text="Age", anchor=CENTER)
tree.heading("number", text="Phone Number", anchor=CENTER)

refresh_treeview()
root.mainloop()

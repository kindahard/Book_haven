import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

class DatabaseConnection:
    def __init__(self):
        self.server = r'.\SQLEXPRESS'
        self.database = 'Book_haven'
        self.username = 'flask_book_user'
        self.password = '123456'
        
    def get_connection(self):
        try:
            conn_str = (
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={self.server};'
                f'DATABASE={self.database};'
                f'UID={self.username};'
                f'PWD={self.password};'
            )
            return pyodbc.connect(conn_str)
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect:\n{str(e)}")
            return None

class LoginWindow:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.root.title("Library Management System - Login")
        self.root.geometry("400x300")
        self.db = DatabaseConnection()
        self.create_login_ui()
        
    def create_login_ui(self):
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(fill=tk.X)
        tk.Label(header, text="Library Management System", font=("Arial", 18, "bold"), 
                bg="#2c3e50", fg="white").pack(pady=10)
        tk.Label(header, text="Staff Login", font=("Arial", 12), 
                bg="#2c3e50", fg="#ecf0f1").pack()
        
        form = tk.Frame(self.root, bg="#ecf0f1")
        form.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        tk.Label(form, text="Email:", font=("Arial", 11), bg="#ecf0f1").grid(row=0, column=0, sticky=tk.W, pady=10)
        self.email_entry = tk.Entry(form, font=("Arial", 11), width=25)
        self.email_entry.grid(row=0, column=1, pady=10)
        
        tk.Label(form, text="Password:", font=("Arial", 11), bg="#ecf0f1").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.password_entry = tk.Entry(form, font=("Arial", 11), width=25, show="*")
        self.password_entry.grid(row=1, column=1, pady=10)
        
        tk.Button(form, text="Login", command=self.authenticate, bg="#27ae60", fg="white", 
                 font=("Arial", 11, "bold"), padx=30, pady=8).grid(row=2, column=0, columnspan=2, pady=20)
        
        self.email_entry.bind('<Return>', lambda e: self.authenticate())
        self.password_entry.bind('<Return>', lambda e: self.authenticate())
        self.email_entry.focus()
        
    def authenticate(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showwarning("Login Failed", "Enter email and password")
            return
        
        conn = self.db.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT staff_id, fname, lname, role FROM staff WHERE email=? AND password=?", [email, password])
            result = cursor.fetchone()
            
            if result:
                staff_data = {'staff_id': result[0], 'fname': result[1], 'lname': result[2], 'role': result[3]}
                conn.close()
                self.root.withdraw()
                self.callback(staff_data)
            else:
                messagebox.showerror("Login Failed", "Invalid credentials")
                self.password_entry.delete(0, tk.END)
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Authentication failed: {str(e)}")
            if conn:
                conn.close()

class LibraryManagementSystem:
    def __init__(self, root, staff_data):
        self.root = root
        self.staff_data = staff_data
        self.root.title("Library Management System")
        self.root.geometry("1200x700")
        self.db = DatabaseConnection()
        
        self.permissions = {
            'Assistant': {'tables': ['member', 'reservation', 'reservation_details'], 
                         'can_add': ['member', 'reservation', 'reservation_details'], 
                         'can_edit': ['reservation', 'reservation_details'], 'can_delete': []},
            'Librarian': {'tables': ['author', 'book', 'book_copy', 'category', 'description', 'book_author', 'book_category', 'member'],
                         'can_add': ['author', 'book', 'book_copy', 'category', 'description', 'book_author', 'book_category'],
                         'can_edit': ['author', 'book', 'book_copy', 'category', 'description', 'book_author', 'book_category'],
                         'can_delete': ['book_copy', 'book_author', 'book_category']},
            'Manager': {'tables': ['author', 'book', 'book_copy', 'category', 'description', 'staff', 'member', 'reservation', 'reservation_details', 'book_author', 'book_category'],
                       'can_add': 'all', 'can_edit': 'all', 'can_delete': 'all'},
            'Technician': {'tables': ['book_copy'], 'can_add': [], 'can_edit': ['book_copy'], 'can_delete': []}
        }
        
        self.identity_columns = self.get_all_identity_columns()
        self.create_menu()
        self.create_main_layout()
        
    def get_all_identity_columns(self):
        conn = self.db.get_connection()
        if not conn:
            return {}
        identity_cols = {}
        try:
            cursor = conn.cursor()
            query = """SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
                      WHERE COLUMNPROPERTY(OBJECT_ID(TABLE_SCHEMA + '.' + TABLE_NAME), COLUMN_NAME, 'IsIdentity') = 1 
                      AND TABLE_SCHEMA = 'dbo'"""
            cursor.execute(query)
            for row in cursor.fetchall():
                if row[0] not in identity_cols:
                    identity_cols[row[0]] = []
                identity_cols[row[0]].append(row[1])
        except:
            pass
        finally:
            conn.close()
        return identity_cols
        
    def has_permission(self, action, table_name):
        role = self.staff_data['role']
        if role not in self.permissions:
            return False
        perms = self.permissions[role]
        if table_name not in perms['tables']:
            return False
        if action == 'view':
            return True
        elif action == 'add':
            return perms['can_add'] == 'all' or table_name in perms['can_add']
        elif action == 'edit':
            return perms['can_edit'] == 'all' or table_name in perms['can_edit']
        elif action == 'delete':
            return perms['can_delete'] == 'all' or table_name in perms['can_delete']
        return False
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        tables_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tables", menu=tables_menu)
        
        for label, table in [("Authors", "author"), ("Books", "book"), ("Book Copies", "book_copy"), 
                            ("Categories", "category"), ("Descriptions", "description"), ("Staff", "staff"), 
                            ("Members", "member"), ("Reservations", "reservation")]:
            if self.has_permission('view', table):
                tables_menu.add_command(label=label, command=lambda t=table: self.show_table_view(t))
        
        rel_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Relationships", menu=rel_menu)
        
        for label, table in [("Book Authors", "book_author"), ("Book Categories", "book_category"), 
                            ("Reservation Details", "reservation_details")]:
            if self.has_permission('view', table):
                rel_menu.add_command(label=label, command=lambda t=table: self.show_table_view(t))
        
        account_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Account", menu=account_menu)
        account_menu.add_command(label="Logout", command=self.logout)
        
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure?"):
            self.root.destroy()
            new_root = tk.Tk()
            LoginWindow(new_root, lambda sd: LibraryManagementSystem(new_root, sd))
            new_root.mainloop()
        
    def create_main_layout(self):
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        tk.Label(title_frame, text="Library Management System", font=("Arial", 20, "bold"), 
                bg="#2c3e50", fg="white").pack(side=tk.LEFT, padx=20, pady=15)
        tk.Label(title_frame, text=f"{self.staff_data['fname']} {self.staff_data['lname']} ({self.staff_data['role']})",
                font=("Arial", 11), bg="#2c3e50", fg="#ecf0f1").pack(side=tk.RIGHT, padx=20, pady=15)
        
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.show_welcome()
        
    def show_welcome(self):
        self.clear_content()
        tk.Label(self.content_frame, text=f"Welcome, {self.staff_data['fname']}!", 
                font=("Arial", 18, "bold")).pack(pady=30)
        tk.Label(self.content_frame, text=f"Role: {self.staff_data['role']}", 
                font=("Arial", 14)).pack(pady=10)
        
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def show_table_view(self, table_name):
        if not self.has_permission('view', table_name):
            messagebox.showerror("Access Denied", "No permission")
            return
        self.clear_content()
        
        tk.Label(self.content_frame, text=f"Manage {table_name.replace('_', ' ').title()}", 
                font=("Arial", 16, "bold")).pack(pady=10)
        
        search_frame = tk.Frame(self.content_frame)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=lambda: self.search_table(table_name),
                 bg="#9b59b6", fg="white", padx=15, pady=3).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Clear", command=lambda: self.clear_search(table_name),
                 bg="#95a5a6", fg="white", padx=15, pady=3).pack(side=tk.LEFT, padx=5)
        
        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        if self.has_permission('add', table_name):
            tk.Button(btn_frame, text="Add New", command=lambda: self.add_record(table_name),
                     bg="#27ae60", fg="white", padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        if self.has_permission('edit', table_name):
            tk.Button(btn_frame, text="Edit Selected", command=lambda: self.edit_record(table_name),
                     bg="#f39c12", fg="white", padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        if self.has_permission('delete', table_name):
            tk.Button(btn_frame, text="Delete Selected", command=lambda: self.delete_record(table_name),
                     bg="#e74c3c", fg="white", padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Refresh", command=lambda: self.show_table_view(table_name),
                 bg="#3498db", fg="white", padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        columns = self.get_table_columns(table_name)
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.load_table_data(table_name)
        self.current_table = table_name
        
    def get_table_columns(self, table_name):
        conn = self.db.get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT TOP 0 * FROM {table_name}")
            return [desc[0] for desc in cursor.description]
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []
        finally:
            conn.close()
            
    def load_table_data(self, table_name):
        conn = self.db.get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for row in rows:
                cleaned_row = [str(v).strip() if v is not None else "" for v in row]
                self.tree.insert("", tk.END, values=tuple(cleaned_row))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()
            
    def search_table(self, table_name):
        search_term = self.search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Search", "Enter search term")
            return
        
        conn = self.db.get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            columns = self.get_table_columns(table_name)
            
            search_conditions = []
            search_params = []
            for col in columns:
                if any(x in col.lower() for x in ['id', 'name', 'title', 'email', 'isbn', 'fname', 'lname']):
                    search_conditions.append(f"CAST({col} AS VARCHAR(MAX)) LIKE ?")
                    search_params.append(f"%{search_term}%")
            
            if not search_conditions:
                messagebox.showinfo("Search", "No searchable columns")
                return
            
            query = f"SELECT * FROM {table_name} WHERE {' OR '.join(search_conditions)}"
            cursor.execute(query, search_params)
            rows = cursor.fetchall()
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            if rows:
                for row in rows:
                    cleaned_row = [str(v).strip() if v is not None else "" for v in row]
                    self.tree.insert("", tk.END, values=tuple(cleaned_row))
                messagebox.showinfo("Search Results", f"Found {len(rows)} record(s)")
            else:
                messagebox.showinfo("Search Results", "No records found")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()
    
    def clear_search(self, table_name):
        self.search_entry.delete(0, tk.END)
        self.load_table_data(table_name)
            
    def add_record(self, table_name):
        if not self.has_permission('add', table_name):
            messagebox.showerror("Access Denied", "No permission")
            return
        
        columns = self.get_table_columns(table_name)
        if not columns:
            return
        
        identity_cols = self.identity_columns.get(table_name, [])
        editable_columns = [col for col in columns if col not in identity_cols]
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Add New {table_name}")
        dialog.geometry("500x600")
        
        canvas = tk.Canvas(dialog)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        entries = {}
        for idx, col in enumerate(editable_columns):
            tk.Label(scrollable_frame, text=f"{col}:", font=("Arial", 10)).grid(row=idx, column=0, sticky=tk.W, padx=10, pady=5)
            if col.lower() == 'description':
                entry = tk.Text(scrollable_frame, width=35, height=4)
            else:
                entry = tk.Entry(scrollable_frame, width=35)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entries[col] = entry
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(side="bottom", pady=20)
        
        def save():
            values = {}
            for col in editable_columns:
                if isinstance(entries[col], tk.Text):
                    values[col] = entries[col].get("1.0", tk.END).strip()
                else:
                    values[col] = entries[col].get()
            if self.insert_record(table_name, values):
                dialog.destroy()
                self.show_table_view(table_name)
        
        tk.Button(btn_frame, text="Save", command=save, bg="#27ae60", fg="white", padx=20).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy, bg="#95a5a6", fg="white", padx=20).pack(side=tk.LEFT, padx=5)
        
    def insert_record(self, table_name, values):
        conn = self.db.get_connection()
        if not conn:
            return False
        try:
            filtered_values = {col: str(val).strip() for col, val in values.items() if str(val).strip()}
            if not filtered_values:
                messagebox.showwarning("Warning", "Fill at least one field")
                return False
            
            columns = list(filtered_values.keys())
            query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({','.join(['?']*len(columns))})"
            cursor = conn.cursor()
            cursor.execute(query, list(filtered_values.values()))
            conn.commit()
            messagebox.showinfo("Success", "Record added!")
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            conn.close()
            
    def edit_record(self, table_name):
        if not self.has_permission('edit', table_name):
            messagebox.showerror("Access Denied", "No permission")
            return
        
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a record")
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        columns = self.get_table_columns(table_name)
        identity_cols = self.identity_columns.get(table_name, [])
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit {table_name}")
        dialog.geometry("500x600")
        
        canvas = tk.Canvas(dialog)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        entries = {}
        for i, col in enumerate(columns):
            tk.Label(scrollable_frame, text=f"{col}:", font=("Arial", 10)).grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            if col.lower() == 'description':
                entry = tk.Text(scrollable_frame, width=35, height=4)
                entry.insert("1.0", str(values[i]))
            else:
                entry = tk.Entry(scrollable_frame, width=35)
                entry.insert(0, str(values[i]))
            entry.grid(row=i, column=1, padx=10, pady=5)
            if col in identity_cols:
                entry.config(state='disabled')
            entries[col] = entry
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(side="bottom", pady=20)
        
        def save():
            new_values = {}
            for col in columns:
                if isinstance(entries[col], tk.Text):
                    new_values[col] = entries[col].get("1.0", tk.END).strip()
                else:
                    new_values[col] = entries[col].get()
            if self.update_record(table_name, columns[0], values[0], new_values):
                dialog.destroy()
                self.show_table_view(table_name)
        
        tk.Button(btn_frame, text="Save", command=save, bg="#27ae60", fg="white", padx=20).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy, bg="#95a5a6", fg="white", padx=20).pack(side=tk.LEFT, padx=5)
        
    def update_record(self, table_name, pk_column, pk_value, values):
        conn = self.db.get_connection()
        if not conn:
            return False
        try:
            query = f"UPDATE {table_name} SET {','.join([f'{col}=?' for col in values.keys()])} WHERE {pk_column}=?"
            cursor = conn.cursor()
            cursor.execute(query, list(values.values()) + [pk_value])
            conn.commit()
            messagebox.showinfo("Success", "Record updated!")
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            conn.close()
            
    def delete_record(self, table_name):
        if not self.has_permission('delete', table_name):
            messagebox.showerror("Access Denied", "No permission")
            return
        
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a record")
            return
        
        if not messagebox.askyesno("Confirm", "Delete this record?"):
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        columns = self.get_table_columns(table_name)
        
        conn = self.db.get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE {columns[0]}=?", [values[0]])
            conn.commit()
            messagebox.showinfo("Success", "Record deleted!")
            self.show_table_view(table_name)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    def on_login(staff_data):
        root.destroy()
        main_root = tk.Tk()
        LibraryManagementSystem(main_root, staff_data)
        main_root.mainloop()
    LoginWindow(root, on_login)
    root.mainloop()
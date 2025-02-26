import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import re
from tkinter.font import Font

class ContactMaster:
    def __init__(self, root):
        self.root = root
        self.root.title("ContactMaster - Your Digital Address Book")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        
        # Initialize styling
        self.setup_styles()
        self.contacts = []
        self.current_contacts = []
        self.selected_contact = None
        
        # Load contacts from file
        self.load_contacts()
        
        # Setup UI
        self.create_widgets()
        self.update_contact_list()
    
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.root.configure(bg='#2d2d2d')
        self.style.configure('TFrame', background='#2d2d2d')
        self.style.configure('TLabel', background='#2d2d2d', foreground='white')
        self.style.configure('TButton', background='#3d3d3d', foreground='white', 
                           borderwidth=1, font=('Helvetica', 10, 'bold'))
        self.style.map('TButton', background=[('active', '#4d4d4d')])
        self.style.configure('Treeview.Heading', background='#3d3d3d', 
                            foreground='white', font=('Helvetica', 10, 'bold'))
        self.style.configure('Treeview', background='#2d2d2d', foreground='white',
                           fieldbackground='#2d2d2d')
        self.style.configure('Search.TEntry', foreground='#2d2d2d')
        
        # Custom title font
        self.title_font = Font(family='Helvetica', size=20, weight='bold')
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="ContactMaster", 
                               font=self.title_font, foreground='#00ff99')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Search Section
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=1, column=0, sticky='ew', pady=(0, 20))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var,
                                style='Search.TEntry', width=40)
        search_entry.pack(side='left', padx=(0, 10))
        search_entry.bind('<KeyRelease>', self.update_search)
        
        search_btn = ttk.Button(search_frame, text="Search", 
                              command=self.update_search)
        search_btn.pack(side='left')
        
        # Contact List
        self.contact_tree = ttk.Treeview(main_frame, columns=('name', 'phone', 'email'),
                                       show='headings', selectmode='browse')
        self.contact_tree.grid(row=2, column=0, sticky='nsew')
        
        # Configure treeview columns
        self.contact_tree.heading('name', text='Name')
        self.contact_tree.heading('phone', text='Phone')
        self.contact_tree.heading('email', text='Email')
        self.contact_tree.column('name', width=200)
        self.contact_tree.column('phone', width=150)
        self.contact_tree.column('email', width=250)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', 
                                command=self.contact_tree.yview)
        scrollbar.grid(row=2, column=1, sticky='ns')
        self.contact_tree.configure(yscrollcommand=scrollbar.set)
        
        # Contact Details Form
        form_frame = ttk.Frame(main_frame)
        form_frame.grid(row=3, column=0, sticky='ew', pady=(20, 0))
        
        # Form fields
        fields = ['Name', 'Phone', 'Email', 'Address']
        self.entries = {}
        for i, field in enumerate(fields):
            lbl = ttk.Label(form_frame, text=f"{field}:")
            lbl.grid(row=i, column=0, padx=5, pady=2, sticky='e')
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky='w')
            self.entries[field.lower()] = entry
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, pady=(20, 0))
        
        ttk.Button(btn_frame, text="Add Contact", command=self.add_contact).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Update Contact", command=self.update_contact).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete Contact", command=self.delete_contact).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).pack(side='left', padx=5)
        
        # Status Bar
        self.status_bar = ttk.Label(self.root, text="Ready", foreground='white')
        self.status_bar.pack(side='bottom', fill='x')
        
        # Bind selection event
        self.contact_tree.bind('<<TreeviewSelect>>', self.load_contact_details)
    
    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone):
        return phone.isdigit() and len(phone) >= 10

    def add_contact(self):
        try:
            contact_data = {field: self.entries[field].get().strip() 
                           for field in ['name', 'phone', 'email', 'address']}
            
            # Validation
            if not all(contact_data.values()):
                raise ValueError("All fields are required")
            if not self.validate_phone(contact_data['phone']):
                raise ValueError("Invalid phone number format")
            if not self.validate_email(contact_data['email']):
                raise ValueError("Invalid email format")
            
            # Add contact
            self.contacts.append(contact_data)
            self.update_contact_list()
            self.save_contacts()
            self.clear_form()
            self.show_status("Contact added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_contact(self):
        if not self.selected_contact:
            messagebox.showwarning("Warning", "Please select a contact to update")
            return
        
        try:
            new_data = {field: self.entries[field].get().strip() 
                       for field in ['name', 'phone', 'email', 'address']}
            
            # Validation
            if not all(new_data.values()):
                raise ValueError("All fields are required")
            if not self.validate_phone(new_data['phone']):
                raise ValueError("Invalid phone number format")
            if not self.validate_email(new_data['email']):
                raise ValueError("Invalid email format")
            
            # Update contact
            index = self.contacts.index(self.selected_contact)
            self.contacts[index] = new_data
            self.update_contact_list()
            self.save_contacts()
            self.show_status("Contact updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_contact(self):
        if not self.selected_contact:
            messagebox.showwarning("Warning", "Please select a contact to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?"):
            self.contacts.remove(self.selected_contact)
            self.update_contact_list()
            self.save_contacts()
            self.clear_form()
            self.show_status("Contact deleted successfully!")
    
    def load_contact_details(self, event):
        selected_item = self.contact_tree.selection()
        if selected_item:
            item = self.contact_tree.item(selected_item)
            contact_name = item['values'][0]
            self.selected_contact = next(
                (c for c in self.contacts if c['name'] == contact_name), None)
            
            if self.selected_contact:
                for field, entry in self.entries.items():
                    entry.delete(0, tk.END)
                    entry.insert(0, self.selected_contact.get(field, ''))
    
    def update_search(self, event=None):
        query = self.search_var.get().lower()
        self.current_contacts = [
            c for c in self.contacts
            if query in c['name'].lower() or 
               query in c['phone'] or 
               query in c['email'].lower()
        ]
        self.update_contact_list()
    
    def update_contact_list(self):
        self.contact_tree.delete(*self.contact_tree.get_children())
        for contact in self.current_contacts:
            self.contact_tree.insert('', 'end', values=(
                contact['name'],
                contact['phone'],
                contact['email']
            ))
    
    def clear_form(self):
        self.selected_contact = None
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.contact_tree.selection_remove(self.contact_tree.selection())
    
    def show_status(self, message):
        self.status_bar.config(text=message)
        self.root.after(3000, lambda: self.status_bar.config(text="Ready"))
    
    def load_contacts(self):
        try:
            with open('contacts.json', 'r') as f:
                self.contacts = json.load(f)
            self.current_contacts = self.contacts.copy()
        except (FileNotFoundError, json.JSONDecodeError):
            self.contacts = []
            self.current_contacts = []
    
    def save_contacts(self):
        with open('contacts.json', 'w') as f:
            json.dump(self.contacts, f, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactMaster(root)
    root.mainloop()

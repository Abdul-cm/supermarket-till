import tkinter as tk
from ttkbootstrap import Style, ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
from decimal import Decimal
from datetime import datetime
from fpdf import FPDF
import os
from users import UserManager
from login_window import LoginWindow
from profile_window import ProfileWindow

class SupermarketTill:
    def __init__(self, root):
        self.root = root
        self.style = Style(theme='cosmo')
        
        # Initialize user management
        self.user_manager = UserManager()
        self.current_user = None
        
        # Initialize receipt history
        self.receipts_dir = "receipts"
        if not os.path.exists(self.receipts_dir):
            os.makedirs(self.receipts_dir)
        
        # Predefined items with prices and categories
        self.predefined_items = {
            # Fruits
            "🍎 Apple": {"price": 2.50, "category": "Fruits"},
            "🍊 Orange": {"price": 1.80, "category": "Fruits"},
            "🍌 Banana": {"price": 1.20, "category": "Fruits"},
            "🍇 Grapes": {"price": 3.50, "category": "Fruits"},
            "🍓 Strawberries": {"price": 4.00, "category": "Fruits"},
            "🥭 Mango": {"price": 3.00, "category": "Fruits"},
            "🍍 Pineapple": {"price": 4.50, "category": "Fruits"},
            "🍉 Watermelon": {"price": 6.00, "category": "Fruits"},
            "🍑 Peach": {"price": 2.00, "category": "Fruits"},
            "🥝 Kiwi": {"price": 1.50, "category": "Fruits"},
            # Vegetables
            "🍅 Tomato": {"price": 1.20, "category": "Vegetables"},
            "🥒 Cucumber": {"price": 1.00, "category": "Vegetables"},
            "🥕 Carrot": {"price": 1.50, "category": "Vegetables"},
            "🥔 Potato": {"price": 2.00, "category": "Vegetables"},
            "🧅 Onion": {"price": 1.00, "category": "Vegetables"},
            "🥬 Lettuce": {"price": 2.50, "category": "Vegetables"},
            "🥦 Broccoli": {"price": 3.00, "category": "Vegetables"},
            "🥦 Cauliflower": {"price": 3.50, "category": "Vegetables"},
            "🫑 Bell Pepper": {"price": 2.00, "category": "Vegetables"},
            "🥬 Spinach": {"price": 2.50, "category": "Vegetables"}
        }
        
        # Start the application
        self.start_application()
        
    def start_application(self):
        """Start the application flow"""
        while True:
            # Show login window
            if not self.show_login():
                break
            
            # Show main application
            if not self.show_main_window():
                break
    
    def show_login(self):
        """Show login window and return True if login successful"""
        try:
            # Ensure any old widgets are destroyed
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Create login window using the main window
            login = LoginWindow(self.root)
            
            # Run the login window
            self.root.mainloop()
            
            # Get login result
            self.current_user = login.get_result()
            
            return bool(self.current_user)
            
        except Exception as e:
            messagebox.showerror("Error", f"Login error: {str(e)}")
            return False
    
    def show_main_window(self):
        """Show main application window"""
        try:
            # Clear all widgets
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Configure main window
            self.root.title("Supermarket Till")
            # Make window responsive
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            window_width = int(screen_width * 0.8)
            window_height = int(screen_height * 0.8)
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            # Initialize variables
            self.items = []
            self.total = Decimal('0.00')
            self.vat_rate = Decimal('0.20')  # 20% VAT
            
            # Create GUI elements
            self.create_widgets()
            
            # Show profile window
            self.show_profile_window()
            
            # Start main loop
            self.root.mainloop()
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Application error: {str(e)}")
            return False
    
    def show_profile_window(self):
        """Show the profile window"""
        self.root.after(100, lambda: ProfileWindow(self.root, self.user_manager, self.current_user))
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.user_manager.logout()
            self.root.quit()
            
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        # Main container with padding
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky="nsew")
        
        # User info and logout frame
        user_frame = ttk.Frame(main_container)
        user_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        user_info = ttk.Frame(user_frame)
        user_info.pack(side=tk.RIGHT)
        
        # Get user profile information
        try:
            profile = self.user_manager.get_user_profile(self.current_user)
            if profile:
                ttk.Label(user_info, text=f"Welcome: {profile['full_name']}", 
                         font=("Arial", 10, "bold")).pack(side=tk.RIGHT, padx=5)
                ttk.Label(user_info, text=f"({profile['email']})", 
                         font=("Arial", 9)).pack(side=tk.RIGHT, padx=5)
            else:
                ttk.Label(user_info, text=f"Welcome: {self.current_user}", 
                         font=("Arial", 10, "bold")).pack(side=tk.RIGHT, padx=5)
        except Exception as e:
            print(f"Error displaying user info: {e}")
            ttk.Label(user_info, text=f"Welcome: {self.current_user}", 
                     font=("Arial", 10, "bold")).pack(side=tk.RIGHT, padx=5)
        
        button_frame = ttk.Frame(user_frame)
        button_frame.pack(side=tk.LEFT)
        
        ttk.Button(button_frame, text="Profile", 
                  command=lambda: ProfileWindow(self.root, self.user_manager, self.current_user)
                  ).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Logout", command=self.logout, 
                  style='secondary.TButton').pack(side=tk.RIGHT, padx=5)
        
        # Item Entry Frame
        entry_frame = ttk.LabelFrame(main_container, text="Add Item", padding="10")
        entry_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        # Category selection
        ttk.Label(entry_frame, text="Category:").grid(row=0, column=6, padx=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(entry_frame, width=15, textvariable=self.category_var)
        self.category_combo['values'] = ["All", "Fruits", "Vegetables"]
        self.category_combo.set("All")
        self.category_combo.grid(row=0, column=5, padx=5)
        
        # Item selection combobox
        ttk.Label(entry_frame, text="Select Item:").grid(row=0, column=4, padx=5)
        self.item_var = tk.StringVar()
        self.item_combo = ttk.Combobox(entry_frame, width=30, textvariable=self.item_var)
        self.update_items_list()
        self.item_combo.grid(row=0, column=3, padx=5)
        
        # Price label (read-only)
        ttk.Label(entry_frame, text="Price (£):").grid(row=0, column=2, padx=5)
        self.price_var = tk.StringVar()
        price_label = ttk.Label(entry_frame, textvariable=self.price_var, width=8)
        price_label.grid(row=0, column=1, padx=5)
        
        # Quantity spinbox
        ttk.Label(entry_frame, text="Qty:").grid(row=0, column=0, padx=5)
        self.item_qty = ttk.Spinbox(entry_frame, from_=1, to=100, width=5)
        self.item_qty.grid(row=1, column=0, padx=5)
        
        # Add button
        ttk.Button(entry_frame, text="Add", 
                  command=self.add_item, style='primary.TButton').grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        
        # Bind combobox selections to update functions
        def update_price(*args):
            selected_item = self.item_var.get()
            if selected_item in self.predefined_items:
                self.price_var.set(f"£{self.predefined_items[selected_item]['price']:.2f}")
            else:
                self.price_var.set("")
        
        def update_items_by_category(*args):
            self.update_items_list()
            self.item_var.set("")
            self.price_var.set("")
        
        self.category_combo.bind('<<ComboboxSelected>>', update_items_by_category)
        self.item_combo.bind('<<ComboboxSelected>>', update_price)
        
        # Items List
        list_frame = ttk.LabelFrame(main_container, text="Items", padding="10")
        list_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        
        # Treeview style
        style = ttk.Style()
        style.configure("Treeview", 
                       rowheight=30,
                       font=('Arial', 11),
                       background="#f0f0f0",
                       fieldbackground="#f0f0f0")
        style.configure("Treeview.Heading", 
                       font=('Arial', 10, 'bold'),
                       padding=5)
        style.map('Treeview',
                 background=[('selected', '#0078D7')],
                 foreground=[('selected', 'white')])
        
        # Treeview for items
        self.tree = ttk.Treeview(list_frame, columns=("name", "price", "qty", "total"), 
                                show="headings", height=15)
        
        # Configure headings with Arabic text
        self.tree.heading("name", text="Item Name")
        self.tree.heading("price", text="Price")
        self.tree.heading("qty", text="Quantity")
        self.tree.heading("total", text="Total")
        
        # Configure columns with better proportions and alignment
        self.tree.column("name", width=300, anchor="e", stretch=True)  # Align right for Arabic
        self.tree.column("price", width=120, anchor="e")
        self.tree.column("qty", width=100, anchor="e")
        self.tree.column("total", width=120, anchor="e")
        
        self.tree.grid(row=0, column=0, sticky="nsew", padx=5)
        
        # Styled scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Buttons frame with better styling
        button_frame = ttk.Frame(list_frame)
        button_frame.grid(row=1, column=0, pady=10)
        ttk.Button(button_frame, text="Remove Selected", 
                  command=self.remove_item, 
                  style='danger.TButton',
                  padding=(20, 5)).pack(side=tk.RIGHT, padx=5)
        
        # Total and Checkout Frame
        total_frame = ttk.LabelFrame(main_container, text="Summary", padding="10")
        total_frame.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        
        # Summary labels with better styling
        self.subtotal_label = ttk.Label(total_frame, text="Subtotal: 0.00 SAR", 
                                      font=("Arial", 10))
        self.subtotal_label.grid(row=0, column=2, padx=10)
        
        self.vat_label = ttk.Label(total_frame, text="VAT (20%): 0.00 SAR", 
                                  font=("Arial", 10))
        self.vat_label.grid(row=0, column=1, padx=10)
        
        self.total_label = ttk.Label(total_frame, text="Total: 0.00 SAR", 
                                   font=("Arial", 12, "bold"))
        self.total_label.grid(row=0, column=0, padx=10)
        
        # Action buttons
        button_frame = ttk.Frame(total_frame)
        button_frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Clear All", 
                  command=self.clear_all, style='secondary.TButton').grid(row=0, column=4, padx=5)
        ttk.Button(button_frame, text="View Receipts", 
                  command=self.view_receipt_history, style='info.TButton').grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Complete Sale", 
                  command=self.checkout, style='success.TButton').grid(row=0, column=0, padx=5)
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(2, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
    def update_items_list(self):
        """Update items list based on selected category"""
        category = self.category_var.get()
        if category == "All":
            items = sorted(self.predefined_items.keys())
        else:
            items = sorted([item for item, details in self.predefined_items.items() 
                          if details['category'] == category])
        self.item_combo['values'] = items
    
    def add_item(self):
        name = self.item_var.get().strip()
        qty_str = self.item_qty.get().strip()
        
        if not name or name not in self.predefined_items:
            messagebox.showerror("Error", "Please select an item from the list")
            return
            
        try:
            qty = int(qty_str)
            if qty < 1:
                messagebox.showerror("Error", "Quantity must be at least 1")
                return
                
            price = Decimal(str(self.predefined_items[name]['price']))
            item_total = price * qty
            
            self.items.append((name, price, qty, item_total))
            self.update_totals()
            
            # Update display
            self.tree.insert("", "end", values=(name, f"£{price:.2f}", qty, f"£{item_total:.2f}"))
            
            # Clear selection
            self.item_var.set('')
            self.price_var.set('')
            self.item_qty.delete(0, tk.END)
            self.item_qty.insert(0, "1")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity (whole number)")
            return
        
    def remove_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an item to remove")
            return
            
        self.tree.delete(selected_item)
        self.items.pop(self.tree.index(selected_item))
        self.update_totals()
        
    def update_totals(self):
        self.total = sum(item[3] for item in self.items)
        vat = self.total * self.vat_rate
        subtotal = self.total - vat
        
        self.subtotal_label.config(text=f"Subtotal: £{subtotal:.2f}")
        self.vat_label.config(text=f"VAT (20%): £{vat:.2f}")
        self.total_label.config(text=f"Total: £{self.total:.2f}")
        
    def clear_all(self):
        self.tree.delete(*self.tree.get_children())
        self.items = []
        self.update_totals()
        
    def generate_receipt(self):
        """Generate receipt text"""
        receipt = []
        receipt.append("=" * 40)
        receipt.append("Supermarket Till Receipt")
        receipt.append("=" * 40)
        receipt.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Add employee info
        try:
            profile = self.user_manager.get_user_profile(self.current_user)
            employee_name = profile['full_name'] if profile else self.current_user
        except:
            employee_name = self.current_user
        receipt.append(f"Employee: {employee_name}")
        receipt.append("-" * 40)
        
        # Add items
        receipt.append("Items:")
        receipt.append("-" * 40)
        for name, price, qty, total in self.items:
            receipt.append(f"{name:<30} {qty:>3} x £{price:>6.2f} = £{total:>7.2f}")
        
        receipt.append("-" * 40)
        
        # Add totals
        vat = self.total * self.vat_rate
        subtotal = self.total - vat
        receipt.append(f"{'Subtotal:':<20} £{subtotal:>7.2f}")
        receipt.append(f"{'VAT (20%):':<20} £{vat:>7.2f}")
        receipt.append(f"{'Total:':<20} £{self.total:>7.2f}")  # Store total in a consistent format
        
        receipt.append("=" * 40)
        receipt.append("Thank you for shopping with us!")
        receipt.append("=" * 40)
        
        return "\n".join(receipt)
        
    def save_receipt_pdf(self):
        if not self.items:
            messagebox.showinfo("Warning", "No items to save")
            return
            
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[(f"PDF Files (*.pdf)", "*.pdf")],
                title="Save Receipt"
            )
            
            if not filename:
                return
                
            # Create PDF
            pdf = FPDF()
            pdf.add_page()
            
            # Add font
            pdf.add_font('Arial', '', 'arial.ttf', uni=True)
            
            # Set page margins
            pdf.set_margins(10, 10, 10)
            
            # Store name - Large font with better spacing
            pdf.set_font('Arial', size=24)
            pdf.ln(10)  # Add space at top
            pdf.cell(0, 15, txt="Supermarket Receipt", ln=True, align='C')
            
            # Receipt type - Medium font with better spacing
            pdf.set_font('Arial', size=18)
            pdf.cell(0, 15, txt="Simple VAT Receipt", ln=True, align='C')
            pdf.ln(5)  # Add space after header
            
            # Add receipt content
            pdf.set_font('Arial', size=12)
            
            # Date and Time
            now = datetime.now()
            pdf.cell(0, 8, txt=f"Date: {now.strftime('%Y-%m-%d')}", ln=True)
            pdf.cell(0, 8, txt=f"Time: {now.strftime('%H:%M:%S')}", ln=True)
            
            # Cashier information
            cashier_profile = self.user_manager.get_user_profile(self.current_user)
            pdf.ln(5)
            pdf.cell(0, 8, txt="Cashier Information", ln=True)
            pdf.cell(0, 8, txt=f"Employee: {cashier_profile['full_name']}", ln=True)
            pdf.cell(0, 8, txt=f"Employee ID: {self.current_user}", ln=True)
            pdf.ln(5)
            
            # Table settings
            col_widths = [90, 30, 30, 40]  # Item, Price, Qty, Total
            row_height = 8
            
            # Draw table header
            pdf.set_fill_color(240, 240, 240)  # Light gray background
            pdf.cell(col_widths[0], row_height, "Item", border=1, fill=True)
            pdf.cell(col_widths[1], row_height, "Price", border=1, fill=True)
            pdf.cell(col_widths[2], row_height, "Qty", border=1, fill=True)
            pdf.cell(col_widths[3], row_height, "Total", border=1, fill=True)
            pdf.ln()
            
            # Draw items
            for name, price, qty, total in self.items:
                pdf.cell(col_widths[0], row_height, name[:35], border=1)
                pdf.cell(col_widths[1], row_height, f"£{price:.2f}", border=1)
                pdf.cell(col_widths[2], row_height, str(qty), border=1)
                pdf.cell(col_widths[3], row_height, f"£{total:.2f}", border=1)
                pdf.ln()
            
            # Add totals with table format
            pdf.ln(5)
            subtotal = self.total / (1 + self.vat_rate)
            vat = self.total - subtotal
            
            # Summary table
            summary_width = 140
            amount_width = 50
            row_height = 10
            
            # Table header
            pdf.set_fill_color(240, 240, 240)  # Light gray background
            pdf.cell(summary_width, row_height, "Summary", border=1, fill=True)
            pdf.cell(amount_width, row_height, "Amount", border=1, fill=True)
            pdf.ln()
            
            # Subtotal and VAT rows
            pdf.cell(summary_width, row_height, "Subtotal", border=1)
            pdf.cell(amount_width, row_height, f"£{subtotal:.2f}", border=1)
            pdf.ln()
            
            pdf.cell(summary_width, row_height, "VAT (20%)", border=1)
            pdf.cell(amount_width, row_height, f"£{vat:.2f}", border=1)
            pdf.ln()
            
            # Total row with color
            pdf.set_fill_color(230, 230, 250)  # Light purple background
            pdf.set_font('Arial', size=12, style='B')  # Bold font for total
            pdf.cell(summary_width, row_height, "Total", border=1, fill=True)
            pdf.cell(amount_width, row_height, f"£{self.total:.2f}", border=1, fill=True)
            pdf.ln()
            
            # Add footer
            pdf.ln(10)
            pdf.set_font('Arial', size=12)
            pdf.cell(0, 8, "Thank you for shopping with us", ln=True, align='C')
            pdf.cell(0, 8, "We hope you have a great day", ln=True, align='C')
            
            # Save the PDF
            pdf.output(filename, 'F')
            messagebox.showinfo("Success", "Receipt saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save receipt: {str(e)}")
        
    def save_receipt_to_history(self, receipt_text):
        """Save receipt to history with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"receipt_{timestamp}.txt"
        filepath = os.path.join(self.receipts_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(receipt_text)
        except Exception as e:
            print(f"Error saving receipt: {e}")
            messagebox.showerror("Error", 
                               "Failed to save receipt to history")

    def view_receipt_history(self):
        """Show receipt history window"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Receipt History")
        history_window.geometry("800x600")
        history_window.minsize(800, 600)  # Set minimum size
        history_window.transient(self.root)
        history_window.grab_set()

        # Main container
        main_frame = ttk.Frame(history_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tree frame with fixed height
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Create and configure the tree
        tree = ttk.Treeview(tree_frame, 
                           columns=("date", "time", "cashier", "total"), 
                           show="headings",
                           height=15)  # Fixed height

        # Configure columns
        tree.heading("date", text="Date", anchor="center")
        tree.heading("time", text="Time", anchor="center")
        tree.heading("cashier", text="Cashier", anchor="center")
        tree.heading("total", text="Total", anchor="center")

        tree.column("date", width=150, anchor="center")
        tree.column("time", width=150, anchor="center")
        tree.column("cashier", width=250, anchor="center")
        tree.column("total", width=150, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Button frame at the bottom
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 5))

        # Add buttons with fixed width and padding
        ttk.Button(btn_frame, text="Close", style='secondary.TButton',
                  command=lambda: self.close_history_window(history_window),
                  width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", style='danger.TButton',
                  command=lambda: self.delete_receipt(tree),
                  width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Print", style='info.TButton',
                  command=lambda: self.print_receipt(tree),
                  width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="View", style='info.TButton',
                  command=lambda: self.view_selected_receipt(tree),
                  width=15).pack(side=tk.LEFT, padx=5)

        # Load receipts
        self.load_receipts(tree)

        # Release grab when window is closed
        history_window.bind("<Destroy>", lambda e: history_window.grab_release())

    def load_receipts(self, tree):
        """Load receipts into treeview"""
        for item in tree.get_children():
            tree.delete(item)
        
        row_count = 0  # Counter for alternating row colors
        for filename in sorted(os.listdir(self.receipts_dir), reverse=True):
            if filename.startswith("receipt_") and filename.endswith(".txt"):
                try:
                    filepath = os.path.join(self.receipts_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract date and time from filename
                    date_str = filename[8:16]  # YYYYMMDD
                    time_str = filename[17:23]  # HHMMSS
                    
                    # Format date and time
                    date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
                    time = f"{time_str[:2]}:{time_str[2:4]}:{time_str[4:]}"
                    
                    # Extract receipt details
                    cashier = "Unknown"
                    total = 0.00
                    
                    for line in content.split('\n'):
                        line = line.strip()
                        if not line:
                            continue
                            
                        if "Employee: " in line:
                            cashier = line.split("Employee: ")[1].strip()
                        elif "Total:" in line:
                            try:
                                total_str = line.split("£")[-1].strip()
                                total = float(total_str)
                            except:
                                pass
                    
                    # Insert with alternating row colors
                    tag = 'evenrow' if row_count % 2 == 0 else 'oddrow'
                    tree.insert("", 0, values=(date, time, cashier, f"£{total:.2f}"), tags=(tag,))
                    row_count += 1
                    
                except Exception as e:
                    print(f"Error loading receipt {filename}: {e}")

    def close_history_window(self, window):
        """Close history window and release grab"""
        window.grab_release()
        window.destroy()
        
    def view_selected_receipt(self, tree):
        """View selected receipt"""
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("Warning", "Please select a receipt to view")
            return
        
        item = tree.item(selected[0])
        date = item['values'][0].replace('-', '')
        time = item['values'][1].replace(':', '')
        filename = f"receipt_{date}_{time}.txt"
        filepath = os.path.join(self.receipts_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self.show_receipt_viewer(content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view receipt: {str(e)}")

    def show_receipt_viewer(self, content):
        """Show receipt content in a viewer window"""
        viewer = tk.Toplevel(self.root)
        viewer.title("Receipt Viewer")
        
        # Make window responsive
        screen_width = viewer.winfo_screenwidth()
        screen_height = viewer.winfo_screenheight()
        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.8)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        viewer.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        viewer.transient(self.root)
        viewer.grab_set()
        
        # Make window resizable
        viewer.resizable(True, True)
        viewer.minsize(600, 400)
        
        # Create main frame with padding
        main_frame = ttk.Frame(viewer, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Improved text widget with better formatting
        text_widget = tk.Text(text_frame, 
                            wrap=tk.WORD, 
                            font=('Courier', 13),  # Larger font
                            padx=15,  # Horizontal padding
                            pady=10,   # Vertical padding
                            spacing1=2,  # Space between lines
                            spacing2=2,  # Space between paragraphs
                            spacing3=2)  # Space after paragraphs
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Pack text widget and scrollbar
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert content
        text_widget.insert('1.0', content)
        text_widget.configure(state='disabled')  # Make read-only
        
        # Button frame with improved styling
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        # Buttons with consistent styling and better spacing
        button_style = {'width': 15, 'padding': (20, 10)}  # Wider buttons with more padding
        
        # Print button
        ttk.Button(button_frame, text="Print", style='info.TButton',
                  command=lambda: self.print_receipt_content(content),
                  **button_style).pack(side=tk.LEFT, padx=10)
        
        # Close button
        ttk.Button(button_frame, text="Close", style='secondary.TButton',
                  command=viewer.destroy,
                  **button_style).pack(side=tk.RIGHT, padx=10)
        
        # Release grab when window is closed
        viewer.bind("<Destroy>", lambda e: viewer.grab_release())

    def print_receipt(self, tree):
        """Print selected receipt"""
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("Warning", 
                              "Please select a receipt")
            return
        
        item = tree.item(selected[0])
        date = item['values'][0].replace('-', '')
        time = item['values'][1].replace(':', '')
        filename = f"receipt_{date}_{time}.txt"
        filepath = os.path.join(self.receipts_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self.print_receipt_content(content)
        except Exception as e:
            messagebox.showerror("Error", 
                               f"Failed to print receipt: {str(e)}")

    def print_receipt_content(self, content):
        """Print receipt content with improved table formatting"""
        try:
            # Create a temporary PDF
            temp_pdf = os.path.join(self.receipts_dir, "temp_print.pdf")
            
            # Create PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font('Arial', '', 'arial.ttf', uni=True)
            
            # Set margins
            pdf.set_margins(10, 10, 10)
            
            # Header
            pdf.set_font('Arial', size=16)
            pdf.cell(0, 10, "Supermarket Receipt", ln=True, align='C')
            pdf.ln(5)
            
            # Parse content sections
            header_info = []
            items = []
            summary = []
            
            section = "header"
            for line in content.split('\n'):
                if "Items:" in line:
                    section = "items"
                    continue
                elif "Subtotal:" in line:
                    section = "summary"
                
                if section == "header" and line.strip() and not line.startswith("="):
                    header_info.append(line)
                elif section == "items" and line.strip() and not line.startswith("-"):
                    if "x" in line:  # Only process item lines
                        items.append(line)
                elif section == "summary" and line.strip() and not line.startswith("="):
                    if any(x in line for x in ["Subtotal:", "VAT", "Total:"]):
                        summary.append(line)
            
            # Print header information
            pdf.set_font('Arial', size=10)
            for line in header_info:
                pdf.cell(0, 6, line, ln=True)
            pdf.ln(5)
            
            # Items table
            pdf.set_font('Arial', size=10)
            
            # Table header
            col_widths = [90, 30, 30, 40]  # Item, Price, Qty, Total
            row_height = 8
            
            # Header style
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(col_widths[0], row_height, "Item", border=1, fill=True)
            pdf.cell(col_widths[1], row_height, "Price", border=1, fill=True)
            pdf.cell(col_widths[2], row_height, "Qty", border=1, fill=True)
            pdf.cell(col_widths[3], row_height, "Total", border=1, fill=True)
            pdf.ln()
            
            # Items
            for item in items:
                parts = item.split('x')
                if len(parts) == 2:
                    name = parts[0].strip()
                    qty_price = parts[1].strip()
                    
                    # Extract price and total
                    try:
                        price = qty_price.split('=')[0].strip().replace('£', '')
                        total = qty_price.split('=')[1].strip().replace('£', '')
                        qty = qty_price.split('£')[0].strip()
                        
                        # Print row
                        pdf.cell(col_widths[0], row_height, name[:35], border=1)
                        pdf.cell(col_widths[1], row_height, f"£{price}", border=1)
                        pdf.cell(col_widths[2], row_height, qty, border=1)
                        pdf.cell(col_widths[3], row_height, f"£{total}", border=1)
                        pdf.ln()
                    except:
                        continue
            
            # Summary section
            pdf.ln(5)
            summary_width = 140
            amount_width = 50
            
            # Summary header
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(summary_width, row_height, "Summary", border=1, fill=True)
            pdf.cell(amount_width, row_height, "Amount", border=1, fill=True)
            pdf.ln()
            
            # Summary items
            for line in summary:
                if ":" in line:
                    label, amount = line.split(":", 1)
                    pdf.cell(summary_width, row_height, label.strip(), border=1)
                    pdf.cell(amount_width, row_height, amount.strip(), border=1)
                    pdf.ln()
            
            # Footer
            pdf.ln(10)
            pdf.cell(0, 8, "Thank you for shopping with us!", ln=True, align='C')
            
            # Save PDF
            pdf.output(temp_pdf)
            
            # Print the PDF
            os.startfile(temp_pdf, 'print')
            
            # Wait a bit before deleting the temporary file
            self.root.after(5000, lambda: os.remove(temp_pdf) if os.path.exists(temp_pdf) else None)
            
            messagebox.showinfo("Success", "Receipt sent for printing")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print receipt: {str(e)}")
            # Clean up temp file in case of error
            if os.path.exists(temp_pdf):
                try:
                    os.remove(temp_pdf)
                except:
                    pass

    def checkout(self):
        if not self.items:
            messagebox.showinfo("Warning", 
                              "No items to complete sale")
            return
            
        receipt = self.generate_receipt()
        
        # Save receipt to history
        self.save_receipt_to_history(receipt)
        
        # Show receipt
        messagebox.showinfo("Receipt", receipt)
        
        # Ask if user wants to save receipt as PDF
        if messagebox.askyesno("Save Receipt", 
                             "Do you want to save the receipt as a PDF?"):
            self.save_receipt_pdf()
        
        # Ask if user wants to print receipt
        if messagebox.askyesno("Print Receipt", 
                             "Do you want to print the receipt?"):
            self.print_receipt_content(receipt)
        
        self.clear_all()

    def delete_receipt(self, tree):
        """Delete selected receipt"""
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("Warning", "Please select a receipt to delete")
            return
        
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this receipt?"):
            return
            
        item = tree.item(selected[0])
        date = item['values'][0].replace('-', '')
        time = item['values'][1].replace(':', '')
        filename = f"receipt_{date}_{time}.txt"
        filepath = os.path.join(self.receipts_dir, filename)
        
        try:
            os.remove(filepath)
            tree.delete(selected[0])
            messagebox.showinfo("Success", "Receipt deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete receipt: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SupermarketTill(root)
    root.mainloop() 
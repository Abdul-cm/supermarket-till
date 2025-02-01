import tkinter as tk
from ttkbootstrap import Style, ttk
from users import UserManager
import tkinter.messagebox as messagebox

class LoginWindow:
    def __init__(self, parent):
        self.parent = parent
        self.user_manager = UserManager()
        
        # Use the main window instead of creating a new one
        self.window = parent
        self.window.title("Login - Supermarket Till")
        self.window.geometry("300x200")
        
        # Center the window
        self.center_window()
        
        # Create widgets
        self.create_widgets()
        
        # Set initial focus
        self.username.focus_force()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.result = None
    
    def create_widgets(self):
        # Create widgets
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Title
        title_label = ttk.Label(main_frame, text="Login", 
                              font=("Arial", 12, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Username
        ttk.Label(main_frame, text="Username:").grid(row=1, column=0, pady=5, sticky="e")
        self.username = ttk.Entry(main_frame)
        self.username.grid(row=1, column=1, pady=5, padx=(5, 0), sticky="ew")
        
        # Password
        ttk.Label(main_frame, text="Password:").grid(row=2, column=0, pady=5, sticky="e")
        self.password = ttk.Entry(main_frame, show="•")
        self.password.grid(row=2, column=1, pady=5, padx=(5, 0), sticky="ew")
        
        # Login button
        login_btn = ttk.Button(main_frame, text="Login", 
                             style="primary.TButton", command=self.login)
        login_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Error label
        self.error_label = ttk.Label(main_frame, text="", foreground="red")
        self.error_label.grid(row=4, column=0, columnspan=2)
        
        # Default user hint
        hint_text = "Default user: admin/admin123"
        hint_label = ttk.Label(main_frame, text=hint_text, font=("Arial", 8))
        hint_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Bind events
        self.window.bind('<Return>', lambda e: self.login())
        self.username.bind('<Return>', lambda e: self.password.focus())
        self.password.bind('<Return>', lambda e: self.login())
        
    def center_window(self):
        """Center the window on the screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def on_close(self):
        """Handle window close button"""
        if messagebox.askokcancel("Exit", "Do you want to exit the application?"):
            self.window.quit()
        
    def login(self):
        try:
            username = self.username.get().strip()
            password = self.password.get().strip()
            
            if not username or not password:
                self.error_label.config(text="Please enter username and password")
                return
            
            if self.user_manager.login(username, password):
                self.result = username
                self.window.quit()
            else:
                self.error_label.config(text="Invalid username or password")
                self.password.delete(0, tk.END)
                self.password.focus()
                
        except Exception as e:
            self.error_label.config(text=f"Login error: {str(e)}")
            
    def get_result(self):
        return self.result 
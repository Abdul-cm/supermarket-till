import tkinter as tk
from ttkbootstrap import Style, ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

class ProfileWindow:
    def __init__(self, parent, user_manager, username):
        self.parent = parent
        self.user_manager = user_manager
        self.username = username
        
        # Get user profile with default values
        self.profile = self.get_profile_with_defaults()
        
        # Create profile window
        self.window = tk.Toplevel(parent)
        self.window.title(f"Profile - {self.profile['full_name']}")
        self.window.geometry("400x600")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center the window
        self.center_window()
        
        # Create widgets
        self.create_widgets()
        
        # Wait for window to be created
        self.window.update_idletasks()
    
    def get_profile_with_defaults(self):
        """Get user profile with default values if any field is missing"""
        try:
            profile = self.user_manager.get_user_profile(self.username)
            if not profile:
                profile = {}
                
            # Ensure all required fields exist with defaults
            defaults = {
                'full_name': self.username,
                'email': 'Not set',
                'role': 'User',
                'profile_image': '',
                'created_date': datetime.now().isoformat(),
                'last_login': None
            }
            
            # Update profile with any missing defaults
            for key, default_value in defaults.items():
                if key not in profile or not profile[key]:
                    profile[key] = default_value
            
            return profile
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load profile: {str(e)}")
            # Return default profile
            return {
                'full_name': self.username,
                'email': 'Not set',
                'role': 'User',
                'profile_image': '',
                'created_date': datetime.now().isoformat(),
                'last_login': None
            }
    
    def center_window(self):
        """Center the window on the screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        try:
            # Main container
            main_frame = ttk.Frame(self.window, padding="20")
            main_frame.grid(row=0, column=0, sticky="nsew")
            
            # Profile Image
            img_frame = ttk.LabelFrame(main_frame, text="Profile Picture", padding="10")
            img_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="nsew")
            
            # Default image or user's profile image
            self.image_label = ttk.Label(img_frame)
            self.image_label.grid(row=0, column=0, columnspan=2, pady=5)
            self.load_profile_image()
            
            ttk.Button(img_frame, text="Change Picture", 
                      command=self.change_image).grid(row=1, column=0, columnspan=2)
            
            # User Information
            info_frame = ttk.LabelFrame(main_frame, text="User Information", padding="10")
            info_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="nsew")
            
            # Username (non-editable)
            ttk.Label(info_frame, text="Username:").grid(row=0, column=0, pady=5, sticky="e")
            ttk.Label(info_frame, text=self.username, 
                     font=("Arial", 10, "bold")).grid(row=0, column=1, pady=5, sticky="w")
            
            # Full Name
            ttk.Label(info_frame, text="Full Name:").grid(row=1, column=0, pady=5, sticky="e")
            self.full_name = ttk.Entry(info_frame)
            self.full_name.insert(0, self.profile['full_name'])
            self.full_name.grid(row=1, column=1, pady=5, sticky="ew")
            
            # Email
            ttk.Label(info_frame, text="Email:").grid(row=2, column=0, pady=5, sticky="e")
            self.email = ttk.Entry(info_frame)
            self.email.insert(0, self.profile['email'])
            self.email.grid(row=2, column=1, pady=5, sticky="ew")
            
            # Role (non-editable)
            ttk.Label(info_frame, text="Role:").grid(row=3, column=0, pady=5, sticky="e")
            ttk.Label(info_frame, text=self.profile['role'],
                     font=("Arial", 10)).grid(row=3, column=1, pady=5, sticky="w")
            
            # Account Information
            account_frame = ttk.LabelFrame(main_frame, text="Account Information", padding="10")
            account_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20), sticky="nsew")
            
            # Created Date
            created_date = datetime.fromisoformat(self.profile['created_date']).strftime("%Y-%m-%d %H:%M")
            ttk.Label(account_frame, text="Created Date:").grid(row=0, column=0, pady=5, sticky="e")
            ttk.Label(account_frame, text=created_date).grid(row=0, column=1, pady=5, sticky="w")
            
            # Last Login
            last_login = "Never logged in"
            if self.profile['last_login']:
                last_login = datetime.fromisoformat(self.profile['last_login']).strftime("%Y-%m-%d %H:%M")
            ttk.Label(account_frame, text="Last Login:").grid(row=1, column=0, pady=5, sticky="e")
            ttk.Label(account_frame, text=last_login).grid(row=1, column=1, pady=5, sticky="w")
            
            # Buttons
            btn_frame = ttk.Frame(main_frame)
            btn_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
            
            ttk.Button(btn_frame, text="Change Password", 
                      command=self.change_password).grid(row=0, column=0, padx=5)
            ttk.Button(btn_frame, text="Save Changes", style="primary.TButton",
                      command=self.save_changes).grid(row=0, column=1, padx=5)
            
            # Configure grid
            self.window.grid_columnconfigure(0, weight=1)
            self.window.grid_rowconfigure(0, weight=1)
            main_frame.grid_columnconfigure(1, weight=1)
            info_frame.grid_columnconfigure(1, weight=1)
            account_frame.grid_columnconfigure(1, weight=1)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating profile window: {str(e)}")
            self.window.destroy()
    
    def load_profile_image(self):
        try:
            # Default image size
            img_size = (150, 150)
            
            if self.profile['profile_image'] and os.path.exists(self.profile['profile_image']):
                # Load user's profile image
                img = Image.open(self.profile['profile_image'])
            else:
                # Load default profile image
                img = Image.open("default_profile.png")
            
            # Resize image
            img = img.resize(img_size, Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.photo)
            
        except Exception as e:
            print(f"Error loading profile image: {e}")
            self.image_label.config(text="No image")
            
    def change_image(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Choose Profile Picture",
                filetypes=[
                    ("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                    ("All Files", "*.*")
                ]
            )
            
            if file_path:
                # Save the image and get the new path
                new_path = self.user_manager.save_profile_image(self.username, file_path)
                if new_path:
                    self.profile['profile_image'] = new_path
                    self.load_profile_image()
                    self.user_manager.update_profile(self.username, profile_image=new_path)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change profile picture: {str(e)}")
            
    def change_password(self):
        # Create password change dialog
        dialog = tk.Toplevel(self.window)
        dialog.title("Change Password")
        dialog.geometry("300x200")
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create widgets
        frame = ttk.Frame(dialog, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")
        
        ttk.Label(frame, text="Current Password:").grid(row=0, column=0, pady=5)
        old_pass = ttk.Entry(frame, show="•")
        old_pass.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="New Password:").grid(row=1, column=0, pady=5)
        new_pass = ttk.Entry(frame, show="•")
        new_pass.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Confirm Password:").grid(row=2, column=0, pady=5)
        confirm_pass = ttk.Entry(frame, show="•")
        confirm_pass.grid(row=2, column=1, pady=5)
        
        error_label = ttk.Label(frame, text="", foreground="red")
        error_label.grid(row=3, column=0, columnspan=2, pady=5)
        
        def do_change_password():
            if new_pass.get() != confirm_pass.get():
                error_label.config(text="Passwords do not match")
                return
                
            if self.user_manager.change_password(self.username, old_pass.get(), new_pass.get()):
                messagebox.showinfo("Success", "Password changed successfully")
                dialog.destroy()
            else:
                error_label.config(text="Current password is incorrect")
        
        ttk.Button(frame, text="Change Password", command=do_change_password,
                  style="primary.TButton").grid(row=4, column=0, columnspan=2, pady=20)
        
        # Configure grid
        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        
        # Set initial focus
        old_pass.focus()
    
    def save_changes(self):
        try:
            full_name = self.full_name.get().strip()
            email = self.email.get().strip()
            
            if not full_name or not email:
                messagebox.showerror("Error", "Please fill in all fields")
                return
                
            if self.user_manager.update_profile(self.username, full_name=full_name, email=email):
                messagebox.showinfo("Success", "Profile updated successfully")
                self.window.title(f"Profile - {full_name}")
            else:
                messagebox.showerror("Error", "Failed to update profile")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {str(e)}") 
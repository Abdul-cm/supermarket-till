import json
import os
import shutil
from hashlib import sha256
from typing import Optional, Dict, Any
from datetime import datetime

class UserManager:
    def __init__(self):
        self.users_file = "users.json"
        self.profile_images_dir = "profile_images"
        self.current_user = None
        self.users: Dict[str, Any] = {}
        
        # Create profile images directory if it doesn't exist
        if not os.path.exists(self.profile_images_dir):
            os.makedirs(self.profile_images_dir)
            
        self.load_users()
    
    def load_users(self):
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            else:
                # Create default admin user with complete profile
                self.users = {
                    "admin": {
                        "password": self._hash_password("admin123"),
                        "role": "admin",
                        "full_name": "Administrator",
                        "email": "admin@example.com",
                        "profile_image": "",
                        "created_date": datetime.now().isoformat(),
                        "last_login": None
                    }
                }
                self.save_users()
        except Exception as e:
            print(f"Error loading users: {e}")
            # Ensure we at least have the admin user with complete profile
            self.users = {
                "admin": {
                    "password": self._hash_password("admin123"),
                    "role": "admin",
                    "full_name": "Administrator",
                    "email": "admin@example.com",
                    "profile_image": "",
                    "created_date": datetime.now().isoformat(),
                    "last_login": None
                }
            }
    
    def save_users(self):
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False
    
    def _hash_password(self, password: str) -> str:
        if not password:
            raise ValueError("Password cannot be empty")
        return sha256(password.encode()).hexdigest()
    
    def login(self, username: str, password: str) -> bool:
        try:
            if not username or not password:
                return False
                
            username = username.strip()
            if username not in self.users:
                return False
                
            stored_password = self.users[username]["password"]
            if stored_password == self._hash_password(password):
                self.current_user = username
                # Update last login
                self.users[username]["last_login"] = datetime.now().isoformat()
                self.save_users()
                return True
                
            return False
            
        except Exception as e:
            print(f"Login error: {e}")
            return False
    
    def logout(self):
        self.current_user = None
    
    def add_user(self, username: str, password: str, full_name: str = "", email: str = "", 
                role: str = "cashier", profile_image: str = "") -> bool:
        try:
            if not username or not password:
                return False
                
            username = username.strip()
            if username in self.users:
                return False
            
            if role not in ["admin", "cashier"]:
                role = "cashier"
            
            # Create user with complete profile
            self.users[username] = {
                "password": self._hash_password(password),
                "role": role,
                "full_name": full_name or username,  # Use username if no full name provided
                "email": email or "Not set",
                "profile_image": profile_image,
                "created_date": datetime.now().isoformat(),
                "last_login": None
            }
            return self.save_users()
            
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    def update_profile(self, username: str, full_name: str = None, email: str = None, 
                      profile_image: str = None) -> bool:
        try:
            if username not in self.users:
                return False
            
            if full_name is not None:
                self.users[username]["full_name"] = full_name
            if email is not None:
                self.users[username]["email"] = email
            if profile_image is not None:
                # Remove old profile image if it exists
                old_image = self.users[username].get("profile_image", "")
                if old_image and os.path.exists(old_image):
                    try:
                        os.remove(old_image)
                    except:
                        pass
                self.users[username]["profile_image"] = profile_image
                
            return self.save_users()
            
        except Exception as e:
            print(f"Error updating profile: {e}")
            return False
    
    def get_user_profile(self, username: str) -> Optional[Dict[str, Any]]:
        try:
            if username in self.users:
                profile = self.users[username].copy()
                profile.pop("password", None)  # Remove password from profile data
                
                # Ensure all required fields exist
                defaults = {
                    "full_name": username,
                    "email": "Not set",
                    "role": "cashier",
                    "profile_image": "",
                    "created_date": datetime.now().isoformat(),
                    "last_login": None
                }
                
                # Add any missing fields with defaults
                for key, default_value in defaults.items():
                    if key not in profile or not profile[key]:
                        profile[key] = default_value
                
                return profile
                
        except Exception as e:
            print(f"Error getting user profile: {e}")
        return None
    
    def get_current_user(self) -> Optional[str]:
        return self.current_user
    
    def get_user_role(self, username: str) -> Optional[str]:
        try:
            if username in self.users:
                return self.users[username]["role"]
        except Exception as e:
            print(f"Error getting user role: {e}")
        return None
        
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        try:
            if username not in self.users:
                return False
                
            if self.users[username]["password"] != self._hash_password(old_password):
                return False
                
            self.users[username]["password"] = self._hash_password(new_password)
            return self.save_users()
            
        except Exception as e:
            print(f"Error changing password: {e}")
            return False
            
    def save_profile_image(self, username: str, image_path: str) -> Optional[str]:
        try:
            if not os.path.exists(image_path):
                return None
                
            # Create a unique filename
            ext = os.path.splitext(image_path)[1]
            new_filename = f"{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
            new_path = os.path.join(self.profile_images_dir, new_filename)
            
            # Copy the image file
            shutil.copy2(image_path, new_path)
            return new_path
            
        except Exception as e:
            print(f"Error saving profile image: {e}")
            return None 
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivy.app import App
import threading

from core.login import perform_login

class HomeScreen(Screen):
    status_text = StringProperty("READY")
    status_color = ListProperty([0.557, 0.557, 0.627, 1])  # Default muted
    btn_color = ListProperty([1, 0.42, 0.42, 1])  # #FF6B6B
    active_profile_name = StringProperty("Profile")
    profile_index_text = StringProperty("1/3")
    
    def on_enter(self, *args):
        self.refresh_profile_ui()
        
    def refresh_profile_ui(self):
        app = App.get_running_app()
        idx = app.app_data.get('active_profile', 0)
        profiles = app.app_data.get('profiles', [])
        if profiles and idx < len(profiles):
            self.active_profile_name = profiles[idx].get('name', f"Profile {idx+1}")
            self.profile_index_text = f"{idx+1}/{len(profiles)}"
            
    def cycle_profile(self):
        app = App.get_running_app()
        idx = app.app_data.get('active_profile', 0)
        profiles = app.app_data.get('profiles', [])
        if profiles:
            next_idx = (idx + 1) % len(profiles)
            app.app_data['active_profile'] = next_idx
            
            from core.storage import save_data
            save_data(app.app_data)
            self.refresh_profile_ui()
            
    def start_login(self):
        if self.status_text == "CONNECTING":
            return
            
        app = App.get_running_app()
        idx = app.app_data.get('active_profile', 0)
        profiles = app.app_data.get('profiles', [])
        
        if not profiles or idx >= len(profiles):
            self.status_text = "FAILED"
            self.status_color = [1, 0.278, 0.34, 1]  # #FF4757
            return
            
        username = profiles[idx].get('username', '')
        password = profiles[idx].get('password', '')
        
        self.status_text = "CONNECTING"
        self.status_color = [1, 0.647, 0.008, 1]  # #FFA502
        self.btn_color = [1, 0.42, 0.42, 1] 
        
        t = threading.Thread(target=perform_login, args=(username, password, self.login_callback), daemon=True)
        t.start()
        
    def login_callback(self, success, message):
        # Runs on main thread
        if success:
            self.status_text = "CONNECTED"
            self.status_color = [0.18, 0.835, 0.45, 1]  # #2ED573
            self.btn_color = [0.263, 0.773, 0.62, 1] # #43C59E
        else:
            self.status_text = "FAILED"
            self.status_color = [1, 0.278, 0.34, 1]  # #FF4757
            self.btn_color = [1, 0.42, 0.42, 1] # #FF6B6B

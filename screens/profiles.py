from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ListProperty
from kivy.app import App
from core.storage import save_data

class ProfilesScreen(Screen):
    active_tab = NumericProperty(0)
    
    def on_enter(self, *args):
        self.load_profile_to_ui(self.active_tab)
        
    def get_tab_color(self, tab_index, active_tab_index):
        if tab_index == active_tab_index:
            return App.get_running_app().accent_color_rgba  # Active
        return [0.086, 0.094, 0.16, 1]  # Inactive
        
    def switch_tab(self, index):
        # Save current tab before switching
        self.save_profile_from_ui(self.active_tab)
        self.active_tab = index
        self.load_profile_to_ui(index)
        
    def load_profile_to_ui(self, index):
        app = App.get_running_app()
        profiles = app.app_data.get('profiles', [])
        if index < len(profiles):
            p = profiles[index]
            self.ids.profile_name.text = p.get('name', '')
            self.ids.username.text = p.get('username', '')
            self.ids.password.text = p.get('password', '')
            
    def save_profile_from_ui(self, index):
        app = App.get_running_app()
        profiles = app.app_data.get('profiles', [])
        if index < len(profiles):
            profiles[index]['name'] = self.ids.profile_name.text
            profiles[index]['username'] = self.ids.username.text
            profiles[index]['password'] = self.ids.password.text
            save_data(app.app_data)
            
    def save_current_profile(self):
        self.save_profile_from_ui(self.active_tab)
        # Refresh UI or show toast if we had kivymd toasts imported

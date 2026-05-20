import kivy
from kivy.utils import platform
from kivy.core.window import Window
import urllib3
import os

if platform != 'android':
    Window.size = (360, 640)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.properties import StringProperty, ListProperty

from core.storage import load_data, save_data
from core.wifi_monitor import WiFiMonitor

THEME_COLORS = {
    "Blue": [0.357, 0.42, 0.96, 1],
    "Purple": [0.61, 0.35, 0.96, 1],
    "Green": [0.18, 0.835, 0.45, 1],
    "Red": [1.0, 0.278, 0.34, 1],
    "Orange": [1.0, 0.647, 0.008, 1],
    "Pink": [1.0, 0.4, 0.7, 1]
}

from screens.home import HomeScreen
from screens.profiles import ProfilesScreen
from screens.settings import SettingsScreen

KV = '''
MDBoxLayout:
    orientation: 'vertical'
    md_bg_color: 0.05, 0.055, 0.10, 1
    
    ScreenManager:
        id: screen_manager
        
        HomeScreen:
            name: 'home'
            
        ProfilesScreen:
            name: 'profiles'
            
        SettingsScreen:
            name: 'settings'
            
    MDBoxLayout:
        size_hint_y: None
        height: "56dp"
        md_bg_color: 0.066, 0.07, 0.125, 1
        
        MDIconButton:
            icon: "home"
            theme_text_color: "Custom"
            text_color: app.accent_color_rgba if app.current_screen == 'home' else (0.557, 0.557, 0.627, 1)
            pos_hint: {"center_y": .5}
            on_release: app.switch_screen('home')
            size_hint_x: 1
            
        MDIconButton:
            icon: "account"
            theme_text_color: "Custom"
            text_color: app.accent_color_rgba if app.current_screen == 'profiles' else (0.557, 0.557, 0.627, 1)
            pos_hint: {"center_y": .5}
            on_release: app.switch_screen('profiles')
            size_hint_x: 1
            
        MDIconButton:
            icon: "cog"
            theme_text_color: "Custom"
            text_color: app.accent_color_rgba if app.current_screen == 'settings' else (0.557, 0.557, 0.627, 1)
            pos_hint: {"center_y": .5}
            on_release: app.switch_screen('settings')
            size_hint_x: 1
'''

class ConnekTorApp(MDApp):
    current_screen = StringProperty('home')
    accent_color_rgba = ListProperty([0.357, 0.42, 0.96, 1])
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        # Load KV files
        # Check paths in case running from another dir
        base_dir = os.path.dirname(__file__) or '.'
        Builder.load_file(os.path.join(base_dir, 'kv', 'home.kv'))
        Builder.load_file(os.path.join(base_dir, 'kv', 'profiles.kv'))
        Builder.load_file(os.path.join(base_dir, 'kv', 'settings.kv'))
        
        return Builder.load_string(KV)
        
    def on_start(self):
        self.app_data = load_data()
        
        if self.app_data.get('theme') == 'light':
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"
            
        color_name = self.app_data.get('accent_color', 'Blue')
        self.accent_color_rgba = THEME_COLORS.get(color_name, THEME_COLORS['Blue'])
            
        self.monitor = WiFiMonitor(
            login_callback=self._auto_login_trigger,
            get_auto_login_enabled=lambda: self.app_data.get('auto_login', False)
        )
        self.monitor.start()
        
    def switch_screen(self, screen_name):
        self.current_screen = screen_name
        sm = self.root.ids.screen_manager
        sm.transition = NoTransition()
        sm.current = screen_name
        
    def _auto_login_trigger(self):
        if not self.app_data.get('auto_login', False):
            return
        home_screen = self.root.ids.screen_manager.get_screen('home')
        home_screen.start_login()
        
if __name__ == '__main__':
    ConnekTorApp().run()

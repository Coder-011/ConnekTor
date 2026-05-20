from kivy.uix.screenmanager import Screen
from kivy.app import App
from core.storage import save_data
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

class SettingsScreen(Screen):
    dialog = None
    
    def on_enter(self, *args):
        app = App.get_running_app()
        self.ids.theme_switch.active = (app.app_data.get('theme', 'dark') == 'light')
        self.ids.auto_login_switch.active = app.app_data.get('auto_login', False)
        
    def on_theme_toggle(self, switch, value):
        app = App.get_running_app()
        new_theme = 'light' if value else 'dark'
        app.app_data['theme'] = new_theme
        save_data(app.app_data)
        
        # We enforce Dark theme according to prompt, but if they want to toggle it,
        # we can set app.theme_cls.theme_style. But colors are hardcoded dark.
        # Just update app.theme_cls anyway.
        app.theme_cls.theme_style = "Light" if value else "Dark"
        
    def on_auto_login_toggle(self, switch, value):
        app = App.get_running_app()
        if value and not app.app_data.get('auto_login', False):
            # Check if confirmed already
            if not app.app_data.get('auto_login_confirmed', False):
                self._show_auto_login_confirm_dialog()
            else:
                self._on_auto_login_confirmed()
        elif not value:
            app.app_data['auto_login'] = False
            save_data(app.app_data)
            if hasattr(app, 'monitor') and app.monitor:
                app.monitor.stop()
                app.monitor.start()
                
    def _show_auto_login_confirm_dialog(self):
        if not self.dialog:
            app = App.get_running_app()
            self.dialog = MDDialog(
                title="Enable Auto Login?",
                text="ConnekTor will automatically try to connect to the campus portal whenever your phone joins a WiFi network, while this app is open.\n\nYour active profile credentials will be used.",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=(0.557, 0.557, 0.627, 1),
                        on_release=self._on_auto_login_cancelled
                    ),
                    MDFlatButton(
                        text="ENABLE",
                        theme_text_color="Custom",
                        text_color=app.accent_color_rgba,
                        on_release=self._on_auto_login_confirmed
                    ),
                ],
            )
        self.dialog.open()
        
    def on_accent_color_select(self, color_name):
        app = App.get_running_app()
        app.app_data['accent_color'] = color_name
        save_data(app.app_data)
        from main import THEME_COLORS
        app.accent_color_rgba = THEME_COLORS.get(color_name, THEME_COLORS['Blue'])
        # Also update dialog button color if it exists
        if self.dialog:
            for btn in self.dialog.buttons:
                if btn.text == "ENABLE":
                    btn.text_color = app.accent_color_rgba
        
    def _on_auto_login_cancelled(self, *args):
        self.ids.auto_login_switch.active = False
        self.dialog.dismiss()
        
    def _on_auto_login_confirmed(self, *args):
        app = App.get_running_app()
        app.app_data['auto_login'] = True
        app.app_data['auto_login_confirmed'] = True
        save_data(app.app_data)
        if self.dialog:
            self.dialog.dismiss()

import os
import json
from kivy.app import App

DEFAULT_DATA = {
    "active_profile": 0,
    "auto_login": False,
    "auto_login_confirmed": False,
    "theme": "dark",
    "accent_color": "Blue",
    "profiles": [
        {"name": "Profile 1", "username": "", "password": ""},
        {"name": "Profile 2", "username": "", "password": ""},
        {"name": "Profile 3", "username": "", "password": ""}
    ]
}

def get_data_file_path():
    app = App.get_running_app()
    if app:
        return os.path.join(app.user_data_dir, 'app_data.json')
    # Fallback for testing without app running
    return 'app_data.json'

def load_data():
    file_path = get_data_file_path()
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Ensure all default keys exist
                for k, v in DEFAULT_DATA.items():
                    if k not in data:
                        data[k] = v
                
                # Ensure 3 profiles exist
                if 'profiles' not in data or not isinstance(data['profiles'], list):
                    data['profiles'] = DEFAULT_DATA['profiles']
                while len(data['profiles']) < 3:
                    data['profiles'].append({"name": f"Profile {len(data['profiles'])+1}", "username": "", "password": ""})
                
                return data
        except Exception as e:
            print(f"Error loading data: {e}")
            return DEFAULT_DATA.copy()
    return DEFAULT_DATA.copy()

def save_data(data):
    file_path = get_data_file_path()
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

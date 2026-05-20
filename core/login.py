import time
import requests
from kivy.clock import Clock

def perform_login(username, password, callback):
    """
    Performs the captive portal login.
    This function should be called from a daemon thread.
    
    Args:
        username (str): The username (e.g. '082bel013')
        password (str): The password
        callback (callable): Function to call with the result.
                             Signature: callback(success: bool, message: str)
                             Note: The callback is invoked on the main UI thread via Clock.schedule_once.
    """
    login_url = 'https://10.100.1.1:8090/login.xml'
    producttype = 'your_producttype'
    
    payload = {
        'mode': '191',
        'username': username,
        'password': password,
        'producttype': producttype,
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://10.100.1.1:8090/',
    }
    
    def report_result(success, message):
        # Ensure the callback runs on the main Kivy thread
        Clock.schedule_once(lambda dt: callback(success, message), 0)

    for attempt in range(2):
        timestamp = int(time.time() * 1000)
        payload['a'] = timestamp
        
        payload_encoded = '&'.join([
            f'{k}={requests.utils.quote(str(v))}'
            for k, v in payload.items()
        ])
        
        try:
            response = requests.post(
                login_url,
                data=payload_encoded,
                headers=headers,
                verify=False,
                timeout=10
            )
            
            if 'You are signed in as' in response.text:
                report_result(True, 'Login successful')
            else:
                report_result(False, 'Login failed: Invalid credentials')
            return
            
        except requests.exceptions.Timeout as e:
            if attempt == 0:
                time.sleep(2)
                continue
            report_result(False, f'Login failed: Timeout')
            return
            
        except requests.exceptions.RequestException as e:
            report_result(False, f'Login failed: {str(e)}')
            return

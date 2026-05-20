import threading
import time
import requests
from kivy.clock import Clock

# How often to probe for captive portal when auto-login is active (seconds)
POLL_INTERVAL = 8

# The portal gateway — if any WiFi network redirects here, we're on campus
PORTAL_HOST = '10.100.1.1'
PORTAL_PROBE_URL = 'http://captive.apple.com'  # plain HTTP, triggers redirect

class WiFiMonitor:
    """
    Polls for captive portal presence every POLL_INTERVAL seconds.
    Fires the login callback when portal is detected and not yet authenticated.
    Runs as a single daemon thread — only one instance allowed at a time.
    """

    def __init__(self, login_callback, get_auto_login_enabled):
        """
        login_callback: callable() — called when portal detected, no args.
                        Must be thread-safe (use Clock.schedule_once inside).
        get_auto_login_enabled: callable() -> bool — checked before every probe.
                                Allows real-time toggle without restarting monitor.
        """
        self._running = False
        self._thread = None
        self._login_callback = login_callback
        self._get_enabled = get_auto_login_enabled
        self._last_attempt_time = 0
        # Minimum seconds between auto-login attempts to avoid hammering portal
        self._cooldown = 30

    def start(self):
        if self._thread and self._thread.is_alive():
            return  # already running
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def _run(self):
        while self._running:
            time.sleep(POLL_INTERVAL)
            if not self._running:
                break

            # Respect the user toggle — check live every cycle
            if not self._get_enabled():
                continue

            # Cooldown guard — don't retry within 30s of last attempt
            now = time.time()
            if now - self._last_attempt_time < self._cooldown:
                continue

            try:
                self._probe_and_act()
            except Exception as e:
                print(f"WiFiMonitor error: {e}")
                pass  # never crash the monitor thread

    def _probe_and_act(self):
        """
        Probe connectivity. If we're behind the campus captive portal
        and not yet authenticated, fire the login callback.
        """
        try:
            # Use a plain HTTP URL — captive portals intercept these
            r = requests.get(
                PORTAL_PROBE_URL,
                timeout=5,
                allow_redirects=True,
                verify=False
            )
            # If redirected to our campus portal gateway, we're on campus WiFi
            # and not yet authenticated
            if PORTAL_HOST in r.url or PORTAL_HOST in r.text:
                self._last_attempt_time = time.time()
                Clock.schedule_once(lambda dt: self._login_callback(), 0)

            # If we got a clean 200/204 with no portal content, already online
            # — do nothing

        except requests.exceptions.ConnectionError:
            # No network at all — do nothing
            pass
        except requests.exceptions.Timeout:
            # Portal is slow — will retry next cycle
            pass

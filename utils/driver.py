from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import HEADLESS
import os
import platform
import tempfile


def resolve_chrome_binary():
    env_chrome_binary = os.getenv("CHROME_BINARY")
    if env_chrome_binary and os.path.exists(env_chrome_binary):
        return env_chrome_binary

    system = platform.system().lower()

    if system == "windows":
        windows_candidates = [
            r"C:\Users\luisd\Downloads\INSTALADORES\chrome-win64\chrome-win64\chrome.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]

        for path in windows_candidates:
            if os.path.exists(path):
                return path

    if system == "linux":
        linux_candidates = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
        ]

        for path in linux_candidates:
            if os.path.exists(path):
                return path

    return None


def get_driver():
    options = Options()

    chrome_path = resolve_chrome_binary()

    if chrome_path:
        options.binary_location = chrome_path
        print(f"[Selenium] Chrome binary detected: {chrome_path}")
    else:
        print("[Selenium] No explicit Chrome binary configured. Selenium will use system default.")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

    options.add_argument("--disable-password-manager-reauthentication")

    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
    }
    options.add_experimental_option("prefs", prefs)

    if HEADLESS:
        options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.maximize_window()
    except Exception:
        pass

    return driver
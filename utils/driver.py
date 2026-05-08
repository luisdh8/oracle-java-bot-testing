from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import HEADLESS
import os


def get_driver():
    """
    Inicializa Selenium WebDriver configurado para Chrome 147.
    WebDriver Manager descarga automáticamente ChromeDriver compatible.

    Returns:
        WebDriver: Selenium WebDriver instance
    """
    options = Options()

    # Usar Chrome (no Brave)
    chrome_path = r"C:\Users\luisd\Downloads\INSTALADORES\chrome-win64\chrome-win64\chrome.exe"

    # Si no existe la ruta portable, usar Chrome del sistema
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    options.binary_location = chrome_path

    # Argumentos para mejor compatibilidad
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Deshabilitar prompts de guardar contraseña y datos
    options.add_argument("--disable-password-manager-reauthentication")
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,  # Bloquear notificaciones
    }
    options.add_experimental_option("prefs", prefs)

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Modo headless si está configurado
    if HEADLESS:
        options.add_argument("--headless=new")

    # WebDriver Manager descargará automáticamente ChromeDriver 147
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.maximize_window()
    return driver
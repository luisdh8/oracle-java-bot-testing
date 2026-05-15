import pytest
from config.settings import BASE_URL, EMAIL, PASSWORD
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


def test_login_success(driver):
    """TC-01: Login con credenciales válidas"""
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    login_page.load(BASE_URL)
    login_page.login(email=EMAILA, password=PASSWORD)

    # Validación: dashboard cargado
    dashboard_page.verify_dashboard_loaded()
    dashboard_page.verify_nav_menu_visible()

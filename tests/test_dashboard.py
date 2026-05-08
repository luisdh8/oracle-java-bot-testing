from config.settings import BASE_URL, EMAIL, PASSWORD
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


def test_dashboard_visible_after_login(driver):
    """TC-02: Validar que dashboard esté visible después del login"""
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    # Login
    login_page.load(BASE_URL)
    login_page.login(email=EMAIL, password=PASSWORD)

    # Validaciones del dashboard
    dashboard_page.verify_dashboard_loaded()
    dashboard_page.verify_nav_menu_visible()
    dashboard_page.verify_project_in_progress("Oracle Java Bot")

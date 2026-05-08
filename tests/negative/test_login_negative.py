import pytest
from config.settings import BASE_URL
from pages.login_page import LoginPage


@pytest.mark.negative
@pytest.mark.ui
def test_login_invalid_credentials_rejected(driver, invalid_login_data):
    """TC-N01: Login inválido debe mostrar error y no guardar token."""
    login_page = LoginPage(driver)

    login_page.load(BASE_URL)
    login_page.login(
        email=invalid_login_data["email"],
        password=invalid_login_data["password"],
    )

    error_text = login_page.get_visible_error_text(timeout=15)
    assert invalid_login_data["expected_error"] in error_text, (
        "No se mostró el mensaje esperado para login inválido. "
        f"Esperado contener: '{invalid_login_data['expected_error']}'. "
        f"Actual: '{error_text}'"
    )

    token = driver.execute_script("return localStorage.getItem('token')")
    assert not token, "No debe existir token en localStorage para login inválido"

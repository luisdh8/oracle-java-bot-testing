from config.settings import BASE_URL, EMAIL, PASSWORD
from pages.login_page import LoginPage
from pages.base_page import BasePage
from selenium.webdriver.common.by import By


VALID_DEMO_MARKERS = [
    "Prueba Correcta",
    "Prueba Correcta 2",
]


def test_demo_quality_gate_marker_visible(driver):
    """
    DEMO-QG-01:
    Valida que el dashboard muestre un marcador aprobado por el quality gate.

    Valores válidos:
    - Prueba Correcta
    - Prueba Correcta 2

    Valor inválido esperado para demo:
    - Prueba Incorrecta
    """

    login_page = LoginPage(driver)
    base_page = BasePage(driver)

    login_page.load(BASE_URL)
    login_page.login(email=EMAIL, password=PASSWORD)

    for marker in VALID_DEMO_MARKERS:
        elements = driver.find_elements(
            By.XPATH,
            f"//*[normalize-space()='{marker}']"
        )

        if elements:
            return

    raise AssertionError(
        "No se encontró un marcador válido de demo. "
        f"Valores aceptados: {VALID_DEMO_MARKERS}. "
        "Esto simula una regresión bloqueada por el Quality Gate."
    )
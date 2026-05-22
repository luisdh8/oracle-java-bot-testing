from config.settings import BASE_URL, EMAIL, PASSWORD
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    login_page.load(BASE_URL)
    login_page.login(email=EMAIL, password=PASSWORD)

    wait = WebDriverWait(driver, 20)

    # 1. Esperar a que el dashboard esté cargado.
    wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//h2[normalize-space()='Vista General']"
            )
        )
    )

    # 2. Esperar a que aparezca uno de los marcadores válidos.
    valid_marker_xpath = (
        "//*[normalize-space()='Prueba Correcta' "
        "or normalize-space()='Prueba Correcta 2']"
    )

    try:
        wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    valid_marker_xpath
                )
            )
        )
    except Exception:
        raise AssertionError(
            "No se encontró un marcador válido de demo. "
            f"Valores aceptados: {VALID_DEMO_MARKERS}. "
            "Esto simula una regresión bloqueada por el Quality Gate."
        )

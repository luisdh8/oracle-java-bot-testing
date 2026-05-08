from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    """
    Clase base para todos los Page Objects.
    Centraliza lógica común: esperas, selectores, operaciones MUI.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(
            driver,
            10,
            ignored_exceptions=(StaleElementReferenceException,),
        )
        self.actions = ActionChains(driver)

    def find_clickable(self, locator):
        """Espera a que un elemento sea clickeable y lo retorna"""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def find_visible(self, locator):
        """Espera a que un elemento sea visible y lo retorna"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_present(self, locator):
        """Espera a que un elemento esté presente en el DOM"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        """Click seguro con espera"""
        self.find_clickable(locator).click()

    def send_keys(self, locator, text):
        """Enviar texto a un input con espera"""
        element = self.find_visible(locator)
        element.send_keys(text)

    def clear_and_send_keys(self, locator, text):
        """Limpiar input y enviar texto"""
        element = self.find_visible(locator)
        element.clear()
        element.send_keys(text)

    def select_dropdown_mui(self, trigger_locator, option_text):
        """
        Maneja dropdowns MUI (combobox):
        1. Click en el trigger (div role="combobox")
        2. Espera a que se abra
        3. Selecciona opción por texto

        Args:
            trigger_locator: tuple (By, selector) del combobox
            option_text: texto exacto o parcial de la opción
        """
        # Click en el combobox para abrir
        self.click(trigger_locator)

        # Esperar y click en opción visible del menú abierto
        option_locator = (
            By.XPATH,
            (
                "//li[@role='option' and "
                f"(normalize-space()='{option_text}' or contains(normalize-space(), '{option_text}'))]"
            ),
        )
        self.click(option_locator)

    def assert_element_visible(self, locator, message="Elemento no visible"):
        """Valida que elemento esté visible (util para assertions)"""
        element = self.find_visible(locator)
        assert element is not None, message
        return element

    def assert_element_present(self, locator, message="Elemento no presente"):
        """Valida que elemento esté en el DOM"""
        element = self.find_present(locator)
        assert element is not None, message
        return element

    def get_element_text(self, locator):
        """Obtiene texto de un elemento"""
        return self.find_visible(locator).text

    def scroll_to_element(self, locator):
        """Scroll hasta un elemento"""
        element = self.find_present(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

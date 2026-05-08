from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class LoginPage(BasePage):
    ERROR_LOCATORS = [
        (By.XPATH, "//*[@role='alert' and normalize-space()]"),
        (By.XPATH, "//*[contains(@class, 'MuiAlert-message') and normalize-space()]"),
        (By.XPATH, "//div[contains(@class, 'error') and normalize-space()]"),
        (By.XPATH, "//p[contains(@class, 'error') and normalize-space()]"),
        (By.XPATH, "//*[contains(normalize-space(), 'Request failed with status code 500')]"),
    ]

    def load(self, url):
        self.driver.get(url)

    def login(self, email, password):
        self.send_keys((By.NAME, "email"), email)
        self.send_keys((By.NAME, "password"), password)
        self.click((By.CSS_SELECTOR, "button[type='submit']"))

    def _get_first_visible_error_element(self):
        for locator in self.ERROR_LOCATORS:
            for element in self.driver.find_elements(*locator):
                if element.is_displayed() and element.text.strip():
                    return element
        return None

    def get_visible_error_text(self, timeout=10):
        """Espera y retorna el texto del primer error visible en pantalla."""
        element = WebDriverWait(self.driver, timeout).until(
            lambda _: self._get_first_visible_error_element()
        )
        return element.text.strip()

    def is_error_visible(self, expected_text=None):
        """Retorna True si hay error visible; opcionalmente valida texto contenido."""
        element = self._get_first_visible_error_element()
        if not element:
            return False

        if expected_text:
            return expected_text in element.text
        return True
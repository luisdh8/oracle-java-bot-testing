"""
Utilidades y helpers para tests E2E.
"""

import logging
from datetime import datetime


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class TestLogger:
    """Helper para logging consistente en tests"""

    @staticmethod
    def log_test_start(test_name):
        logger.info(f"▶ Iniciando: {test_name}")

    @staticmethod
    def log_test_step(step_description):
        logger.info(f"  ├─ {step_description}")

    @staticmethod
    def log_test_validation(validation_description):
        logger.info(f"  ├─ ✓ Validación: {validation_description}")

    @staticmethod
    def log_test_end(test_name, status="PASSED"):
        logger.info(f"◀ {status}: {test_name}\n")

    @staticmethod
    def log_error(error_message):
        logger.error(f"  ✗ ERROR: {error_message}")


class WaitUtils:
    """Utilidades para esperas avanzadas"""

    @staticmethod
    def wait_for_element_to_disappear(driver, locator, timeout=10):
        """
        Espera a que un elemento desaparezca del DOM o sea invisible.

        Args:
            driver: Selenium WebDriver
            locator: Tuple (By, selector)
            timeout: Tiempo máximo de espera en segundos
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    @staticmethod
    def wait_for_url_change(driver, original_url, timeout=10):
        """
        Espera a que la URL cambie.

        Args:
            driver: Selenium WebDriver
            original_url: URL original
            timeout: Tiempo máximo de espera
        """
        from selenium.webdriver.support.ui import WebDriverWait

        WebDriverWait(driver, timeout).until(
            lambda d: d.current_url != original_url
        )


class DataValidationUtils:
    """Utilidades para validación de datos en tests"""

    @staticmethod
    def is_valid_email(email):
        """Valida formato de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_datetime(date_string):
        """Valida formato ISO de fecha"""
        try:
            datetime.fromisoformat(date_string)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_timestamp_string():
        """Retorna timestamp para datos únicos"""
        return datetime.now().strftime("%Y%m%d%H%M%S")

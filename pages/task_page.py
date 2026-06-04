from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class TaskPage(BasePage):
    TASKS_LINK = (
        By.XPATH,
        "//aside[contains(@class, 'nav-quick-rail')]//a[@aria-label='Tareas' or @href='/tareas']",
    )
    NEW_TASK_BUTTON = (By.XPATH, "//button[contains(., 'Nueva tarea')]")
    MODAL = (By.XPATH, "//div[@role='dialog']")
    PROJECT_COMBOBOX = (
        By.XPATH,
        (
            "//div[@role='dialog']//div[@role='combobox' and "
            "(@id='mui-component-select-projectId' or "
            "@aria-labelledby='mui-component-select-projectId' or "
            "following-sibling::input[@name='projectId'])]"
        ),
    )
    PRIORITY_COMBOBOX = (
        By.XPATH,
        (
            "//div[@role='dialog']//div[@role='combobox' and "
            "(@id='mui-component-select-prioridadId' or "
            "@aria-labelledby='mui-component-select-prioridadId' or "
            "following-sibling::input[@name='prioridadId'])]"
        ),
    )
    SUBMIT_BUTTON = (
        By.XPATH,
        "//div[@role='dialog']//button[@type='submit' and contains(., 'Agregar Tarea')]",
    )
    REJECTION_FEEDBACK_LOCATORS = [
        (By.XPATH, "//*[@role='alert' and normalize-space()]"),
        (By.XPATH, "//*[contains(@class, 'MuiAlert-message') and normalize-space()]"),
        (By.XPATH, "//p[contains(@class, 'error') and normalize-space()]"),
        (By.XPATH, "//div[contains(@class, 'error') and normalize-space()]"),
    ]

    def go_to_tasks(self):
        """Navega a la sección de Tareas usando el navbar rápido."""
        self.click(self.TASKS_LINK)

    def open_new_task_modal(self):
        """Abre el modal de nueva tarea usando selectores específicos"""
        self.click(self.NEW_TASK_BUTTON)
        self.find_visible(self.MODAL)

    def _find_first_visible(self, locators):
        """Retorna el primer locator visible de la lista o lanza TimeoutException."""
        last_error = None
        for locator in locators:
            try:
                return self.find_visible(locator)
            except TimeoutException as error:
                last_error = error
        raise last_error if last_error else TimeoutException("No se encontró elemento visible")

    def _clear_and_type(self, locators, value):
        element = self._find_first_visible(locators)
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        if value:
            element.send_keys(value)
        return element

    def _get_first_visible_element(self, locators):
        for locator in locators:
            for element in self.driver.find_elements(*locator):
                if element.is_displayed():
                    return element
        return None

    def _set_datetime_local(self, value):
        date_input = self._find_first_visible(
            [
                (By.XPATH, "//div[@role='dialog']//input[@name='fechaLimite']"),
                (By.XPATH, "//div[@role='dialog']//input[@type='datetime-local']"),
            ]
        )

        self.driver.execute_script(
            """
            const input = arguments[0];
            const value = arguments[1];
            const nativeSetter = Object.getOwnPropertyDescriptor(
              window.HTMLInputElement.prototype,
              'value'
            ).set;
            input.focus();
            nativeSetter.call(input, value);
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            input.blur();
            """,
            date_input,
            value,
        )

        current_value = date_input.get_attribute("value")
        if current_value != value:
            date_input.click()
            date_input.send_keys(Keys.CONTROL, "a")
            date_input.send_keys(Keys.DELETE)
            date_input.send_keys(value)

    def fill_form(self, title="Test Selenium", description="test case",
                  project="Oracle Java Bot", priority="Media", deadline="2026-05-26T17:00",
                  estimated_time="1"):
        """
        Llena el formulario de nueva tarea.

        Args:
            title: Título de la tarea
            description: Descripción
            project: Nombre del proyecto
            priority: Nivel de prioridad
            deadline: Fecha límite (formato ISO)
            estimated_time: Tiempo estimado en horas
        """
        self.find_visible(self.MODAL)

        # Proyecto
        self.select_dropdown_mui(self.PROJECT_COMBOBOX, project)

        # Título
        self._clear_and_type(
            [
                (By.XPATH, "//div[@role='dialog']//input[@name='titulo']"),
                (By.XPATH, "//div[@role='dialog']//input[@name='title']"),
                (By.XPATH, "//div[@role='dialog']//input[contains(@placeholder, 'Título')]"),
            ],
            title,
        )

        # Descripción
        self._clear_and_type(
            [
                (By.XPATH, "//div[@role='dialog']//textarea[@name='descripcion']"),
                (By.XPATH, "//div[@role='dialog']//textarea[@name='description']"),
                (By.XPATH, "//div[@role='dialog']//*[self::textarea or self::input][contains(@placeholder, 'Descripción')]"),
            ],
            description,
        )

        # Fecha (datetime-local en formato ISO)
        self._set_datetime_local(deadline)

        # Tiempo estimado
        self._clear_and_type(
            [
                (By.XPATH, "//div[@role='dialog']//input[@name='tiempoEstimado']"),
                (By.XPATH, "//div[@role='dialog']//input[@name='estimatedTime']"),
                (By.XPATH, "//div[@role='dialog']//input[contains(@placeholder, 'Tiempo Estimado')]"),
            ],
            estimated_time,
        )

        # Prioridad
        self.select_dropdown_mui(self.PRIORITY_COMBOBOX, priority)

    def submit(self):
        """Envía el formulario usando el botón 'Agregar Tarea'"""
        self.click(self.SUBMIT_BUTTON)

    def is_modal_open(self):
        """Retorna True si el modal de nueva tarea sigue visible."""
        return self._get_first_visible_element([self.MODAL]) is not None

    def is_task_visible_by_title(self, title):
        """Retorna True si la tarjeta de tarea con ese título está visible en el tablero."""
        locator = (
            By.XPATH,
            f"//p[contains(@class, 'tarea-titulo') and normalize-space()='{title}']",
        )
        for element in self.driver.find_elements(*locator):
            if element.is_displayed():
                return True
        return False

    def get_rejection_feedback_text(self):
        """Retorna texto visible de rechazo si existe; de lo contrario None."""
        element = self._get_first_visible_element(self.REJECTION_FEEDBACK_LOCATORS)
        if not element:
            return None

        text = element.text.strip()
        return text or None

    def wait_for_optional_rejection_signal(self, timeout=5):
        """Espera señal de rechazo y retorna estado; no falla si no aparece."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda _: self.is_modal_open() or self.get_rejection_feedback_text() is not None
            )
        except TimeoutException:
            return None

        return {
            "modal_open": self.is_modal_open(),
            "feedback_text": self.get_rejection_feedback_text(),
        }

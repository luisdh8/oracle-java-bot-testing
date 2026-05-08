from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """
    Page Object para el dashboard del sistema.
    """

    def verify_dashboard_loaded(self):
        """
        Verifica que el dashboard esté completamente cargado.
        Valida la presencia del botón de navegación.
        """
        # Buscar el botón de toggle del menú (nav-toggle-btn)
        return self.find_present(
            (By.XPATH, "//button[@class='nav-toggle-btn']"),
        )

    def get_user_name(self):
        """Obtiene el nombre del usuario actual del dashboard"""
        # Ajusta el selector según tu aplicación
        return self.get_element_text((By.XPATH, "//div[@role='button']//p[1]"))

    def verify_nav_menu_visible(self):
        """Verifica que el botón de navegación está presente"""
        return self.find_present(
            (By.XPATH, "//button[@class='nav-toggle-btn']")
        )

    def toggle_nav_menu(self):
        """Abre/cierra el menú de navegación"""
        self.click((By.XPATH, "//button[@class='nav-toggle-btn']"))

    def verify_project_in_progress(self, project_name="Oracle Java Bot"):
        """
        Verifica que un proyecto aparezca en la sección "Proyectos en curso".
        """
        return self.assert_element_visible(
            (
                By.XPATH,
                (
                    "//div[contains(@class, 'page-section')]"
                    "[.//span[normalize-space()='Proyectos en curso']]"
                    f"//tbody//td[contains(@class, 'cell-primary') and normalize-space()='{project_name}']"
                ),
            ),
            message=f"No se encontró el proyecto en curso '{project_name}' en dashboard",
        )

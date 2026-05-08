from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time


class ProjectsPage(BasePage):
    """Page Object para la sección de Proyectos"""

    # Localizadores centralizados
    TEAM_COMBOBOX = (By.XPATH, "(//div[@role='combobox'])[1]")
    PROJECT_COMBOBOX = (By.XPATH, "(//div[@role='combobox'])[2]")

    def go_to_projects(self):
        """Navega a la sección de Proyectos, abriendo el menú si es necesario"""
        try:
            self.click((By.XPATH, "//span[text()='Proyectos']"))
        except:
            # Si falla, probablemente el menú está cerrado
            # Abre el menú de navegación
            self.click((By.XPATH, "//button[@class='nav-toggle-btn']"))
            time.sleep(0.5)
            # Intentar nuevamente
            self.click((By.XPATH, "//span[text()='Proyectos']"))

    def filter_by_team(self, team_name):
        """
        Filtra proyectos por equipo usando el primer combobox.

        Args:
            team_name: Nombre del equipo (ej: "Equipo 43")
        """
        self.select_dropdown_mui(self.TEAM_COMBOBOX, team_name)

    def select_project_dashboard(self, project_name):
        """
        Selecciona un proyecto del dashboard usando el segundo combobox.

        Args:
            project_name: Nombre del proyecto
        """
        self.select_dropdown_mui(self.PROJECT_COMBOBOX, project_name)

    def verify_dashboard_loaded(self, project_name):
        """
        Verifica que el dashboard se haya cargado con el proyecto especificado.

        Args:
            project_name: Nombre del proyecto esperado

        Returns:
            Element si está visible, raises exception si no
        """
        return self.assert_element_visible(
            (By.XPATH, f"//span[text()='{project_name}']"),
            message=f"Dashboard para proyecto '{project_name}' no cargó"
        )

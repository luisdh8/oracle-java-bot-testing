from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProjectsPage(BasePage):
    """Page Object para la sección de Proyectos"""

    # Localizadores centralizados
    TEAM_COMBOBOX = (By.XPATH, "(//div[@role='combobox'])[1]")
    PROJECT_COMBOBOX = (By.XPATH, "(//div[@role='combobox'])[2]")
    PROJECTS_LINK = (
        By.XPATH,
        "//aside[contains(@class, 'nav-quick-rail')]//a[@aria-label='Proyectos' or @href='/proyectos']",
    )

    def go_to_projects(self):
        """Navega a la sección de Proyectos usando el navbar rápido."""
        self.click(self.PROJECTS_LINK)

    def filter_by_team(self, team_name):
        """
        Filtra proyectos por equipo usando el primer combobox.

        Args:
            team_name: Nombre del equipo (ej: "Equipo 43")
        """
        self.select_dropdown_mui(self.TEAM_COMBOBOX, team_name)

    def select_project_dashboard(self, project_name):
        """
        Selecciona un proyecto desde la tarjeta correspondiente.

        Args:
            project_name: Nombre del proyecto
        """
        card_locator = (
            By.XPATH,
            (
                "//section[contains(@class, '_section_')]"
                f"//button[contains(@class, '_card_')][.//h3[normalize-space()='{project_name}']]"
            ),
        )
        self.click(card_locator)

    def verify_dashboard_loaded(self, project_name):
        """
        Verifica que el dashboard se haya cargado con el proyecto especificado.

        Args:
            project_name: Nombre del proyecto esperado

        Returns:
            Element si está visible, raises exception si no
        """
        return self.assert_element_visible(
            (By.XPATH, f"//h2[normalize-space()='{project_name}']"),
            message=f"Dashboard para proyecto '{project_name}' no cargó"
        )

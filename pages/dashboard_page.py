from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """
    Page Object para el dashboard del sistema.
    """

    def verify_dashboard_loaded(self):
        """
        Verifica que el dashboard esté cargado.

        La versión actual del frontend muestra:
        - Encabezado "Vista General"
        - Subtítulo "Resumen del proyecto"
        - Sección "Proyectos en curso"
        """
        return self.find_present(
            (
                By.XPATH,
                "//h2[normalize-space()='Resumen' or normalize-space()='Vista General']"
            )
        )

    def get_user_name(self):
        """
        Obtiene el email o identificador del usuario visible en el menú lateral.
        """
        return self.get_element_text(
            (
                By.CSS_SELECTOR,
                ".nav-rail-email"
            )
        )

    def verify_nav_menu_visible(self):
        """
        Verifica que el menú lateral principal esté presente.
        """
        return self.find_present(
            (
                By.CSS_SELECTOR,
                "aside.nav-quick-rail[role='navigation']"
            )
        )

    def verify_nav_link_visible(self, label):
        """
        Verifica que exista un link de navegación por su aria-label.
        Ejemplos: Inicio, Tareas, Agent, Proyectos, Equipos.
        """
        return self.find_present(
            (
                By.XPATH,
                f"//aside[contains(@class, 'nav-quick-rail')]"
                f"//a[@aria-label='{label}']"
            )
        )

    def verify_project_in_progress(self, project_name="Oracle Java Bot"):
        """
        Verifica que un proyecto aparezca en la sección 'Proyectos en curso'.
        """
        return self.assert_element_visible(
            (
                By.XPATH,
                (
                    "//div[contains(@class, 'page-section')]"
                    "[.//span[normalize-space()='Proyectos en curso']]"
                    f"//tbody//td[contains(@class, 'cell-primary') "
                    f"and normalize-space()='{project_name}']"
                ),
            ),
            message=f"No se encontró el proyecto en curso '{project_name}' en dashboard",
        )

    def verify_dashboard_kpi_visible(self, kpi_name):
        """
        Verifica que una métrica/KPI esté visible en el dashboard.
        Ejemplos:
        - Avg General Progress
        - Avg Sprint Completion
        - Avg On-Time Delivery
        - Avg Estimation Precision
        - Total Active Tasks
        """
        return self.find_present(
            (
                By.XPATH,
                f"//*[normalize-space()='{kpi_name}']"
            )
        )

    def verify_chart_visible(self, chart_title):
        """
        Verifica que una gráfica esté visible por su título.
        Ejemplos:
        - Delivery Health
        - Estimation vs Real (hrs)
        - Resource Workload / Productivity
        """
        return self.find_present(
            (
                By.XPATH,
                f"//h3[normalize-space()='{chart_title}']"
            )
        )

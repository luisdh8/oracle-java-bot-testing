from config.settings import BASE_URL
from pages.login_page import LoginPage
from pages.projects_page import ProjectsPage


def test_projects_dashboard_filter(authenticated_driver, valid_project_filter):
    """TC-04: Navegar a proyectos, filtrar por equipo y seleccionar proyecto"""
    driver = authenticated_driver
    projects_page = ProjectsPage(driver)

    # Extraer datos del fixture
    team_name = valid_project_filter["team"]
    project_name = valid_project_filter["project"]

    # Navegar a Proyectos
    projects_page.go_to_projects()

    # Filtrar por equipo
    projects_page.filter_by_team(team_name)

    # Seleccionar proyecto
    projects_page.select_project_dashboard(project_name)

    # Validación: dashboard del proyecto cargado
    projects_page.verify_dashboard_loaded(project_name)

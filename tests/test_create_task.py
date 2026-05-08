import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.task_page import TaskPage


@pytest.mark.smoke
def test_create_task_success(authenticated_driver, valid_task_data):
    """TC-03: Crear tarea válida y validar que aparezca en el tablero."""
    driver = authenticated_driver
    task_page = TaskPage(driver)
    task_title = valid_task_data["title"]

    task_page.go_to_tasks()
    task_page.open_new_task_modal()
    task_page.fill_form(
        title=valid_task_data["title"],
        description=valid_task_data["description"],
        project=valid_task_data["project"],
        priority=valid_task_data["priority"],
        deadline=valid_task_data["deadline"],
        estimated_time=valid_task_data["estimated_time"],
    )
    task_page.submit()

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//p[contains(@class, 'tarea-titulo') and normalize-space()='{task_title}']")
        )
    )

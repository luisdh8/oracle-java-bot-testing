import os
import sys
import shutil
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import pytest
from utils.driver import get_driver
from config.settings import BASE_URL, EMAIL, PASSWORD
from pages.login_page import LoginPage
from utils.test_data import TestDataFactory, TaskTestData, ProjectTestData, NegativeTestData
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver():
    """Fixture centralizado: crea y limpia driver"""
    driver = get_driver()
    yield driver
    driver.quit()


@pytest.fixture
def authenticated_driver(driver):
    """Fixture: driver ya autenticado (login previo)"""
    login_page = LoginPage(driver)
    login_page.load(BASE_URL)
    login_page.login(EMAIL, PASSWORD)

    # Esperar a que la autenticación sea completa (token en localStorage)
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return localStorage.getItem('token') !== null")
    )

    yield driver
    driver.quit()


@pytest.fixture
def wait(driver):
    """Fixture: WebDriverWait configurado por defecto"""
    return WebDriverWait(driver, 10)


# Fixtures de datos de prueba
@pytest.fixture
def valid_task_data():
    """Proporciona datos válidos para crear una tarea"""
    return TaskTestData.valid_task()


@pytest.fixture
def valid_project_filter():
    """Proporciona filtros válidos para proyectos"""
    return ProjectTestData.valid_filter()


@pytest.fixture
def test_data_factory():
    """Proporciona acceso directo a TestDataFactory para personalización"""
    return TestDataFactory


@pytest.fixture
def invalid_login_data():
    """Proporciona credenciales inválidas para login negativo"""
    return NegativeTestData.invalid_login()


@pytest.fixture
def invalid_task_past_deadline():
    """Proporciona payload inválido por fecha en el pasado"""
    return NegativeTestData.task_with_past_deadline()


@pytest.fixture
def invalid_task_huge_hours():
    """Proporciona payload inválido por horas excesivas"""
    return NegativeTestData.task_with_huge_hours()


@pytest.fixture
def invalid_task_negative_hours():
    """Proporciona payload inválido por horas negativas"""
    return NegativeTestData.task_with_negative_hours()


def pytest_sessionfinish(session, exitstatus):
    """Limpia artefactos de caché al terminar la ejecución."""
    root = Path(__file__).resolve().parent
    for path in root.rglob("*"):
        if path.is_dir() and path.name in {"__pycache__", ".pytest_cache"}:
            shutil.rmtree(path, ignore_errors=True)

"""
Módulo de generación de datos de prueba dinámicos.
Evita hardcoding y colisiones entre tests.
"""

import random
import string
from datetime import datetime, timedelta


class TestDataFactory:
    """Factory para generar datos de prueba únicos y válidos"""

    @staticmethod
    def generate_unique_title(prefix="Test Task"):
        """
        Genera títulos únicos para tareas.

        Returns:
            str: ej. "Test Task - ABC123"
        """
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"{prefix} - {random_suffix}"

    @staticmethod
    def generate_unique_email(base_email="test"):
        """
        Genera emails únicos para testing.

        Args:
            base_email: parte del email antes del @

        Returns:
            str: ej. "test.abc123xyz@example.com"
        """
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{base_email}.{random_suffix}@example.com"

    @staticmethod
    def generate_future_date(days_ahead=7, include_time=True, before_5pm=False):
        """
        Genera fechas futuras válidas para límites.

        Args:
            days_ahead: días en el futuro
            include_time: si incluye hora (formato ISO con T)
            before_5pm: si True, genera horas entre 08:00-16:59

        Returns:
            str: ej. "2026-04-26" o "2026-04-26T17:00" o "2026-04-26T14:35"
        """
        future_date = datetime.now() + timedelta(days=days_ahead)

        if include_time:
            if before_5pm:
                # Generar hora entre 08:00 y 16:59
                hour = random.randint(8, 16)
                minute = random.randint(0, 59)
                return future_date.strftime(f"%Y-%m-%dT{hour:02d}:{minute:02d}")
            return future_date.strftime("%Y-%m-%dT%H:00")
        return future_date.strftime("%Y-%m-%d")

    @staticmethod
    def generate_description(base="Automated test case"):
        """
        Genera descripciones únicas.

        Returns:
            str: ej. "Automated test case - ABC123"
        """
        random_suffix = ''.join(random.choices(string.ascii_uppercase, k=4))
        return f"{base} - {random_suffix}"

    @staticmethod
    def get_valid_project():
        """Retorna proyecto válido disponible en el sistema"""
        return "Oracle Java Bot"

    @staticmethod
    def get_valid_priority():
        """Retorna prioridad válida"""
        return "Media"

    @staticmethod
    def get_valid_team():
        """Retorna equipo válido disponible"""
        return "Equipo 43"

    @staticmethod
    def get_estimated_hours():
        """Retorna horas estimadas válidas (1-8)"""
        return str(random.randint(1, 8))


# Datos de prueba comúnmente usados
VALID_PROJECTS = ["Oracle Java Bot", "Proyecto Backend", "Frontend React"]
VALID_PRIORITIES = ["Baja", "Media", "Alta"]
VALID_TEAMS = ["Equipo 43", "Equipo 44", "Equipo 45"]
ESTIMATED_HOURS_RANGE = range(1, 9)  # 1-8 horas


# Fixture de datos para tests
class TaskTestData:
    """Datos pre-configurados para tests de tareas"""

    @staticmethod
    def valid_task():
        """Tarea válida con datos dinámicos"""
        return {
            "title": TestDataFactory.generate_unique_title("Tarea Selenium"),
            "description": TestDataFactory.generate_description("Test automatizado"),
            "project": "Oracle Java Bot",
            "priority": "Media",
            "deadline": TestDataFactory.generate_future_date(days_ahead=5, include_time=True, before_5pm=True),
            "estimated_time": TestDataFactory.get_estimated_hours()
        }


# Fixture de datos para projects
class ProjectTestData:
    """Datos pre-configurados para tests de proyectos"""

    @staticmethod
    def valid_filter():
        """Filtro válido para proyectos"""
        return {
            "team": "Equipo 43",
            "project": "Oracle Java Bot"
        }


class NegativeTestData:
    """Datos pre-configurados para escenarios negativos"""

    @staticmethod
    def invalid_login():
        """Credenciales inválidas para login"""
        return {
            "email": "invalid.user@example.com",
            "password": "invalid-password",
            "expected_error": "Usuario no encontrado",
        }

    @staticmethod
    def task_with_past_deadline():
        """Tarea inválida por fecha límite en el pasado"""
        data = TaskTestData.valid_task()
        data["title"] = TestDataFactory.generate_unique_title("Negativa Fecha")
        data["deadline"] = "1970-06-12T11:00"
        return data

    @staticmethod
    def task_with_huge_hours():
        """Tarea inválida por tiempo estimado excesivo"""
        data = TaskTestData.valid_task()
        data["title"] = TestDataFactory.generate_unique_title("Negativa Horas Max")
        data["estimated_time"] = "10000000"
        return data

    @staticmethod
    def task_with_negative_hours():
        """Tarea inválida por tiempo estimado negativo"""
        data = TaskTestData.valid_task()
        data["title"] = TestDataFactory.generate_unique_title("Negativa Horas Neg")
        data["estimated_time"] = "-10"
        return data

# Sprint 2 (Quality)

## Instalacion rapida
1. Crear y activar entorno virtual.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

2. Instalar dependencias.

```bash
pip install -r requirements.txt
```

3. Configurar archivo .env en la raiz del proyecto.

```env
BASE_URL=http://159.54.133.243:8080
EMAIL=tu_email@example.com
PASSWORD=tu_password
BROWSER=brave
HEADLESS=false
```

## Tarea para miembros del equipo
Escribir 4 casos de prueba automatizados con Selenium WebDriver.

## Casos de prueba del Sprint (4)
1. Login exitoso: tests/test_login.py::test_login_success
2. Dashboard visible despues de login: tests/test_dashboard.py::test_dashboard_visible_after_login
3. Crear tarea valida: tests/test_create_task.py::test_create_task_success
4. Filtro de proyectos y acceso a dashboard: tests/test_projects.py::test_projects_dashboard_filter

## Ejecucion
Ejecutar los 4 casos requeridos por la actividad:

```bash
pytest tests/test_login.py tests/test_dashboard.py tests/test_create_task.py tests/test_projects.py -v
```

Ejecutar toda la suite del proyecto:

```bash
pytest -v
```

Opcional (suite negativa implementada en Sprint 2):

```bash
pytest tests/negative -v
```

## Resultado esperado
Un conjunto de 4 casos de prueba cubriendo las funcionalidades clave del desarrollo para el reto (Delivery 2).

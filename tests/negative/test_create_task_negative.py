import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from pages.task_page import TaskPage


@pytest.mark.negative
@pytest.mark.ui
@pytest.mark.parametrize(
    "task_fixture_name",
    [
        "invalid_task_past_deadline",
        "invalid_task_huge_hours",
        "invalid_task_negative_hours",
    ],
    ids=["past_deadline", "huge_estimated_hours", "negative_estimated_hours"],
)
def test_create_task_invalid_data_rejected(authenticated_driver, request, task_fixture_name):
    """TC-N02..N04: Inputs inválidos no deben crear una nueva tarea."""
    driver = authenticated_driver
    task_page = TaskPage(driver)
    invalid_task_data = request.getfixturevalue(task_fixture_name)
    task_title = invalid_task_data["title"]

    task_page.go_to_tasks()
    task_page.open_new_task_modal()
    task_page.fill_form(
        title=invalid_task_data["title"],
        description=invalid_task_data["description"],
        project=invalid_task_data["project"],
        priority=invalid_task_data["priority"],
        deadline=invalid_task_data["deadline"],
        estimated_time=invalid_task_data["estimated_time"],
    )
    task_page.submit()

    rejection_signal = task_page.wait_for_optional_rejection_signal(timeout=6)

    with pytest.raises(TimeoutException):
        WebDriverWait(driver, 6).until(
            lambda _: task_page.is_task_visible_by_title(task_title)
        )

    assert not task_page.is_task_visible_by_title(task_title), (
        "Se creó una tarea cuando se esperaba rechazo para input inválido: "
        f"{task_fixture_name}"
    )

    if rejection_signal and rejection_signal["feedback_text"] is not None:
        assert rejection_signal["feedback_text"], "El feedback de rechazo visible no debe estar vacío"

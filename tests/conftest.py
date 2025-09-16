"""Фикстуры для тестов."""

from pathlib import Path
import pytest


@pytest.fixture
def sample_csv(tmp_path: Path):
    """Создаёт временный CSV-файл со студентами."""
    csv_path = tmp_path / "students.csv"
    csv_content = (
        "student_name,subject,teacher_name,date,grade\n"
        "Иванов Иван,Математика,Петрова,2023-10-10,5\n"
        "Петров Петр,Математика,Сидорова,2023-10-10,4\n"
        "Сидоров Сид,Математика,Иванова,2023-10-10,3\n"
    )
    csv_path.write_text(csv_content, encoding="utf-8")
    return csv_path

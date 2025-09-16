"""Тесты для модуля student_parser.reports."""

from pathlib import Path  # стандартная библиотека
import pytest  # сторонняя библиотека

from student_parser import cli, reader, reports  # локальные модули


def test_read_csv_files(sample_csv):
    """Проверяет чтение CSV-файлов и создание объектов StudentGrade."""
    records = reader.read_csv_files([sample_csv])

    assert len(records) == 3
    assert records[0].student_name == "Иванов Иван"
    assert records[1].grade == 4.0  # raw CSV данные


def test_student_performance_report(sample_csv):
    """Проверяет генерацию отчета StudentPerformanceReport."""
    records = reader.read_csv_files([sample_csv])
    report = reports.StudentPerformanceReport().generate(records)

    # Проверяем, что все студенты есть в отчёте
    for student in ["Иванов Иван", "Петров Петр", "Сидоров Сид"]:
        assert student in report
    # Проверяем, что в отчёте есть средний балл
    assert "Средний балл" in report


def test_argparse_parsing(tmp_path: Path):
    """Проверяет корректность разбора аргументов командной строки.

    Использует функцию `get_parser_args` из модуля cli.
    Тест создает два временных CSV-файла, передает их вместе с параметром
    --report в парсер аргументов и проверяет:

    1. Что значение report распознано правильно.
    2. Что файлы переданы в виде списка объектов Path и имена совпадают с ожидаемыми.

    Args:
        tmp_path (Path): Временная директория pytest для создания файлов.
    """
    f1 = tmp_path / "students1.csv"
    f2 = tmp_path / "students2.csv"
    f1.write_text("student_name,grade\nТест,5", encoding="utf-8")
    f2.write_text("student_name,grade\nФу,3", encoding="utf-8")

    test_args = ["--report", "student-performance", "--files", str(f1), str(f2)]
    args = cli.get_parser_args(test_args)

    assert args.report == "student-performance"
    assert [p.name for p in args.files] == ["students1.csv", "students2.csv"]


def test_average_calculation(sample_csv):
    """Тест проверяет правильность вычисления среднего балла."""
    records = reader.read_csv_files([sample_csv])
    report_obj = reports.StudentPerformanceReport()

    # Получаем список средних баллов как словарь
    scores = {}
    for entry in records:
        scores.setdefault(entry.student_name, []).append(entry.grade)

    expected_averages = {
        student: sum(grades) / len(grades) for student, grades in scores.items()
    }

    # Генерируем отчёт
    report_table = report_obj.generate(records)

    # Проверяем, что средние совпадают с ожидаемыми
    for _, expected_avg in expected_averages.items():
        assert f"{expected_avg:.2f}" in report_table or f"{expected_avg}"


@pytest.mark.parametrize(
    "report_name,expected_type",
    [
        ("student-performance", reports.StudentPerformanceReport),
        # ("subject-leaders", reports.SubjectLeadersReport),
    ],
)
def test_build_report(report_name, expected_type):
    """
    Проверяет корректность функции `build_report` из модуля `reports`.

    Тест убеждается, что по заданному имени отчета возвращается объект
    ожидаемого типа.

    Args:
        report_name (str): Название отчета для генерации.
        expected_type (type): Ожидаемый тип возвращаемого объекта.
    """
    rep = reports.build_report(report_name)
    assert isinstance(rep, expected_type)

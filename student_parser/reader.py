"""
Модуль для чтения CSV-файлов с данными студентов.

Содержит функцию read_csv_files, которая создает список объектов StudentGrade
из CSV-файлов.
"""

import csv
from pathlib import Path
from typing import List
from .models import StudentGrade


def read_csv_files(file_paths: list[str]) -> List[StudentGrade]:
    """
    Читает CSV-файлы со студентами и возвращает список StudentGrade.

    Args:
        paths (list[Path]): Список путей к CSV-файлам.

    Returns:
        list[StudentGrade]: Список объектов с информацией о студенте.
    """
    records: List[StudentGrade] = []
    for path in file_paths:
        file = Path(path)
        if not file.exists():
            raise FileNotFoundError(f"Файл не найден: {path}")

        with file.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(
                    StudentGrade(
                        student_name=row["student_name"],
                        subject=row["subject"],
                        teacher_name=row["teacher_name"],
                        date=row["date"],
                        grade=float(row["grade"]),
                    )
                )
    return records

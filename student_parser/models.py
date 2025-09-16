"""Модуль с моделями данных проекта student_parser."""

from dataclasses import dataclass


@dataclass
class StudentGrade:
    """Класс, описывающий запись о студенте и его оценке."""

    student_name: str
    subject: str
    teacher_name: str
    date: str
    grade: float

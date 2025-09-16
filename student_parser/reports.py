"""
Модуль с реализацией отчетов по студентам.

Содержит абстрактный класс Report и конкретные реализации отчетов,
например, StudentPerformanceReport, а также фабрику build_report для
создания отчетов по имени.
"""

from abc import ABC, abstractmethod
from typing import List
from collections import defaultdict
from tabulate import tabulate
from .models import StudentGrade


class Report(ABC):
    """
    Абстрактный класс для всех отчетов.

    Классы-наследники должны реализовать метод generate, который
    принимает список StudentGrade и возвращает строку с отчетом.
    """

    @abstractmethod
    def generate(self, data: List[StudentGrade]) -> str:
        """
        Генерирует отчет по данным студентов.

        Args:
            data (List[StudentGrade]): Список записей студентов.

        Returns:
            str: Сгенерированный отчет в виде строки.
        """

    pass


class StudentPerformanceReport(Report):
    """
    Отчет с вычислением среднего балла студентов.

    Формирует таблицу с именами студентов и их средним баллом.
    """

    def generate(self, data: List[StudentGrade]) -> str:
        """
        Генерирует таблицу средних баллов студентов.

        Args:
            data (List[StudentGrade]): Список объектов StudentGrade.

        Returns:
            str: Таблица с именами студентов и их средним баллом в формате GitHub.
        """
        scores = defaultdict(list)
        for entry in data:
            scores[entry.student_name].append(float(entry.grade))

        averages = [
            (student, sum(grades) / len(grades)) for student, grades in scores.items()
        ]
        averages.sort(key=lambda x: x[1], reverse=True)

        return tabulate(
            averages, headers=["Студент", "Средний балл"], tablefmt="github"
        )


REPORTS: dict[str, Report] = {
    "student-performance": StudentPerformanceReport(),
}


def build_report(name: str) -> Report:
    """Возвращает объект отчёта по имени."""
    if name not in REPORTS:
        raise ValueError(f"Неизвестный отчёт: {name}")
    return REPORTS[name]

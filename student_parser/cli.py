"""
Модуль для работы с аргументами командной строки проекта.

Содержит функцию get_parser_args, которая парсит аргументы для генерации отчетов.
"""

import argparse
from pathlib import Path
from typing import List

from .reader import read_csv_files
from .reports import REPORTS


def main():
    """
    Основная функция запуска генератора отчетов по студентам.

    Читает CSV-файлы с оценками студентов, проверяет название отчета
    и выводит сгенерированный отчет в консоль.

    Использует:
        - read_csv_files для чтения данных из CSV
        - REPORTS для получения соответствующего отчета

    Пример использования:
        python -m student_parser.cli --files students.csv --report student-performance
    """
    parser = argparse.ArgumentParser(
        description="Генерация отчётов по успеваемости студентов"
    )
    parser.add_argument("--files", nargs="+", required=True, help="CSV файлы с данными")
    parser.add_argument("--report", required=True, help="Название отчёта")

    args = parser.parse_args()

    if args.report not in REPORTS:
        print(f"Неизвестный отчёт: {args.report}")
        print(f"Доступные: {', '.join(REPORTS.keys())}")
        return

    records = read_csv_files(args.files)
    report = REPORTS[args.report]
    print(report.generate(records))


def get_parser_args(args: List[str] = None):
    """
    Парсит аргументы командной строки для генератора отчетов.

    Args:
        args (List[str], optional): Список аргументов для тестирования.
                                    Если None, берутся аргументы из sys.argv.

    Returns:
        argparse.Namespace: Объект с распарсенными аргументами.
    """
    parser = argparse.ArgumentParser(description="Генератор отчетов по студентам")
    parser.add_argument(
        "--report",
        type=str,
        choices=["student-performance"],
        required=True,
        help="Название отчета",
    )
    parser.add_argument(
        "--files", type=Path, nargs="+", required=True, help="CSV файлы со студентами"
    )
    return parser.parse_args(args)


if __name__ == "__main__":
    main()

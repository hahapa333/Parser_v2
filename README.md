# Parser

Скрипт для генерации отчётов об успеваемости студентов.

## Установка
```bash
pip install -r requirements.txt
```

## Запуск
```bash
python -m student_parser.cli --files students1.csv sudents2.csv --report student-performance
```

## Пример вывода
```text
| Студент       |   Средний балл |
|---------------|----------------|
| Иванов Иван   |            4.5 |
| Петров Петр   |            3.0 |
```

## Тесты
```bash
pytest --cov=student_parser
```

## Как добавить новый отчёт
1. Создать новый класс, наследующийся от `Report` в `parser/reports.py`
2. Добавить его в словарь `REPORTS`

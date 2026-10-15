# Лабораторная 1 по дисциплине "Технологии программирования"

Знакомство с системой контроля версий Git и инструментом CI/CD GitHub Actions.

## Постановка задачи

Проект `rating` рассчитывает средний рейтинг студентов по дисциплинам на основе
списка студентов и полученных ими оценок, хранящегося в файле. Проект должен быть
размещён в репозитории GitHub, а его проверка (проверка стиля кода и запуск
модульных тестов) должна выполняться автоматически при каждом пуше в ветку `main`
с помощью GitHub Actions.

## Состав проекта

```
rating
  |----.github
  |     |----workflows
  |           |----github-actions-testing.yml
  |
  |----data
  |     |----data.txt
  |
  |----src
  |     |----CalcRating.py
  |     |----DataReader.py
  |     |----TextDataReader.py
  |     |----Types.py
  |     |----main.py
  |
  |----test
  |     |----test_CalcRating.py
  |     |----test_TextDataReader.py
  |     |----test_main.py
  |
  |----README.md
  |----requirements.txt
```

## Используемые языки, библиотеки и технологии

- Python 3.10;
- `pytest` — модульное тестирование;
- `pycodestyle` — проверка соответствия стандарту PEP8;
- `git` — распределённая система контроля версий;
- GitHub, GitHub Actions — CI (непрерывная интеграция).

## Запуск локально

```text
cd <путь>/rating
conda create -n tplab1-env python=3.10
conda activate tplab1-env
pip install -r requirements.txt
pycodestyle.exe src test
$env:PYTHONPATH = "./:./src"
pytest.exe test
python.exe ./src/main.py -p ./data/data.txt
```

## Непрерывное тестирование

Файл `.github/workflows/github-actions-testing.yml` описывает workflow, который
при пуше в `main` устанавливает Python 3.10, ставит зависимости из
`requirements.txt`, запускает `pycodestyle src test` и `pytest test`.

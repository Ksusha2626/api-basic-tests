# api-basic-tests
Примеры тестов на pytest

### Настройка окружения
- Python 3.9
- Создать и активировать виртуальное окружение
```shell script
python3 -m venv venv
. venv/bin/activate
```
- Установить необходимые пакеты python из requirements.txt:

```shell
pip3 install -r requirements.txt
```

### Запуск
- запуск тестов:
```shell script
py.test {TARGET} -s -v
```
- запуск тестов с allure отчетами:
```shell script
py.test {TARGET} -s -v --alluredir={ALLURE_REPORT_DIR}
```
Где параметры:

TARGET - Пакет или конкретный файл.

ALLURE_REPORT_DIR - директория с allure-отчетами. Будет создана, если не существует.
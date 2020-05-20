# Посчитайте клики по ссылкам
1. Получите доступ к API bit.ly
2. Создайте консольную утилиту, сокращающую ссылки
3. Научите её считать переходы

## How to use
* Создайте виртуальное окружение и активируйте его:
```shell script
~ python3 -m venv env && source env/bin/activate
```
* Обновите pip до последней версии:
```shell script
~ pip install --upgrade pip
```
* Установите зависимости:
```shell script
~ pip install -r requirements.txt
```
* Создайте [token](https://bitly.com/a/oauth_apps):
* Создайте конфигурационный файл и добавьте token:
```shell script
~ nano configuration.yml
```
```
user:
  token: ''
```
* Запустите тесты:
```shell script
~ python3 -m pytest test_script.py [--verbose] --html=report.html
```
* Arguments:
```sh
[--verbose]: increase verbosity
[--html]: generate a HTML report for the test results
```
# Посчитайте клики по ссылкам

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
~ python3 -m pytest test_parser.py -v --html=report.html
```
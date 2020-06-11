# Загрузите в imgur фотографии космоса

![Image](https://dvmn.org/media/lessons/space.jpg)

1. Автоматизируйте сбор фотографий космоса через API (`SpaceX` и `Hubble`)
2. Напишите функцию для скачивания картинок любого формата
3. Подготовьте фотографии к публикации в imgur
4. Опубликуйте все фотографии

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
* Создайте [приложение](https://api.imgur.com/oauth2/addclient)
    - В поле `Authorization callback URL` напишите `http://localhost`
* Создайте конфигурационный файл и добавьте полученные выше `Client ID` и `Client secret`
```shell script
~ nano configuration.yml
```
```
imgur:
  client_id: ''
  client_secret: ''
```
* Запустите скрипт:
```shell script
~ python3 main.py
```

* Во время выполнения по [ссылке](https://api.imgur.com/oauth2/authorize) получите PIN и введите ниже: 
```
Input pin: 
```
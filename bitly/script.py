import json
import requests
import yaml


conf = yaml.safe_load(open('configuration.yml'))
token = conf['user']['token']


def get_user_info():
    url = f'https://api-ssl.bitly.com/v4/user'

    headers = {
        'Authorization': token
    }

    response = requests.get(url, headers=headers).json()
    return response


def expand_link(link):
    url = f'https://api-ssl.bitly.com/v4/expand'

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }

    payload = {
        'bitlink_id': link
    }

    payload = json.dumps(payload)
    response = requests.post(url, headers=headers, data=payload).json()
    return response


def shorten_link(link):
    url = f'https://api-ssl.bitly.com/v4/shorten'

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }

    payload = {
        'long_url': link
    }

    payload = json.dumps(payload)
    response = requests.post(url, headers=headers, data=payload)
    return response


def count_clicks(bitlink):
    url_template = f'https://api-ssl.bitly.com/v4/bitlinks/' \
                   f'{bitlink}/clicks/summary?units=-1'

    url = url_template.format(bitlink)

    headers = {
        'Authorization': token
    }

    response = requests.get(url, headers=headers)
    return response


def main(user_input):

    if user_input[0:5] == 'https':
        is_bitly = user_input.startswith("bit.ly", 8, 14)
        bitlink = user_input[8:]
    elif user_input[0:4] == 'http':
        is_bitly = user_input.startswith("bit.ly", 7, 13)
        bitlink = user_input[7:]
    else:
        is_bitly = user_input.startswith("bit.ly")
        bitlink = user_input

    if is_bitly:

        try:
            response = count_clicks(bitlink)
            response.raise_for_status()
            total_clicks = response.json()['total_clicks']
            result = f'По вашей ссылке прошли {total_clicks} раз(а)'
            print(result)
            return result

        except Exception as err:
            print(f'Ошибка при загрузке страницы: {err}')

        except requests.exceptions.ConnectionError:
            print('\nConnectionError occured')

        except requests.exceptions.HTTPError as err:
            print('\nHTTP Error occured')
            print('Response is: {content}'.format(
                content=err.response.content))
            print(err.response.status_code)

    elif not is_bitly:

        try:

            response = requests.get(user_input)
            response.raise_for_status()

        except Exception as err:
            print(f'Ошибка при загрузке страницы: {err}')

        except requests.exceptions.ConnectionError:
            print('\nConnectionError occured')

        except requests.exceptions.HTTPError as err:
            print('\nHTTP Error occured')
            print('Response is: {content}'.format(
                content=err.response.content))
            print(err.response.status_code)

        else:

            bitlink = shorten_link(user_input)

            if bitlink.ok is True and 'bit.ly' in bitlink.json()['id']:
                result = f"Короткая ссылка: {bitlink.json()['link']}"
                print(result)
                return result

            elif bitlink.json()['errors'][0]['error_code'] == 'invalid':
                result = f'Error: {bitlink.json()["message"]}'
                print(result)
                return result


if __name__ == "__main__":
    user_input_url = str(input('Введите ссылку: '))
    main(user_input_url)

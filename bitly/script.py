import requests
import yaml


def return_token():
    conf = yaml.safe_load(open('configuration.yml'))
    token = conf['user']['token']

    return token


def return_bitly(user_input):
    if user_input.startswith('https', 0, 5):
        is_bitly = user_input.startswith("bit.ly", 8, 14)
        bitlink = user_input[8:]
    elif user_input.startswith('http', 0, 4):
        is_bitly = user_input.startswith("bit.ly", 7, 13)
        bitlink = user_input[7:]
    else:
        is_bitly = user_input.startswith("bit.ly")
        bitlink = user_input

    return bitlink, is_bitly


def shorten_link(link, token):
    url = f'https://api-ssl.bitly.com/v4/shorten'

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }

    payload = {
        'long_url': link
    }

    try:

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        if response.ok and 'bit.ly' in response.json()['id']:
            result = f"Короткая ссылка: {response.json()['link']}"
            return result

        elif response.json()['errors'][0]['error_code'] == 'invalid':
            result = f'Error: {response.json()["message"]}'
            return result

    except requests.exceptions.ConnectionError:
        result = f'\nConnectionError occured'
        return result

    except requests.exceptions.HTTPError as err:
        result = '\nHTTP Error occured. ' \
                 '\nResponse is: {content}. ' \
                 '\nStatus code: {status_code}'\
            .format(content=err.response.content,
                    status_code=err.response.status_code)
        return result


def count_clicks(bitlink, token):
    url_template = f'https://api-ssl.bitly.com/v4/bitlinks/' \
                   f'{bitlink}/clicks/summary?units=-1'

    url = url_template.format(bitlink)

    headers = {
        'Authorization': token
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        total_clicks = response.json()['total_clicks']
        result = f'По вашей ссылке прошли {total_clicks} раз(а)'
        return result

    except requests.exceptions.ConnectionError:
        result = f'\nConnectionError occured'
        return result

    except requests.exceptions.HTTPError as err:

        result = '\nHTTP Error occured. ' \
                 '\nResponse is: {content}. ' \
                 '\nStatus code: {status_code}'\
            .format(content=err.response.content,
                    status_code=err.response.status_code)
        return result


def main():

    user_input = input('Введите ссылку: ')
    token = return_token()
    bitlink, is_bitly = return_bitly(user_input)

    if is_bitly:

        total_clicks = count_clicks(bitlink, token)
        print(total_clicks)

    elif not is_bitly:

        short_link = shorten_link(user_input, token)
        print(short_link)


if __name__ == "__main__":
    main()

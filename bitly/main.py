import argparse
import requests
import yaml


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('link', type=str,
                        help='Enter a link to shorten or count clicks')

    return parser


def get_token():

    with open('configuration.yml', 'r') as stream:
        conf = yaml.safe_load(stream)
        token = conf['user']['token']

    return token


def get_bitly(user_input):
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

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    response = response.json()

    return response['link']


def count_clicks(bitlink, token):
    url_template = f'https://api-ssl.bitly.com/v4/bitlinks/' \
                   f'{bitlink}/clicks/summary?units=-1'

    url = url_template.format(bitlink)

    headers = {
        'Authorization': token
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response = response.json()

    total_clicks = response['total_clicks']
    return total_clicks


def main():

    try:

        parser = create_parser()
        namespace = parser.parse_args()

        user_input = namespace.link

        token = get_token()
        bitlink, is_bitly = get_bitly(user_input)

        if is_bitly:
            total_clicks = count_clicks(bitlink, token)
            print(f'Followed your link {total_clicks} time(s)')

        elif not is_bitly:
            short_link = shorten_link(user_input, token)
            print(f'Your short link: {short_link}')

    except FileNotFoundError as err:
        print(err)

    except yaml.YAMLError as err:
        print(err)

    except requests.exceptions.ConnectionError:
        print(f'\nConnectionError occured')

    except requests.exceptions.HTTPError as err:
        response = '\nHTTP Error occured. ' \
                   '\nResponse is: {content}. ' \
                   '\nStatus code: {status_code}'\
            .format(content=err.response.content,
                    status_code=err.response.status_code)
        print(response)


if __name__ == "__main__":
    main()

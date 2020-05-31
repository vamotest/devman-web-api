import requests

from .script import get_token, get_bitly, shorten_link, count_clicks
import pytest


@pytest.mark.parametrize('user_input', [
	"http://google.com",
	"https://google.com"
])
def test_shorten_link_positive(user_input):
	token = get_token()
	short_link = shorten_link(user_input, token)
	print(f'Короткая ссылка: {short_link}')
	is_bitly = get_bitly(short_link)[1]

	assert is_bitly


@pytest.mark.parametrize('user_input', [
	"google"
])
def test_shorten_link_negative(user_input):
	token = get_token()

	try:
		short_link = shorten_link(user_input, token)
		is_bitly = get_bitly(short_link)[1]
		assert not is_bitly

	except requests.exceptions.HTTPError as err:
		print(f'HTTP Error occured: {err}')


@pytest.mark.parametrize('user_input', [
	"http://bit.ly/3d5pjun",
	"https://bit.ly/2y6XJ1f"
])
def test_count_clicks_positive(user_input):
	token = get_token()
	bitlink = get_bitly(user_input)[0]
	total_clicks = count_clicks(bitlink, token)
	print(f'По вашей ссылке прошли {total_clicks} раз(а)')

	assert isinstance(total_clicks, int)


@pytest.mark.parametrize('user_input', [
	"http://bit.ly/5dc76c61-4291-429b-9111-bcbe73621eef",
	"https://bit.ly/dc4ed5c0-05b9-4558-937e-2fba1c9119af"
])
def test_count_clicks_negative(user_input):
	token = get_token()
	bitlink = get_bitly(user_input)[0]

	try:
		total_clicks = count_clicks(bitlink, token)
		assert not isinstance(total_clicks, int)

	except requests.exceptions.HTTPError as err:
		print(f'HTTP Error occured: {err}')

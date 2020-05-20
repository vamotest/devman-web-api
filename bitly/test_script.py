from .script import return_token, return_bitly, shorten_link, count_clicks
import pytest


@pytest.mark.parametrize('user_input', [
	"http://google.com",
	"https://google.com"
])
def test_shorten_link_positive(user_input):

	token = return_token()
	short_link = shorten_link(user_input, token)
	print(short_link)

	assert short_link.startswith('Короткая ссылка')


@pytest.mark.parametrize('user_input', [
	"google"
])
def test_shorten_link_negative(user_input):

	token = return_token()
	short_link = shorten_link(user_input, token)
	print(short_link)

	assert short_link.startswith('\nHTTP Error occured')


@pytest.mark.parametrize('user_input', [
	"http://bit.ly/3d5pjun",
	"https://bit.ly/2y6XJ1f"
])
def test_count_clicks_positive(user_input):

	token = return_token()
	bitlink = return_bitly(user_input)[0]

	total_clicks = count_clicks(bitlink, token)
	print(total_clicks)

	assert total_clicks.startswith('По вашей ссылке прошли')


@pytest.mark.parametrize('user_input', [
	"http://bit.ly/5dc76c61-4291-429b-9111-bcbe73621eef",
	"https://bit.ly/dc4ed5c0-05b9-4558-937e-2fba1c9119af"
])
def test_count_clicks_negative(user_input):
	token = return_token()
	bitlink = return_bitly(user_input)[0]

	total_clicks = count_clicks(bitlink, token)
	print(total_clicks)

	assert total_clicks.startswith('\nHTTP Error occured')

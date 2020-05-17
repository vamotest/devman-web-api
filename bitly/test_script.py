from .script import main
import pytest


@pytest.mark.parametrize('user_input_url', [
	"http://google.com",
	"https://google.com",
	"http://bit.ly/3d5pjun",
	"https://bit.ly/2y6XJ1f",
])
def test_qwe(user_input_url):

	# if 'http' or 'https' not in user_input_url:
	# 	user_input = f'https://{user_input_url}'
	# 	result = main(user_input)
	# else:
	# 	result = main(user_input_url)

	result = main(user_input_url)

	if 'Короткая ссылка:' in result:
		assert True
	elif 'По вашей ссылке прошли' in result:
		assert True
	else:
		assert False

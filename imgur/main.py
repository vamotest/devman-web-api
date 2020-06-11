from pathlib import Path
import os
import shutil

from interruptingcow import timeout
from progress.bar import IncrementalBar
from imgurpython import ImgurClient
from PIL import Image
import requests
import yaml


def get_imgur_configuration():
	with open('configuration.yml', 'r') as stream:
		conf = yaml.safe_load(stream)

		imgur = conf['imgur']
		client_id = imgur['client_id']
		client_secret = imgur['client_secret']

	return client_id, client_secret


def authenticate_imgur_client(client_id, client_secret):
	client = ImgurClient(client_id, client_secret)
	authorization_url = client.get_auth_url('pin')

	return client, authorization_url


@timeout(60)
def authorize_imgur_client(client, pin):
	client.authorize(pin, 'pin')

	return client


def fetch_spacex_last_launch(host, filename):
	response = requests.get(f'{host}/v3/launches/latest')
	response.raise_for_status()
	response = response.json()

	flickr_images = response['links']['flickr_images']

	image_urls = []
	bar = IncrementalBar(f'Fetch {filename} url ', max=len(
		flickr_images))
	for image_url in enumerate(flickr_images):
		bar.next()
		image_urls.append(image_url[1])
	bar.finish()

	return image_urls


def fetch_hubble(host, filename):
	response = requests.get(f'{host}/api/v3/images/wallpaper')
	response.raise_for_status()
	response = response.json()

	id_images = []
	for number, image_url in enumerate(response):
		id_images.append(f'{response[number]["id"]}')

	image_urls = []
	bar = IncrementalBar(f'Fetch {filename} urls:', max=len(id_images))
	for id_image in enumerate(id_images):
		bar.next()

		response = requests.get(f'{host}/api/v3/image/{id_image[1]}/')
		response.raise_for_status()
		response = response.json()

		image_files = response['image_files']
		image_urls.append(f'http:{image_files[-1]["file_url"]}')

	bar.finish()

	return image_urls


def download_image(image_urls, filename, file_extensions):
	Path('images').mkdir(parents=True, exist_ok=True)

	size = None
	if len(image_urls) == len(file_extensions):
		size = len(image_urls)
	elif image_urls != file_extensions:
		raise AssertionError('image_urls != file_extensions')

	bar = IncrementalBar(f'Download {filename} images:', max=size)
	for number, (image_url, file_extension) in enumerate(
			zip(image_urls, file_extensions)):
		bar.next()
		response = requests.get(image_url)
		response.raise_for_status()

		with open(f'images/{filename}{number}.{file_extension}', 'wb') as file:
			file.write(response.content)

	bar.finish()


def find_out_file_extension(image_urls):
	file_extensions = []

	for number, image_url in enumerate(image_urls):
		file_extensions.append(image_url.split('.')[-1])

	return file_extensions


def change_image_proportion():
	images = os.listdir(path="images")
	bar = IncrementalBar(f'Change image proportion:', max=len(images))

	for image in images:
		bar.next()
		image_path = f'images/{image}'
		im = Image.open(image_path)
		os.remove(image_path)

		image_file, ext = os.path.splitext(image)

		if im.mode == 'RGBA':
			im = im.convert('RGB')

		im.thumbnail((1080, 1080))
		im.save(f'images/{image_file}.jpg', format='JPEG')
	bar.finish()

	return os.listdir(path="images")


def upload_images(client, images):
	bar = IncrementalBar(f'Upload images to imgur:', max=len(images))
	upload_links = []

	for image in images:
		bar.next()

		config = {
			'privacy': 'public',
			'name': f'{image}',
		}

		upload_link = client.upload_from_path(
			f'images/{image}', config=config, anon=False)['link']
		upload_links.append(upload_link)
	bar.finish()

	return upload_links


def main():
	try:

		filenames = ['spacex', 'hubble']
		urls = ['https://api.spacexdata.com', 'http://hubblesite.org']

		for filename, url in zip(filenames, urls):

			image_urls = None
			if filename == 'spacex':
				image_urls = fetch_spacex_last_launch(url, filename)
			elif filename == 'hubble':
				image_urls = fetch_hubble(url, filename)

			file_extension = find_out_file_extension(image_urls)
			download_image(image_urls, filename, file_extension)

		images = change_image_proportion()

		client_id, client_secret = get_imgur_configuration()
		client, authorization_url = \
			authenticate_imgur_client(client_id, client_secret)

		print(f'\nGo to the following URL: {authorization_url}')
		pin = input('Input pin: ')

		client = authorize_imgur_client(client, pin)
		upload_links = upload_images(client, images)

		for upload_image_link in upload_links:
			print(
				f'Image was posted! You can find it here: {upload_image_link}')

	except FileNotFoundError as err:
		print(err)

	except yaml.YAMLError as err:
		print(err)

	except requests.exceptions.ConnectionError:
		print(f'\nConnectionError occured')

	except requests.exceptions.HTTPError as err:
		response = '\nHTTP Error occured. ' \
		           '\nResponse is: {content}. ' \
		           '\nStatus code: {status_code}'.format(
			content=err.response.content, status_code=err.response.status_code)
		print(response)

	finally:
		shutil.rmtree('images')


if __name__ == "__main__":
	main()

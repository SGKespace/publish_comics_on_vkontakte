import requests
from pathlib import Path
import urllib
import os
from dotenv import load_dotenv
import random

def return_pars_name(url):
    spliten_url = urllib.parse.urlsplit(url)
    (full_path, full_name) = os.path.split(spliten_url.path)
    return os.path.splitext(full_name)


def download_file(url, path_to_save_files, params: str = ''):
    photo_response = requests.get(url, params=params)
    photo_response.raise_for_status()
    with path_to_save_files.open('wb') as file:
        file.write(photo_response.content)


def main():
    load_dotenv()
    vk_token = os.environ["VK_TOKEN"]
    group_id = 218953627

    comics_url, comics_title = get_comic()
    path_to_file = download_comics_image(comics_url)
    upload_url = get_url_upload(vk_token, group_id)
    upload_photo_on_wall(path_to_file, upload_url)


def upload_photo_on_wall(path_to_file, upload_url):
    with open(path_to_file, 'rb') as photo:
        files = {'Content-Type': 'multipart/form-data', 'photo': photo}
        response = requests.post(upload_url, files=files)

    upload_response = response.json()
    upload_server = upload_response['server']
    upload_photo = upload_response['photo']
    upload_hash = upload_response['hash']

    return upload_server, upload_photo, upload_hash


def get_url_upload(vk_token, group_id):
    url_method = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': vk_token,
        'group_id': group_id,
        'v': 5.131
               }

    response = requests.get(url_method, params=params)
    response.raise_for_status()
    response_message = response.json()
    upload_url = response_message['response']['upload_url']

    return upload_url



def get_groups(vk_token):
    url_method = 'https://api.vk.com/method/groups.get'
    params = {
        'access_token': vk_token,
        'v': 5.131,
        'extended': 1
    }

    response = requests.get(url_method, params=params)
    response.raise_for_status()
    groups = response.json()

    return groups


def get_comic():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    all_comics_count = response.json()['num']

    random.seed()
    random_comic_index = random.randint(0, all_comics_count)

    url = f'https://xkcd.com/{random_comic_index}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics_data = response.json()

    return comics_data['img'], comics_data['alt']


def download_comics_image(url):

    photo_response = requests.get(url)
    (file_name, file_extension) = return_pars_name(url)

    path_to_save_files = Path(f'images/{file_name}{file_extension}')
    path_to_save_files.parent.mkdir(parents=True, exist_ok=True)

    with path_to_save_files.open('wb') as file:
        file.write(photo_response.content)

    return path_to_save_files



    response = requests.get(url)
    response.raise_for_status()

    file_path = urllib.parse.unquote(urlparse(url).path)
    path, file_name = os.path.split(file_path)

    with open(file_name, 'wb') as file:
        file.write(response.content)

    return file_name



if __name__ == '__main__':
    main()
import requests
from pathlib import Path
import urllib
import os
from dotenv import load_dotenv


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
    print(get_url_upload(vk_token, group_id))


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
    url_vk = 'https://vk.com/public218953627'
    # url = 'https://xkcd.com/info.0.json'
    url = 'https://xkcd.com/353/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    request = response.json()
    img_url = request['img']
    text = request['alt']
    (file_name, file_extension) = return_pars_name(img_url)
    photo_response = requests.get(img_url)
    path_to_save_files = Path(f'images/{file_name}{file_extension}')
    path_to_save_files.parent.mkdir(parents=True, exist_ok=True)
    with path_to_save_files.open('wb') as file:
        file.write(photo_response.content)
    print(text)


if __name__ == '__main__':
    main()
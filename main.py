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
    vk_client_id = os.environ["VK_CLIENT_ID"]
    vk_token = os.environ["VK_TOKEN"]
    get_grouups(vk_token)
    

def get_grouups(vk_token):
    url_method = 'https://api.vk.com/method/groups.get'  #  список ваших групп.
    params = {
        'access_token': vk_token,
        'v': 5.131,
        'extended': 1
    }

    response = requests.get(url_method, params=params)
    response_message = response.json()
    print(response_message)


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
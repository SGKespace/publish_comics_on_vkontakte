from dotenv import load_dotenv
import os
import random
import shutil
from pathlib import Path
import requests
import urllib


def main():
    load_dotenv()
    vk_token = os.environ["VK_TOKEN"]
    vk_group_id = int(os.environ["VK_GROUP_ID"])

    try:
        comics_url, comics_title = get_comic()
        path_to_file = download_comics_image(comics_url)
        upload_url = get_upload_url(vk_token, vk_group_id)
        server_id, photo, photo_hash = upload_photo_on_wall(path_to_file, upload_url)
        owner_id, photo_id = save_photo_to_vk(server_id, photo, photo_hash, vk_token, vk_group_id)
        post_photo_on_wall_vk(vk_token, vk_group_id, comics_title, owner_id, photo_id)
    except requests.exceptions.HTTPError:
        print('Cформировался неверный запрос.')
    except VkErrors as error:
        print('Ошибка при обращении к API во Вконтакте:', error)
    finally:
        shutil.rmtree('images')


def return_pars_name_img(url):
    spliten_url = urllib.parse.urlsplit(url)
    (full_path, full_name) = os.path.split(spliten_url.path)
    return os.path.splitext(full_name)


def post_photo_on_wall_vk(vk_token, vk_group_id, comics_title, owner_id, photo_id):
    url_method = 'https://api.vk.com/method/wall.post/'
    params = {
        'access_token': vk_token,
        'owner_id': f'-{vk_group_id}',
        'from_group': -1,
        'message': comics_title,
        'attachments': {f'photo{owner_id}_{photo_id}'},
        'v': 5.131
               }

    response = requests.post(url_method,  params=params,)
    post_photo_response = response.json()

    return post_photo_response


def save_photo_to_vk(server_id, photo, photo_hash, vk_token, vk_group_id):
    url_method = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'server': server_id,
        'photo': photo,
        'hash': photo_hash,
        'access_token': vk_token,
        'group_id': vk_group_id,
         'v': 5.131
              }

    response = requests.post(url_method, params=params)
    save_photo_response = response.json()
    owner_id = save_photo_response['response'][0]['owner_id']
    photo_id = save_photo_response['response'][0]['id']

    return owner_id, photo_id


def upload_photo_on_wall(path_to_file, upload_url):
    with open(path_to_file, 'rb') as photo:
        files = {'Content-Type': 'multipart/form-data', 'photo': photo}
        response = requests.post(upload_url, files=files)

    upload_response = response.json()
    upload_server = upload_response['server']
    upload_photo = upload_response['photo']
    upload_hash = upload_response['hash']

    return upload_server, upload_photo, upload_hash


def get_upload_url(vk_token, vk_group_id):
    url_method = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': vk_token,
        'group_id': vk_group_id,
        'v': 5.131
               }

    response = requests.get(url_method, params=params)
    response.raise_for_status()
    response_message = response.json()
    upload_url = response_message['response']['upload_url']

    return upload_url


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

def create_path_to_save_files(file_name, file_extension):
    path_to_save_files = Path(f'images/{file_name}{file_extension}')
    path_to_save_files.parent.mkdir(parents=True, exist_ok=True)
    return path_to_save_files


def download_comics_image(url):
    photo_response = requests.get(url)
    file_name, file_extension = return_pars_name_img(url)
    path_to_save_files = create_path_to_save_files(file_name, file_extension)

    with path_to_save_files.open('wb') as file:
        file.write(photo_response.content)

    return path_to_save_files


if __name__ == '__main__':
    main()
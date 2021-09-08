from pprint import pprint
import requests
import os
import json
import time
import sys

class VK_Get_Photo:
    url = 'https://api.vk.com/method/'
    file_path = os.path.join(os.getcwd(), "photos.json")
    def __init__(self, token_vk):
        self.params = {
            'access_token': token_vk,
            'v': '5.60'
        }

    # получаем фотографии
    def get_photo(self, user_id=None, file_path=file_path):
        url_get_photo = self.url + 'photos.get'
        get_photo_params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': '1',
            'count': 30,
        }
        res = requests.get(url_get_photo, params={**self.params, **get_photo_params}).json()

        # количество фотографий для цикла
        number_of_items = int(res['response']['count'])

        # объявляем все нужные списки и словари
        photos_size_max = {}
        likes_list = []
        max_name_list = []
        file_name_list = []
        url_list = []
        all_data_list = []

        # запускаем цикл для каждой фотографии (item)
        for count in range(number_of_items):
            item = res['response']['items'][count]

            # список для сплита названий фоток и определения максимального размера
            photos_names = []

            # находим фотографию максимального размера, указанного в имени фото (можно использовать параметр photo_size, но я его поздно заметил в описании)
            for name in item:
                if 'photo' in name:
                    image_size = int(name.split('_',1)[1])
                    photos_names.append(image_size)
            photo_max_name = 'photo_' + str(max(photos_names))
            max_name_list.append(photo_max_name)
            url_list.append(res['response']['items'][count][photo_max_name])

            # достаем лайки и проверяем на повтор количества лайков
            likes = res['response']['items'][count]['likes']['count']
            likes_list.append(likes)
            if likes in likes_list[0:count]:
                date = res['response']['items'][count]['date']
                likes = str(likes) + '_' + str(date)
                photos_size_max[likes] = photo_max_name
                file_name_list.append(likes)

            else:
                likes = str(likes)
                photos_size_max[likes] = photo_max_name
                file_name_list.append(likes)

        # Запускаем первую часть прогресс бара
        print('Выполнение загрузки:\n')
        for i in file_name_list:
            print(f'Фото №{i} загружено')

        # записываем все данные в список словарей
        name_data_dict = dict(zip(file_name_list, max_name_list))
        url_data_dict = dict(zip(file_name_list, url_list))

        for k, v in name_data_dict.items():
            all_data_dict = {}
            all_data_dict['file name'] = k + '.jpg'
            all_data_dict['photo name'] = v
            all_data_dict['url'] = url_data_dict.get(k)
            all_data_list.append(all_data_dict)

        # делаем json
        json_data = json.dumps(all_data_list, indent=4)
        with open(file_path, "w") as file:
            file.write(json_data)

        # Запускаем вторую часть прогресс бара
        print('json создан')

# Загрузка фотографий на Я.Диск
class YaUploader:
    def __init__(self, token):
        self.token = token

    # Делаем папку на Я.Диске
    def make_dir(self, token):
        headers = {
            'accept': 'application/json',
            'authorization': f'OAuth {token}'
        }

        params = {
            'path': 'New folder',
        }

        url = "https://cloud-api.yandex.net/v1/disk/resources/"
        r = requests.put(url=url, params=params, headers=headers)
        res = r.json()
        json.dumps(res, sort_keys=True, indent=4, ensure_ascii=False)

    # Загружаем фотки из photos.json на Я.Диск
    def upload(self, token):
        headers = {
            'accept': 'application/json',
            'authorization': f'OAuth {token}'
        }

        with open('photos.json', 'r') as file:
            data = json.load(file)
            for item in range(len(data)):
                a = data[item]["file name"]
                url = data[item]["url"]

                params = {
                    'path': f'New folder/{a}',
                    'url': f'{url}'
                }

                url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
                r = requests.post(url=url, params=params, headers=headers)
                res = r.json()
                json.dumps(res, sort_keys=True, indent=4, ensure_ascii=False)
                print(f'Фото №{a} передано')


# запускаем Коровина
token_vk = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
token_ya = input('Введите токен для Я.Диска: ')

korovin = VK_Get_Photo(token_vk)

user_id = input('Введите id пользователя в VK: ')

# Тестовый id - '552934290'

korovin.get_photo(user_id)

uploader = YaUploader(token_ya)
make_dir = uploader.make_dir(token_ya)
result = uploader.upload(token_ya)




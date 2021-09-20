from pprint import pprint
import requests
import os
import json


class VK_Get_Photo:
    url = 'https://api.vk.com/method/'
    def __init__(self):
        self.params = {
            'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
            'v': '5.131'
        }

    def get_photo(self):
        user_input = input("Введите ID или screen_name: ")
        url_get_profile = self.url + 'users.get'
        get_user_params = {
            'user_ids': user_input
        }

        user_profile = requests.get(url_get_profile, params={**self.params, **get_user_params})
        user_id = user_profile.json()['response'][0]['id']

        url_get_photo = self.url + 'photos.get'
        input_count = int(input("Введите количество фотографий: "))
        get_photo_params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': '1',
            'count': input_count,
        }
        res = requests.get(url_get_photo, params={**self.params, **get_photo_params}).json()

        photo_list = []
        name_list = []
        if input_count > res['response']['count']:
            input_count = res['response']['count']

        for i in range(input_count):
            photo_dict = {}
            name = res['response']['items'][i]['likes']['count']
            date = res['response']['items'][i]['date']

            if name in name_list:
                name = f'{name}_{date}'
            else:
                name_list.append(name)

            for p in res['response']['items'][i]['sizes']:
                size = p['height']
                max_size = 0
                if size > max_size:
                    max_size = size
                    photo_url = p['url']
                    photo_size = p['type']

            photo_dict["file_name"] = f'{name}.jpg'
            photo_dict["size"] = photo_size
            photo_dict["url"] = photo_url
            photo_list.append(photo_dict)

        print('\nВыполнение загрузки:')
        x = 0
        for i in photo_list:
            x += 1
            print(f'Фото загружено №{x}')
        print('\n')

    # # Загрузка фотографий на Я.Диск
    # def upload(self):
        token = input('Ввести токен Я.Диска: ')
        headers_make_path = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {token}'}

        url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        path = input('Введите название папки: ')
        requests.put(f'{url}?path={path}', headers=headers_make_path)

        headers_post_photo = {
            'accept': 'application/json',
            'authorization': f'OAuth {token}'
        }


        # photo_list =

        for item in photo_list:
            file_name = item['file_name']
            photo_url = item['url']

            upload_params = {
                'path': f'{path}/{file_name}',
                'url': f'{photo_url}'
            }

            url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
            r = requests.post(url=url, params=upload_params, headers=headers_post_photo)

        for i in photo_list:
            del i["url"]
        file_path = os.path.join(os.getcwd(), "photos.json")
        json_data = json.dumps(photo_list, indent=4)
        with open(file_path, "w") as file:
            file.write(json_data)
        print('\n')
        print('JSON создан')
        print('Все готово')


vk_user = VK_Get_Photo()
result = vk_user.get_photo()




# main
Публикуем комиксы во Вконтакте.
Скрипт берет случайный комикс с [сайта Рэндела Манро](https://xkcd.com/) и публикует в VK на стену сообщества. Необходимо создать руппу в VK где будут публиковаться комиксы и [получить Токен Вконтакте](https://vk.com/dev/implicit_flow_user). Общая документация по [API](https://vk.com/dev/manuals). Узнать ID группы ВКонтакте можно [следуя описанию](https://regvk.com/id/) или воспользовавшись функцией get_groups(vk_token) из main.py.

# Переменные окружения
Пример файла .env
``` 
VK_TOKEN='vk1.a.CRv-aE6vkhgklhkho8yo8y71y5UGBpsoXZgTk-HaezHvmhfcjhdhdFJYFI9YGKBGLHJg,jb,73YTIAcUMAnI3Mb1mD-ikNtZSrvUKsZXuUh6YSPM4Nq1xCyDIwJhDc-EYmhgvkhhjjkkkhgkfjfgkhYz_w'

```

## Требования к окружению

Python 3.xx и выше (должен быть уже установлен)

requests 2.24.0

python-dotenv==0.21.0


Можно установить командой  
``` 
PIP install -r requirements.txt
```
# Запустить скрипт командой
``` 
python main.py
``` 
# Пример правльной отработки скрипта:

<img width="558" alt="image" src="https://user-images.githubusercontent.com/55636018/220386270-6420c564-85e7-44e5-81ea-41039863a526.png">



## Отказ от ответственности

Автор программы не несет никакой ответственности за то, как вы используете этот код или как вы используете сгенерированные с его помощью данные. Эта программа была написана для обучения автора и других целей не несет. Не используйте данные, сгенерированные с помощью этого кода в незаконных целях.

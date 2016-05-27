# Установка и настройка

* Установить **Python 3.5.1**<br>
(для debian: `apt-get install python3-pip`)

* Установить фреймворк **Django** (cmd из-под админа):<br>
`pip install django`<br>
(для debian: `pip3 ...`)

* Перейти в папку проекта и инициализировать приложение:<br>
`django-admin startproject mysite .`

* Поправить время и папку статичных файлов в mysite/settings.py:<br>
```ini
    TIME_ZONE = 'Europe/Moscow'
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

* Создать БД по-умолчанию:<br>
`python manage.py migrate`<br>
(в debian здесь и далее команда: `python3 ...`)

* Проверить работу запуском:<br>
`python manage.py runserver`<br>
и зайти на: **http://localhost:8000/admin/login/**

* Создаем новое приложение:<br>
`python manage.py startapp dashboard`<br>
и добавить в *mysite/settings.py* в список *INSTALLED_APPS*:<br>
```
    dashboard
```

* После создания модели определяем миграцию:<br>
`python manage.py makemigrations dashboard`<br>
и накатываем её:<br>
`python manage.py migrate dashboard`

* Добавляем работу с таблицей в админку, дописывая в файл *dashboard/admin.py*:<br>
```python
    from .models import КлассМодели
    admin.site.register(КлассМодели)
```

* Создаем юзера:<br>
`python manage.py createsuperuser`<br>
(в админке, если надо залогиниваться под определенным пользователем, то ставим ему "*статус персонала*" в "*Пользователи и группы*" > "*Пользователи*")

# Запуск на продакшене

```
screen

python3 manage.py runserver romanov-vrn.ru:8000
```

`Ctrl+A D` - выйти из консоли в систему

```
screen -r - вернуться в консоль
```

`Ctrl+A K` - убить консоль

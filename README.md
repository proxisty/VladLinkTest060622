VladLink

# Задание
[Тестовое задание.docx](https://github.com/proxisty/VladLinkTest060622/files/8845633/default.docx)

Меню выполненно на django версии 4.0.5, python 3.9. 

При открытии пути http://127.0.0.1:8000/menu/ :
1) Загрузится в БД PostgreSQL json, расположенный по пути BASE_DIR/categories_old.json.
![image](https://user-images.githubusercontent.com/42601425/172199309-0757a5c5-e99d-4da4-916d-98d837aa2595.png)
2) Также отобразится на вкладке http://127.0.0.1:8000/menu/ . Для построения меню используется алгоритм Nested Set: 
![image](https://user-images.githubusercontent.com/42601425/172196242-f21feb38-b5ca-4f65-b3ef-726ef7dfd5fd.png)
4) CRUD меню возможен через админ-панель: http://127.0.0.1:8000/admin/menu/categories/
5) Также автоматически выполнится экспорт в type_a.txt и type_b.txt соответственно заданию.

# Установка
В виртуальном окружении (virtualenv) выполнить данную команду:
-- pip install -r requirements.txt
Создать базу данный, пример на psql:

create database vladlink;
create user vladlink_user WITH PASSWORD 'vladlink';
ALTER ROLE vladlink_user SET client_encoding TO 'utf8';
ALTER ROLE vladlink_user SET default_transaction_isolation TO 'read committed'; 
ALTER ROLE vladlink_user SET timezone TO 'Asia/Vladivostok'; 
GRANT ALL PRIVILEGES ON DATABASE vladlink TO vladlink_user;

Выполнить миграции
python manage.py makemigrations
python manage.py migrate

Создаем супер пользователя: с паролем и логинов uznavaika
python manage.py createsuperuser

Далее запустить сервер командой:
python manage.py runserver
Зайти на http://127.0.0.1:8000/menu/ для выполнения действий, описанных выше.

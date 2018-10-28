Для создания базы данных надо запустить python url_base.py

Перед запуском задайте логин и пароль к SMTP-серверу в переменных:
email_account_login = "insert_emaillogin_there"
email_account_password = "insert_emailpassword_there"

Для запуска сервера используем FLASK:
set FLASK_APP=service.py
python -m flask run

после чего вводим POST и GET запросы в командную строку
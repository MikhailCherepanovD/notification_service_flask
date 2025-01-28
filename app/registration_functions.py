from flask import Request
import logging
GLOBAL_COUNTER=0
def get_status_and_user_info_by_login_request(request: Request)->tuple:
    global GLOBAL_COUNTER
    # Используется в login
    login = request.form['login']
    password = request.form['password']
    logging.info(f"Вход пользователя: {login}, Пароль: {password}")
    mp =dict() #эти данные возмем из базы данных
    mp["login"]=GLOBAL_COUNTER
    mp["username"]="username"
    mp["telegram"]="telegram"
    mp["email"]="email"
    GLOBAL_COUNTER=GLOBAL_COUNTER+1
    return 1,mp

def get_status_by_register_request(request: Request)->int: #0 - регистрация успешна, 1 - пароли не совпадают, 2 - внешняя ошибка сервера
    username = request.form['username']
    email = request.form['email']
    telegram = request.form['telegram']
    login = request.form['login']
    password = request.form['password']
    repeat_password = request.form['repeat_password']
    if repeat_password != password:
        logging.info(f"Требуется повтор регистрации пользователя {username}. Пароли не совпадают.")
        return 1
    else:
        # логика запроса на сервер
        # записи в бд
        return 0
    return 0

def delete_user_by_request(request: Request)->bool:

    return 1;

def update_user_by_request(request: Request)->bool:
    return 1;
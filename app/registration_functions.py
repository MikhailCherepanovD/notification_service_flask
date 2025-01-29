import logging
import os
from operator import truediv

from flask import Request
import requests

GLOBAL_COUNTER: int = 0
def get_name_frequency_by_value(str_value: str) -> str:
    name_matching = {
        '1': 'Каждый час',
        '6': 'Каждые 6 часов',
        '12': 'Каждые 12 часов',
        '24': 'Каждые 24 часа',
        '48': 'Каждые 2 дня',
        '168': 'Раз в неделю',
    }
    if str_value in name_matching:
        return name_matching[str_value]
    else:
        return "".join(["Каждые ", str_value, " часов"])

def get_direct_by_name(str_value:str) -> str:
    if str_value=="Только без пересадок":
        return "true"
    return "false"

def get_status_and_info_by_login_request(request: Request) -> tuple:
    """0 - успешный вход, 1 - пользователь не найден, 2 - внешняя ошибка сервера"""
    login = request.form["login"]
    password = request.form["password"]
    data = {
        'login': login,
        'password': password
    }
    response_user = requests.post( os.getenv("LOGIN_URL"), json=data)
    if response_user.status_code == requests.codes.unauthorized:
        logging.info(f"User {login}: wrong login or password")
        return 1,None
    if response_user.status_code == requests.codes.ok:
        mp = dict()
        mp['email'] = response_user.json()['email']
        mp['id'] = response_user.json()['id']
        mp['login'] = response_user.json()['login']
        mp['telegram'] = response_user.json()['telegram']
        mp['user_name'] = response_user.json()['user_name']
        response_routes = requests.get("".join([os.getenv("USERS_URL"),'/', str(mp['id']),'/', "routes"]))
        print(response_routes.status_code)
        if response_routes.status_code == requests.codes.ok:
            mp['routes'] = response_routes.json()
        #print(mp)
        logging.info(f"User {login}: successful login")
        return 0,mp
    logging.info(f"External server error")
    return 2, None


def user_create_or_update(request: Request,user_id=None) -> int:
    """0 - регистрация успешна, 1 - пароли не совпадают, 2 - пользователь с таким логином уже существует, 3 - внешняя ошибка сервера"""
    user_name = request.form["username"]
    email = request.form["email"]
    telegram = request.form["telegram"]
    login = request.form["login"]
    password = request.form["password"]
    repeat_password = request.form["repeat_password"]
    if repeat_password != password:
        logging.info(f"User {login}: passwords don't match.")
        return 1
    data = {
        'login': login,
        'user_name': user_name,
        'password': password,
        'email':email,
        'telegram': telegram
    }
    if user_id is None:
        url = os.getenv("REGISTER_URL")
        response = requests.post(url, json=data)
    else:
        url = os.getenv("USERS_URL")+"/"+user_id
        response = requests.put(url, json=data)

    if response.status_code == 201:
        logging.info(f"User {login}: success creating.")
        return 0
    if response.status_code == 200:
        logging.info(f"User {login}: success updating.")
        return 0
    if response.status_code == 409:
        logging.info(f"User {login}: user conflict.")
        return 2
    logging.info(f"External server error")
    return 3

from flask import render_template, request, session
from app import app
from app.forms import LoginForm  # Импортируем форму
from app.registration_functions import *

import logging



@app.route('/')
def index():
    return render_template('index.html')

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # метод POST будет вызван при нажатии на кнопку
        login_status,user_info = get_status_and_user_info_by_login_request(request)
        if(login_status):
            session["login"] =user_info["login"]
            session["username"] = user_info["username"]
            session["telegram"] = user_info["telegram"]
            session["email"] = user_info["email"]
            return render_template('personal_account.html', message=str(user_info["login"]))      # тут будет имя вместо логина
        else:
            error_message = "Пароль или имя пользователя указаны неверно."
            return render_template('login.html', error_message = error_message)
    if request.method == 'GET':
        return render_template('login.html')


# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        register_status = get_status_by_register_request(request)
        if register_status==0:
            return render_template('login.html')
        elif register_status==1:
            error_message = "Пароли не совпадают. Попробуйте снова."
            return render_template('register.html', error_message = error_message)
        elif register_status==2:
            error_message = "Произошла внутренняя ошибка сервера. Попробуйте позже."
            return render_template('register.html', error_message=error_message)
    if request.method == 'GET':
        return render_template('register.html')


@app.route('/user_info', methods=['GET', 'POST', 'DELETE'])
def user_info():
    logging.info("зашли в user_info")
    user_info_strs = [session["username"], session["email"], session["telegram"], session["login"]]
    if(request.method == 'GET'):
        logging.info("Вызван метод GET")
        return render_template('user_info.html',user_info_strs = user_info_strs)

    if (request.method == 'POST' and request.form.get('action') == "update"):
        logging.info("Вызван метод POST - обновлении информации о пользователе")
        flag_update = update_user_by_request(request)
        if(flag_update):
            return render_template('personal_account.html', message=str(session["login"]))
        else:
            error_message = "Информация не была обновлена. Внутренняя ошибка сервера."
            return render_template('welcome.html', message=str(session["login"]),error_message=error_message)
    if (request.method == 'POST' and request.form.get('action') == "delete"):
        logging.info("Вызван метод POST - удаления пользователя")
        flag_delete = delete_user_by_request(request)
        if (flag_delete):
            return render_template('index.html')
        else:
            error_message = "Информация не была удалена. Внутренняя ошибка сервера."
            return render_template('welcome.html', message=str(session["login"]), error_message=error_message)

@app.route('/welcome', methods=['GET', 'POST', 'DELETE'])
def welcome():
    user_name = session["login"]
    return render_template('welcome.html',message = user_name)


@app.route('/personal_account', methods=['GET'])
def personal_account():
    return render_template('personal_account.html')



@app.route('/ticket_data/cheapest', methods=['GET'])
def cheapest():
    return render_template('ticket_data/cheapest.html')

@app.route('/ticket_data/current', methods=['GET'])
def current():
    return render_template('ticket_data/current.html')

@app.route('/ticket_data/statistic', methods=['GET'])
def statistic():
    return render_template('ticket_data/statistic.html')
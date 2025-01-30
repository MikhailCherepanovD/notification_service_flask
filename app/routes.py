from flask import render_template, request, session, Response, redirect, url_for
from app import app
from app.registration_functions import *
import json
import logging

app.jinja_env.filters["fromjson"] = lambda x: eval(x)  # Быстрый, но небезопасный способ


@app.route("/")
def index():
    return render_template("index.html")


# Страница входа
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":  # метод POST будет вызван при нажатии на кнопку
        login_status, user_info = get_status_and_info_by_login_request(request)
        if login_status == 0:
            session["id"] = user_info["id"]
            session["login"] = user_info["login"]
            session["user_name"] = user_info["user_name"]
            session["telegram"] = user_info["telegram"]
            session["email"] = user_info["email"]
            if "routes" in user_info and user_info["routes"]:
                session["routes"] = [
                    {
                        "start_city": route["start_city"],
                        "finish_city": route["finish_city"],
                        "id": route["route_monitoring_id"],
                        "start_time": route["start_time_monitoring"][:10],
                        "finish_time": route["finish_time_monitoring"][:10],
                        "frequency_monitoring": get_name_frequency_by_value(
                            str(route["frequency_monitoring"])
                        ),
                        "transfers_are_allowed": (
                            ""
                            if route["transfers_are_allowed"] == True
                            else "Только без пересадок"
                        ),
                    }
                    for route in user_info["routes"]
                ]
            else:
                session["routes"] = []
            print(session["routes"])
            return redirect(url_for("personal_account"))
        elif login_status == 1:
            error_message = "Пользователь не найден. Пароль или логин указаны неверно."
            return render_template("login.html", error_message=error_message)
        elif login_status == 2:
            error_message = "Произошла внутренняя ошибка сервера. Попробуйте позже."
            return render_template("login.html", error_message=error_message)
    if request.method == "GET":
        return render_template("login.html")


@app.route("/register", methods=["GET"])
def get_register():
    session.clear()
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def post_register():
    session.clear()
    register_status = user_create_or_update(request)
    if register_status == 0:
        return render_template("login.html")
    elif register_status == 1:
        error_message = "Пароли не совпадают. Попробуйте снова."
        return render_template("register.html", error_message=error_message)
    elif register_status == 2:
        error_message = "Пользователь с таким логином уже существует."
        return render_template("register.html", error_message=error_message)
    elif register_status == 3:
        error_message = "Произошла внутренняя ошибка сервера. Попробуйте позже."
        return render_template("register.html", error_message=error_message)


@app.route("/user_info", methods=["GET"])
def get_user_info():
    if "id" not in session:
        return Response(status=403)
    user_info_strs = [
        session["user_name"],
        session["email"],
        session["telegram"],
        session["login"],
    ]
    if request.method == "GET":
        logging.info("Вызван метод GET")
        return render_template("user_info.html", user_info_strs=user_info_strs)


@app.route("/user_info", methods=["POST"])
def post_user_info():
    if "id" not in session:
        return Response(status=403)
    if request.form.get("action") == "update":
        update_status = user_create_or_update(request, str(session["id"]))
        if update_status == 0:
            session["login"] = request.form["login"]
            session["user_name"] = request.form["username"]
            session["telegram"] = request.form["telegram"]
            session["email"] = request.form["email"]
            return redirect(url_for("personal_account"))
        elif update_status == 1:
            error_message = "Пароли не совпадают. Попробуйте снова."
            return render_template("user_info.html", error_message=error_message)
        elif update_status == 2:
            error_message = "Пользователь с таким логином уже существует."
            return render_template("user_info.html", error_message=error_message)
        elif update_status == 3:
            error_message = "Произошла внутренняя ошибка сервера. Попробуйте позже."
            return render_template("user_info.html", error_message=error_message)
    if request.form.get("action") == "delete":
        url = os.getenv("USERS_URL") + "/" + str(session["id"])
        response = requests.delete(url)
        if response.status_code == 200:
            logging.info(f"User {session["login"]}: deleted.")
            session.clear()
            return redirect(url_for("index"))
        else:
            logging.info(f"User {session["login"]}: error deleting.")
            error_message = "Произошла внутренняя ошибка сервера. Попробуйте позже."
            return render_template("user_info.html", error_message=error_message)


@app.route("/personal_account", methods=["GET"])
def personal_account():
    if "id" not in session:
        return Response(status=403)
    return render_template("personal_account.html", routes=session["routes"])


@app.route("/routes", methods=["DELETE"])
def delete_route():
    if "id" not in session:
        return Response(status=403)
    data_journey = request.get_json()
    routes_url = (
        os.getenv("USERS_URL")
        + "/"
        + str(session["id"])
        + "/routes/"
        + str(data_journey["id"])
    )
    response = requests.delete(routes_url)
    if response.status_code == 200:
        logging.info(f"Route {str(data_journey["id"])}: deleted.")
        session["routes"] = [
            route
            for route in session["routes"]
            if str(route["id"]) != str(data_journey["id"])
        ]
    else:
        logging.info(f"Route {str(data_journey["id"])}: error deleting.")
    return Response(status=response.status_code)


@app.route("/routes", methods=["POST"])
def post_route():
    if "id" not in session:
        return Response(status=403)
    data_journey = request.get_json()
    print(data_journey)
    routes_url = os.getenv("USERS_URL") + "/" + str(session["id"]) + "/routes"
    body_request = {
        "origin": data_journey["from"],
        "destination": data_journey["to"],
        "type_of_journey": "avia",
        "frequency_of_monitoring": get_value_frequency_by_name(
            data_journey["frequency"]
        ),  # поправить
        "type_frequency_of_monitoring": "minutes",  # поправить
        "begin_date_monitoring": data_journey["dateBegin"],
        "end_date_monitoring": data_journey["dateEnd"],
        "direct": get_direct_by_name(data_journey["directOnly"]),
    }
    response = requests.post(routes_url, json=body_request)
    if response.status_code == 201:
        returned_route_id = response.headers.get("Location").split("/")[-1]
        logging.info(f"Route {str(returned_route_id)}: successful created.")
        new_route = {
            "start_city": data_journey["from"],
            "finish_city": data_journey["to"],
            "id": returned_route_id,  # уникальный ID для нового маршрута
            "start_time": data_journey["dateBegin"],
            "finish_time": data_journey["dateEnd"],
            "frequency_monitoring": data_journey["frequency"],  # исправить
            "transfers_are_allowed": (
                ""
                if get_direct_by_name(data_journey["directOnly"]) == True
                else "Только без пересадок"
            ),
        }
        session["routes"].append(new_route)
        return Response(
            json.dumps({"id": returned_route_id}),
            status=201,
            content_type="application/json",
        )
    logging.info(f"Route №NnN: error creating.")
    return Response(status=response.status_code)


@app.route("/ticket_data/cheapest", methods=["GET"])
def cheapest():
    if "id" not in session:
        return Response(status=403)
    route_id = request.args.get("route_id")
    url = (
        os.getenv("USERS_URL")
        + "/"
        + str(session["id"])
        + "/routes/"
        + route_id
        + "/cheapest"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return render_template("ticket_data/cheapest.html", json_data=data)
    return render_template("ticket_data/cheapest.html")


@app.route("/ticket_data/current", methods=["GET"])
def current():
    if "id" not in session:
        return Response(status=403)
    route_id = request.args.get("route_id")
    url = (
        os.getenv("USERS_URL")
        + "/"
        + str(session["id"])
        + "/routes/"
        + route_id
        + "/current"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return render_template("ticket_data/current.html", json_data=data)
    return render_template("ticket_data/current.html")


@app.route("/ticket_data/statistic", methods=["GET"])
def statistic():
    if "id" not in session:
        return Response(status=403)
    route_id = request.args.get("route_id")
    url = (
        os.getenv("USERS_URL")
        + "/"
        + str(session["id"])
        + "/routes/"
        + route_id
        + "/statistic"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return render_template("ticket_data/statistic.html", json_data=data)
    return render_template("ticket_data/statistic.html")

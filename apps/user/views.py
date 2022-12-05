from flask import Blueprint, jsonify, render_template, redirect, url_for, request, flash, g, session, Response, flash
from apps.user.models import my_db




user_app = Blueprint("user_app", import_name=__name__, url_prefix="/user")


@user_app.route("/login", methods=['GET', "POST"], endpoint="user_login")
def user_login():
    if request.method == "GET":
        return render_template('login/login.html')
    if request.method == "POST":
        try:
            user_name = request.form.get("user_name")
            password = request.form.get("password")
            login_status = request.form.get("login_status")
            # print(login_status)
            one_user = my_db.query_one(f"select * from user where username='{user_name}' and password='{password}'")
            if one_user:
                session['user_name'] = user_name
                if login_status:
                    session.permanent = True
                return redirect(url_for("log_app.shengsheng_index"))
        except Exception as e:
            print(e)
        flash(message="账号或密码错误,请重新输入", category="warning")
        return render_template('login/login.html')


@user_app.get("/logout", endpoint="user_logout")
def user_logout():
    try:
        if "user_name" in session:
            session.clear()
        return redirect(url_for("user_app.user_login"))
    except Exception as e:
        return jsonify({"status": 10404, "msg": "异常"})


@user_app.route("/login/test", methods=['GET', "POST"], endpoint="user_login111")
def user_login111():
    if request.method == "GET":
        return jsonify({"google": "string"})

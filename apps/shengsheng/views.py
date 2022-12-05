import datetime

from flask import Blueprint, jsonify, render_template, redirect, url_for, request, flash, g, session, Response

from apps.shengsheng.models import ShengShengLog, db
from sqlalchemy import func, desc, asc

from apps.user.models import my_db
from apps.utils.util import Aescrypt

# from sqlalchemy.sql import or_
from apps.models.redis import r
log_app = Blueprint(name="log_app", import_name=__name__, url_prefix="/log")

ignore_path = ["/log/upload/log/record"]


@log_app.before_request
def before_app_request():
    if session.get("user_name"):
        g.user_name = session.get("user_name")
        pass
    elif request.path in ignore_path:
        pass
    else:
        return redirect(url_for("user_app.user_login"))


@log_app.get("/ss/index", endpoint="shengsheng_index")
def shengsheng_index():
    if request.method == "GET":
        return render_template("shengsheng/index/index.html")


@log_app.post("/upload/log/record", endpoint="upload_log_record")
def upload_log_record():
    if request.method == "POST":
        try:
            aes = Aescrypt()
            json_data = request.get_json()

            token = request.headers.get("token").strip()
            one_token_info = my_db.query_one(
                f"select * from token_info where token='{token}' and update_time>'{datetime.datetime.now() - datetime.timedelta(hours=24)}' limit 1")
            if not one_token_info:
                return jsonify({"status": 10404, "msg": "token不存在或已过期"})
            code = one_token_info.get("code")

            username = my_db.query_one(f"select username from verfydevice where verfydevice.function='{code}' limit 1")
            if not username:
                return jsonify({"status": 10404, "msg": "此授权码不存在"})
            log_info = aes.decrypt_aes(json_data.get("log"))
            db.session.add(
                ShengShengLog(code=code, log_info=log_info, user_name=username.get("username"),
                              insert_time=datetime.datetime.now()))
            db.session.commit()
            return jsonify({"status": 10000, "msg": "成功"})
        except Exception as e:
            print(e)
            return jsonify({"status": 10404, "msg": "异常"})
        finally:
            db.session.close()


@log_app.route("/query/log/record/by/code", methods=['GET', 'POST'], endpoint="query_log_record_by_code")
def query_log_record_by_code():
    # if request.method == "GET":
    #     try:
    #         return render_template('shengsheng/codes/index.html')
    #     except Exception as e:
    #         print(e)
    #         return jsonify({"status": 10404, "msg": "异常"})
    if request.method == "POST":
        try:
            code = request.form.get("code", "").strip()
            user_name = session.get("user_name")

            all_log_datas = db.session.query(ShengShengLog).filter(
                ShengShengLog.code == code, ShengShengLog.user_name == user_name).order_by(
                desc(ShengShengLog.insert_time)).all()

            return render_template('shengsheng/codes/index.html', all_log_datas=all_log_datas, code=code)
        except Exception as e:
            print(e)
            return jsonify({"status": 10404, "msg": "异常"})
        finally:
            db.session.close()


@log_app.get("/clear/log/by/code", endpoint="clear_log_record_by_code")
def clear_log_record_by_code():
    if request.method == "GET":
        try:
            code = request.args.get("code").strip()

            user_name = session.get("user_name")

            if code:
                db.session.query(ShengShengLog).filter(ShengShengLog.code == code,
                                                       ShengShengLog.user_name == user_name).delete()
                db.session.commit()

            return render_template('shengsheng/codes/index.html', all_log_datas=[], code="")
        except Exception as e:
            print(e)
            return jsonify({"status": 10404, "msg": "异常"})
        finally:
            db.session.close()


@log_app.get("/delete/log/record", endpoint="delete_log_record")
def delete_log_record():
    if request.method == "GET":
        try:
            data_id = request.args.get("id")
            data_code = request.args.get("code").strip()
            user_name = session.get("user_name")

            db.session.query(ShengShengLog).filter_by(id=data_id).delete()
            db.session.commit()
            all_log_datas = db.session.query(ShengShengLog).filter(
                ShengShengLog.code == data_code, ShengShengLog.user_name == user_name).order_by(
                desc(ShengShengLog.insert_time)).all()

            return render_template('shengsheng/codes/index.html', all_log_datas=all_log_datas, code=data_code)
        except Exception as e:
            print(e)
            return jsonify({"status": 10404, "msg": "异常"})
        finally:
            db.session.close()


# 日志统计图

@log_app.get("/query/log/record/chart", endpoint="query_log_record_chart")
def query_log_record_chart():
    if request.method == "GET":
        try:
            user_name = session.get("user_name")
            now_time = datetime.datetime.now()
            time_list = []
            for i in range(14, -1, -1):
                time_list.append((now_time - datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
            all_data = db.session.query(
                func.substr(ShengShengLog.insert_time, 1, 10),
                func.count("*")).filter(
                ShengShengLog.insert_time >= datetime.date.today() - datetime.timedelta(days=14),
                ShengShengLog.user_name == user_name
            ).group_by(func.substr(ShengShengLog.insert_time, 1, 10)).all()
            # print(time_list)
            # print(all_data)
            log_record_data = []
            for i in time_list:
                for j in all_data:
                    if j[0] == i:
                        log_record_data.append(j[1])
                        break
                else:
                    log_record_data.append(0)

            # print(log_record_data)
            log_record_time = list(map(lambda x: x[-5:], time_list))
            log_record_data = log_record_data

            return render_template('shengsheng/chart/log_record_chart.html', log_record_data=log_record_data,
                                   log_record_time=log_record_time)
        except Exception as e:
            print(e)
            return jsonify({"status": 10404, "msg": "异常"})
        finally:
            db.session.close()



@log_app.get("/query/version/count/chart", endpoint="query_version_count_chart")
def query_version_count_chart():
    if request.method == "GET":
        username = g.get("user_name")

        data_list = []
        sums = 0
        for version in r.keys(f"{username}_version_function_*"):
            sums += r.scard(version)
            data_list.append(
                {"name": version.lstrip(f"{username}_version_function_") + f"--{r.scard(version)}个", "y": r.scard(version)})
        if data_list:
            data_list = sorted(data_list, key=lambda x: x["y"], reverse=True)
            data_list[0] = data_list[0] | {"sliced": False, "selected": True}
            all_version_bind_code = len(r.sunion(r.keys(f"{username}_version_function_*")))
            return render_template("shengsheng/chart/version_count_chart.html", data_list=data_list[:10],
                                   all_version_bind_code=all_version_bind_code)
        else:
            return render_template("shengsheng/chart/version_count_chart.html", data_list=[],
                                   all_version_bind_code=0)
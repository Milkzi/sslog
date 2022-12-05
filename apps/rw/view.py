import datetime

from flask import Blueprint, jsonify, render_template, redirect, url_for, request, flash, g, session, Response

from apps.rw.models import db, RWData

rw_app = Blueprint(name="rw_app", import_name=__name__,)


@rw_app.get("/read", endpoint="rw_read_index")
def rw_read_index():
    if request.method == "GET":
        rw_data = db.session.query(RWData.data).filter(RWData.id == 1).first()
        return render_template("rw/read_page.html", rw_data=rw_data[0])


@rw_app.route("/write", methods=["GET", "POST"], endpoint="rw_write_index")
def rw_write_index():
    if request.method == "GET":
        return render_template("rw/write_page.html")
    if request.method == "POST":
        try:
            data = request.form.get("write_data")
            first_data = db.session.query(RWData).filter(RWData.id == 1).first()
            if not first_data:
                db.session.add(RWData(data=data,create_time=datetime.datetime.now()))
            else:
                first_data.data = data
                first_data.create_time = datetime.datetime.now()
            db.session.commit()
            flash(message="写入成功！", category="warning")
            return render_template("rw/write_page.html")
        except Exception as e:
            print(e)
            return jsonify({"msg":"程序错误"})

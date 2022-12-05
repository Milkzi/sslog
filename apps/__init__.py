import time

from flask import Flask
from setting import SQLALCHEMY_DATABASE_URI
from apps.models import db

from datetime import timedelta

from .user.views import user_app
from .rw.view import rw_app
from .shengsheng.views import log_app







def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    # templates
    app.jinja_env.auto_reload = True

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    # redis
    app.config['SECRET_KEY'] = 'hu123456'
    # app.config['SESSION_TYPE'] = 'redis'
    # app.config['SESSION_PERMANENT'] = False
    # app.config['SESSION_USE_SIGNER'] = False
    # app.config['SESSION_KEY_PREFIX '] = 'ff_session:'
    # app.config['SESSION_REDIS'] = redis.Redis(host='192.168.5.1', port=6379)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)
    # mysql
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["SQLALCHEMY_POOL_SIZE"] = 50
    app.config["SQLALCHEMY_MAX_OVERFLOW"] = 30
    app.config["SQLALCHEMY_POOL_TIMEOUT"] = 10
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 120

    # Session(app)
    db.init_app(app)

    app.register_blueprint(user_app)
    app.register_blueprint(log_app)
    app.register_blueprint(rw_app)

    return app


# def start_runner():
#     def start_loop(t_db,t_db_session):
#         while True:
#             print("执行后台任务...")
#             share_order_share_add(db=t_db,db_session=t_db_session)
#             time.sleep(3)
#
#     thread = threading.Thread(target=start_loop,args=(db,db_session))
#     thread.start()



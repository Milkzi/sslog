import os

# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hu697693@192.168.5.1:3306/feng'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://hucheng:hu697693@106.14.26.159:3306/shengsheng'

# TODO docker部署时下面要改连接地址
# SQLALCHEMY_DATABASE_8C8G_URI = 'mysql+pymysql://root:hu697693@host.docker.internal:3306/feng'
# SQLALCHEMY_DATABASE_8C8G_URI = 'mysql+pymysql://root:hu697693@110.42.1.173:3306/feng'

# redis数据库地址
# REDIS_URI = 'fangfeng-redis'

REDIS_URI = '106.14.26.159'
# 便于调试
TEMPLATES_AUTO_RELOAD = True
SEND_FILE_MAX_AGE_DEFAULT = 0
SQLALCHEMY_TRACK_MODIFICATIONS = True
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

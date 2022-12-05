FROM python:3.9.2
MAINTAINER hucheng<12064936@qq.com>

ENV MYPATH /home/hucheng/sslog
WORKDIR $MYPATH 
COPY . .

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' > /etc/timezone

RUN  python -m pip install --upgrade pip -i http://pypi.douban.com/simple/
RUN	pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 9200

ENTRYPOINT  uwsgi --ini sslog.ini


FROM python:3.6.5

RUN mkdir /opt/KanelbulleWeb

ADD serve.py /opt/KanelbulleWeb
ADD requirements.txt /opt/KanelbulleWeb

WORKDIR /opt/KanelbulleWeb/
RUN pip install -r requirements.txt
CMD [ "python", "./main.py" ]

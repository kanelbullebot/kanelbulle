FROM python:3.6.5

ENV nohotreload true

RUN mkdir /opt/Kanelbulle

ADD main.py /opt/Kanelbulle
ADD requirements.txt /opt/Kanelbulle
ADD config.json /opt/Kanelbulle
ADD whitelist.json /opt/Kanelbulle
ADD /cogs/ /opt/Kanelbulle/cogs

RUN pip install -r requirements.txt
CMD [ "python", "./main.py" ]

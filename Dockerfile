FROM python:3.6.5

ADD main.py /
ADD requirements.txt /
ADD config.json /
ADD whitelist.json /
ADD /cogs/ /cogs/
ADD /.git/ /.git/

RUN pip install -r requirements.txt
CMD [ "python", "./main.py" ]

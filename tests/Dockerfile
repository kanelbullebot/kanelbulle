FROM python:3.6.5

ADD main.py /
ADD config.json /
ADD /cogs/ /cogs/
ADD /.git/ /.git/

RUN pip install asyncio requests wikipedia
RUN pip install -U git+https://github.com/Rapptz/discord.py@rewrite
CMD [ "python", "./importandrun.py" ]

FROM node:8

RUN mkdir /opt/KanelbulleFrontend

WORKDIR /opt/KanelbulleFrontend
COPY package*.json ./
RUN npm install

COPY . .

CMD [ "npm", "start" ]

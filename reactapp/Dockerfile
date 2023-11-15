FROM node:21-alpine3.17

WORKDIR /reactapp

RUN apk add python3

RUN apk add --no-cache libpng-dev cairo-dev pango-dev jpeg-dev giflib-dev

RUN apk add --no-cache make g++

COPY ./package.json .

RUN npm install

COPY . .

RUN npm i react-scripts@latest

EXPOSE 3005

CMD ["npm","start"]
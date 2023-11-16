FROM node:21-alpine3.17

WORKDIR /reactapp

RUN mkdir build

#RUN apk add python3

#RUN apk add --no-cache libpng-dev cairo-dev pango-dev jpeg-dev giflib-dev

#RUN apk add --no-cache make g++

#COPY ./package.json .

RUN npm install -g serve

COPY ./build ./build

EXPOSE 3005

CMD ["serve","-s","build","-l","3005"]
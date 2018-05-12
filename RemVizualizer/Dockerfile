FROM node:9.11.1

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install



# RUN yarn global add phantomjs-prebuilt

# ADD ./package.json $APPDIR/package.json
# ADD ./yarn.lock $APPDIR/yarn.lock
# RUN yarn install

# ADD . $APPDIR

# RUN yarn run build


EXPOSE 8080

CMD [ "npm", "start" ]
# CMD yarn start



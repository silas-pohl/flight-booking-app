FROM node:16.8.0-alpine

WORKDIR /code
#COPY rollup.config.js ./
#COPY package*.json ./
#RUN npm install

#COPY svelte.config.js ./
#COPY jest.config.js ./
#COPY tsconfig.json ./
#COPY .eslintrc.js ./
#COPY .eslintignore ./
#COPY ./src ./src
#COPY ./public ./public

#RUN npm run build
EXPOSE 5000
ENV HOST=0.0.0.0
#CMD npm run check && npm run lint && npm start
CMD npm run dev
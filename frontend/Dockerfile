FROM node:16.8.0-alpine

WORKDIR /code
COPY rollup.config.js ./
COPY package*.json ./
RUN npm install

COPY svelte.config.js ./
COPY prettier.config.js ./
COPY tsconfig.json ./
COPY .eslintrc.js ./
COPY ./src ./src
COPY ./public ./public

RUN npm run build
EXPOSE 5000
ENV HOST=0.0.0.0
CMD npm run lint && npm run check && npm start
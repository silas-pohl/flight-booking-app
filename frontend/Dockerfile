FROM node:16.8.0-alpine

WORKDIR /code
COPY rollup.config.js ./
COPY package*.json ./
RUN npm install

COPY ./src ./src
COPY ./public ./public
COPY svelte.config.js ./
COPY tsconfig.json ./
COPY .eslintrc.js ./
COPY .eslintignore ./

RUN npm run build
EXPOSE 5000
ENV HOST=0.0.0.0
CMD npm run check && npm run lint && npm test && npm start
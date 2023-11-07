FROM node:16.14.2-slim

EXPOSE 3000

WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN npm install
RUN npm install -g serve

COPY . .

RUN npm run build

CMD ["serve", "-s", "build"]
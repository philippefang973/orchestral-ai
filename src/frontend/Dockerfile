FROM node:latest as build

WORKDIR /app

COPY . .

# Install all the dependencies
RUN npm install -g @angular/cli
RUN npm install

CMD ["ng", "serve"]
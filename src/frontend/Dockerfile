FROM node:20-slim as build

WORKDIR /app

COPY package*.json /app/
# Install all the dependencies
RUN npm install 

COPY . /app/
RUN npm run build:ng

FROM nginx:alpine

# Copy the build output to replace the default nginx contents.
COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html
COPY ./custom-nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 4200

FROM node:20-slim as build

WORKDIR /app

COPY . .

# Install all the dependencies
RUN npm install 
RUN npm run build:ng

FROM nginx:alpine

# Copy the build output to replace the default nginx contents.
COPY --from=build /app/dist/frontend /usr/share/nginx/html

# Expose port 80
EXPOSE 4200
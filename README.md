#OrchestralAI Project
An audio converter application using neural network

This source code consists of :
- Backend in Flask divided in microservices (app, auth, converter)
- Frontend in Angular divided in components (homepage, dashboard, sigin, signup) 

## Installation
Python 3.10 and Node 20.9.0 versions are used.
For deployment, `docker`, `kubectl` and `minikube` are required.
Make sure to have 'ffmpeg', 'sox' and 'fluidsynth' installed in the system

The project needs to be launched from src/
Run `npm install`

## Local Run
Run `npm start`

## Deployment
Run `npm run deploy` to deploy both frontend/backend. A local Kubernetes cluster will be created.
Then `npm run push` to change the default cluster IP/PORT to localhost, the status of each pod will be displayed. This command is necessary to ensure the communication ports between backend and frontend.
If needed, use `npm run logs` to check the logs of every pods.
To stop the deployment, use `npm stop`.

The application is accessible from: http://localhost:4200/

# OrchestralAI Project
An audio converter application using neural network

This source code consists of :
- Backend in Flask divided in microservices (app, auth, converter)
- Frontend in Angular divided in components (homepage, dashboard, signin, signup) 

## Installation
Required : Python v3.10  Node v20.9.0, `ffmpeg`, `sox` and `fluidsynth` 

For deployment only : `docker`, `kubectl` and `minikube`

Using GPU (optional) : CUDA-Toolkit v11 and cuDNN v8

The project needs to be launched from src/

Run `npm install`

## Local Run
Run `npm start`

## Deployment
Run `npm run deploy` to deploy both frontend/backend. A local Kubernetes cluster will be created.

Then `npm run push` to change the default cluster IP/PORT to localhost, the status of each pod will be displayed. This command is necessary to ensure that the communication ports between backend and frontend works.

If needed, use `npm run logs` to check the logs of every pods.

To stop the deployment, use `npm stop`.

The application is accessible from: http://localhost:4200/

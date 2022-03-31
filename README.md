# GHost
Web interface to automatically deploy game servers to a Kubernetes cluster

## Setup
As it stands, this is very much a dev environment, and not ready for production. As such, all you should need to do is clone the repo, and run `flask run` in the project's root directory. This will start the web interface at `127.0.0.1:5000`

This project was written on the python Kubernetes client, which means you must have a valid kubeconfig saved to `~/.kube/config` in order for it to run. If this file exists, the program should configure itself to run on your instance

## Issues:
Currently, all persistent storage is local on nodes, which the Kubernetes API does not let you manage automatically. I am working on implementing Storage Classes, but for the time being, every persistent volume directory must be created manually on every node you would like to run this program on. This is kind of awful, but it's not a huge problem on a single node dev cluster, and I'm actively working on making this work better.

Obviously, the web UI is also very lackluster, however it currently only exists to test the backend. Once I have the backend in a good state, I'll start fleshing out the frontend.

## TODO:
  - [X] Translate YAML files to Kubernetes API calls
  - [ ] Add support for Storage Classes and dynamic storage allocation
  - [ ] Add support user accounts, resource limuts, etc.
  - [ ] Allow for management of files and pods after creation
  - [ ] Flesh out frontend, make it look nicer

# Demo Instagram object recognition service on DCOS/Marathon
Given an Instagram username, return the recognized objects from the user's latest image posts. 

<p align="center">
<img src="https://raw.githubusercontent.com/xiaoganghan/mesos-instagram-image-recognition/master/pictures/result.png" width="640">
</p>

* microservice architecture based on DCOS/Marathon
* TensorFlow + ImageNet model as deep learning backend

<p align="center">
<img src="https://raw.githubusercontent.com/xiaoganghan/mesos-instagram-image-recognition/master/pictures/logos.png" width="320">
</p>

## Architecture

<p align="center">
<img src="https://raw.githubusercontent.com/xiaoganghan/mesos-instagram-image-recognition/master/pictures/arch.png" width="480">
</p>

#### Front api service

* Provide Web UI to accept an Instagram username as input. It then send requests to the backend recognition service. 
* Routed with marathon-lb

#### Backend recognition service
* Uses TensorFlow to classify the input image with pre-trained ImageNet model.
* Routed using DCOS VIP

## Deployment

<p align="center">
<img src="https://raw.githubusercontent.com/xiaoganghan/mesos-instagram-image-recognition/master/pictures/dcos-running.png" width="640">
</p>

### setup

#### Clone the repo
```
git clone https://github.com/xiaoganghan/mesos-instagram-image-recognition.git
```

#### Install and boot dcos-vagrant

Follow the instructions [DC/OS-vagrant](https://dcos.io/docs/1.7/administration/installing/local/) to install DC/OS with Vagrant.

```
# suppose your DC/OS-vagrant directory is dcos-vagrant
cp mesos-instagram-image-recognition/ops/VagrantConfig.yaml dcos-vagrant/VagrantConfig.yaml
cd dcos-vagrant
vagrant up m1 a1 p1 boot 
```
#### Install DC/OS Command Line Interface (CLI)
Follow the instruction [DC/OS CLI](https://dcos.io/docs/1.7/usage/cli/install/) to install DC/OS CLI

#### Install marathon-lb

```
cd mesos-instagram-image-recognition/ops
dcos package install --options=marathon-lb.json marathon-lb --yes
```

### Deploy Backend recognition services (3 instances)

#### Install Docker
Install the Docker software by following the [Docker Installation](https://docs.docker.com/engine/installation/) 

#### Creat a Docker Hub account 

Create a [Docker Hub account](https://hub.docker.com/) to store the docker images created in the following step, 
assume your docker account name is 'DockerAccount'

#### build docker image, test locally, and push it to dockerhub
```
cd mesos-instagram-image-recognition/backend

# build a docker image called 'mesos-instagram-detect-backend'
# use sudo under ubuntu if 'Cannot connect to the Docker daemon. Is the docker daemon running on this host?' error shown
docker build -t mesos-instagram-detect-backend .   

# find out the id of image 'mesos-instagram-detect-backend'
docker images

#tag the image
docker tag [image_id] DockerAccount/mesos-instagram-detect-backend:latest

# run locally to test
docker run -it -p 5000:5000 --rm  DockerAccount/mesos-instagram-detect-backend

open the [url](http://localhost:5000/?image_url=https://igcdn-photos-b-a.akamaihd.net/hphotos-ak-xfa1/t51.2885-15/e35/1209679_1683062908612265_1359743351_n.jpg?ig_cache_key=MTIwODEwNzI1NDU2NjQzODE4NA%3D%3D.2) in browser to test

# If correct, the following results should be shown in the browser

{
objects: [
"stage (score = 0.02232)",
"wool, woolen, woollen (score = 0.01913)",
"mitten (score = 0.01680)",
"balloon (score = 0.01405)",
"cloak (score = 0.01377)"
]
}

# push to Docker Hub
docker push DockerAccount/mesos-instagram-detect-backend:latest
```

#### deploy backend to DCOS
```
cd mesos-instagram-image-recognition/ops
#Using [Web UI](http://m1.dcos): create application using ops/launch_backend.json
or,
#Using DC/OS CLI: 
dcos marathon app add launch_backend.json
```


### deploy front server (2 instances)

#### build docker image, test locally, and push it to dockerhub
```
cd mesos-instagram-image-recognition/front
docker build -t DockerAccount/mesos-instagram-detect-frontend:latest .

# run locally to test
docker run -it -p 5001:5001 --rm  DockerAccount/mesos-instagram-detect-frontend

# find out the id of image 'mesos-instagram-detect-backend'
docker images

# tag the image similar as the mesos-instagram-detect-backend
docker tag [image_id] DockerAccount/mesos-instagram-detect-frontend:latest

# push to Docker Hub
docker push DockerAccount/mesos-instagram-detect-frontend:latest
```

#### deploy frontend to DCOS

cd mesos-instagram-image-recognition/ops
Using [Web UI](http://m1.dcos): create application using ops/launch_front.json
or,
Using DC/OS CLI: 
dcos marathon app add launch_front.json

# verify it works
open http://instagramdemo.com in your browser

## references

* marathon-lb settings 
    * https://github.com/dcos/dcos-vagrant/blob/e9c0d6ade775debf0889b69b67f87cfdbf1aec9b/examples/oinker/README.md
* VIP settings
    * https://github.com/dcos/dcos-vagrant/tree/master/examples/minuteman
    * https://github.com/dcos/dcos-docs/pull/199/files

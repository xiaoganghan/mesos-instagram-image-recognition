# Demo Instagram object recognition service on DCOS/Marathon
Given an Instagram username, return the recognized objects from the user's latest image posts. 

![result])https://raw.githubusercontent.com/xiaoganghan/mesos-instagram-image-recognition/master/pictures/result.png]

* microservice architecture based on DCOS/Marathon
* TensorFlow + ImageNet model as deep learning backend

![logos])https://raw.githubusercontent.com/xiaoganghan/mesos-instagram-image-recognition/master/pictures/logos.png]


## Architecture

![arch])https://raw.githubusercontent.com/xiaoganghan/mesos-instagram-image-recognition/master/pictures/arch.png]

#### Front api service

* Provide Web UI to accept an Instagram username as input. It then send requests to the backend recognition service. 
* Routed with marathon-lb

#### Backend recognition service
* Uses TensorFlow to classify the input image with pre-trained ImageNet model.
* Routed using DCOS VIP

## Deployment

![dcos])https://raw.githubusercontent.com/xiaoganghan/mesos-instagram-image-recognition/master/pictures/dcos-running.png]

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

#### Install marathon-lb

```
cd mesos-instagram-image-recognition/ops
dcos package install --options=marathon-lb.json marathon-lb --yes
```

### Deploy Backend recognition services (3 instances)

#### build docker image, test locally, and push it to dockerhub
```
cd mesos-instagram-image-recognition/backend
docker build --pull -t hanxiaogang/mesos-instagram-detect-backend:latest .

# run locally to test
docker run -it -p 5000:5000 --rm  hanxiaogang/mesos-instagram-detect-backend
http://192.168.99.100:5000/?image_url=https://igcdn-photos-b-a.akamaihd.net/hphotos-ak-xfa1/t51.2885-15/e35/1209679_1683062908612265_1359743351_n.jpg?ig_cache_key=MTIwODEwNzI1NDU2NjQzODE4NA%3D%3D.2

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
docker push hanxiaogang/mesos-instagram-detect-backend:latest
```

#### deploy backend to DCOS
```
cd mesos-instagram-image-recognition/ops
Using Web UI: create application using ops/launch_backend.json
or,
Using dcos-cli: dcos marathon app add launch_backend.json
```


### deploy front server (2 instances)

#### build docker image, test locally, and push it to dockerhub
```
cd mesos-instagram-image-recognition/front
docker build -t hanxiaogang/mesos-instagram-detect-frontend:latest .

# run locally to test
docker run -it -p 5001:5001 --rm  hanxiaogang/mesos-instagram-detect-frontend

# push to Docker Hub
docker push hanxiaogang/mesos-instagram-detect-frontend:latest
```

#### deploy frontend to DCOS

```
cd mesos-instagram-image-recognition/ops
Using Web UI: create application using ops/launch_front.json
or,
Using dcos-cli: dcos marathon app add launch_front.json

# verify it works
open http://instagramdemo.com in your browser
```

## references

* marathon-lb settings 
    * https://github.com/dcos/dcos-vagrant/blob/e9c0d6ade775debf0889b69b67f87cfdbf1aec9b/examples/oinker/README.md
* VIP settings
    * https://github.com/dcos/dcos-vagrant/tree/master/examples/minuteman
    * https://github.com/dcos/dcos-docs/pull/199/files

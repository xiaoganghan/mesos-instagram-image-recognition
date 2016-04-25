# Demo Instagram object recognition service on DCOS/Marathon
Given an Instagram username, return the recognized objects from the user's latest image posts. 

* microservice architecture based on DCOS/Marathon
* TensorFlow + ImageNet model as deep learning backend

## Architecture

#### Front api service

* The front API service provide Web UI to accept an Instagram username as input. It then send requests to the backend recognition service. 
* The front services are routed with marathon-lb

#### Backend recognition service
* The backend recognition service uses TensorFlow to classify the input image with pre-trained ImageNet model.
* The recognition services are routed using DCOS VIP

## Development

#### Front service

To be added

#### Backend service

To be added

## Deployment

### setup [DCOS-vagrant](https://dcos.io/docs/1.7/administration/installing/local/)

#### Install and boot dcos-vagrant
```
download and install dcos-vagrant and dcos-cli
cp ops/VagrantConfig.yaml dcos-vagrant/VagrantConfig.yaml
cd dcos-vagrant
vagrant up m1 a1 p1 boot 
```

#### Install marathon-lb

```
cd ops
dcos package install --options=marathon-lb.json marathon-lb --yes
```

### Deploy Backend recognition services (1 vs. 3 instances)

#### build docker image, test locally, and push it to dockerhub
```
cd backend
docker build --pull -t hanxiaogang/mesos-instagram-detect-backend:latest .

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

docker push hanxiaogang/mesos-instagram-detect-backend:latest
```

#### deploy backend to DCOS
```
cd ops
Using Web UI: create application using ops/launch_backend.json
or,
Using dcos-cli: dcos marathon app add launch_backend.json
```

* references 
    * https://github.com/dcos/dcos-vagrant/tree/master/examples/minuteman
    * https://github.com/dcos/dcos-docs/pull/199/files

### deploy front server (one instance)

#### build docker image, test locally, and push it to dockerhub
```
cd front
docker build -t hanxiaogang/mesos-instagram-detect-frontend:latest .
docker run -it -p 5001:5001 --rm  hanxiaogang/mesos-instagram-detect-frontend
docker push hanxiaogang/mesos-instagram-detect-frontend:latest
```

#### deploy frontend to DCOS

```
cd ops
Using Web UI: create application using ops/launch_front.json
or,
Using dcos-cli: dcos marathon app add launch_front.json

# verify it works
open http://instagramdemo.com in browser
```

* reference settings for marathon-lb https://github.com/dcos/dcos-vagrant/blob/e9c0d6ade775debf0889b69b67f87cfdbf1aec9b/examples/oinker/README.md

## Introduction
#### I made this project to practice my docker-compose knowledge. It should not be used for interview purpose.

## Scenario 
#### Assume we have N virtual cameras, each records a event to redis every 10 seconds. Each camera has a long-polling with the API server. Once a user request for camera log from web page, the server let that camera know (I used Pushpin, so it is pub-sub), then that camera instantly start a new HTTP request to send log to the API server, at that time that log should also be stored to disk DB. The long-polling should refresh every 1 min.  
![Image of Architecture](https://github.com/ZiyeHan/DockerComposeProject/blob/master/architecture.png)

## How to run
#### step1: download or git clone this project 
#### step2: make sure you have the docker engine installed already
#### step3: go inside the folder, run "docker-compose up" in the terminal
#### step4: wait until no more promoted logs, then open another new terminal, run "open -a Google\ Chrome --args --disable-web-security --user-data-dir="  (because Chrome has some cross-domain restrictions)
#### step5: in the opened browser, open "localhost:8000/admin.html", enjoy



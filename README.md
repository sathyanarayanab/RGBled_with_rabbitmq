# RGBled_with_rabbitmq
Control RBG LED via webserver that can sync across many devices through rabbitmq

## Setup

### On PI

```
pip install -r requirements.txt
export FLASK_ENV=app.py
```

### Any device that can serve Rabbitmq

```
sudo docker run -it --rm --name rabbitmq --network host rabbitmq:3.10-management
sudo docker exec rabbitmq rabbitmq-plugins enable rabbitmq_web_stomp
sudo docker exec rabbitmq rabbitmqadmin declare exchange name=logs type=fanout durable=false
```

### On sourcecode

1. Change the WS endpoint in main.js (Line 2)
2. Change the user credentials as per your configurations in main.js (Line 4)
3. Change the IP of PI in main.js (Line 27 and 54)


https://user-images.githubusercontent.com/83451857/182020507-525f85e8-e6a3-489f-90d0-985db866bb1f.mp4


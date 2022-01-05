docker build -t yolov5-flask-kunshujo .

docker run -d -p 5003:5000 yolov5-flask-kunshujo:latest

docker run -p 5002:5000 yolov5-flask-kunshujo:latest

docker stop 255fee9edb19

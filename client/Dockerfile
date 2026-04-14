FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3
COPY iot_sensor.py /iot_sensor.py
CMD ["python3", "/iot_sensor.py"]

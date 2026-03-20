FROM  python:3.11

WORKDIR /app

COPY multicast_receiver.py .
COPY multicast_sender.py .

RUN apt-get update && apt-get install -y tcpdump

CMD ["python", "-u", "multicast_sender.py"]
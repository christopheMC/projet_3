FROM debian:latest

ADD api_projet_3.py requirements.txt /my_server/

WORKDIR /my_server/

RUN apt update && apt install python3-pip -y && pip3 install -r requirements.txt

EXPOSE 5000

CMD python3 api_projet_3.py

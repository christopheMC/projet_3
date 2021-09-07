FROM debian:latest

ADD fill_docker.py requirements.txt insert.sh  projet_3_analyzer.json  top250-00-19.csv /fill/

WORKDIR /fill/

RUN apt-get update && apt-get install python3-pip -y && pip3 install -r requirements.txt

EXPOSE 9200

CMD python3 fill_docker.py

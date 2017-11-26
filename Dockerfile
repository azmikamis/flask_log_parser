From ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential unzip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN unzip CTF1.zip
ENTRYPOINT ["python"]
CMD ["run.py"]

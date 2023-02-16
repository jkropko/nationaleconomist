# syntax=docker/dockerfile:1

FROM python:3.11-bullseye

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN apt-get update -y
RUN curl -fsSL https://deb.nodesource.com/setup_19.x | bash - &&\
apt-get install -y nodejs
RUN apt-get install tesseract-ocr -y
RUN apt-get install libtesseract-dev -y
RUN apt-get install libgl1 -y
RUN apt install sudo
RUN sudo apt install nano

WORKDIR /nationaleconomist

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root"]


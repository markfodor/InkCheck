FROM python:latest

RUN apt-get update \
    && apt-get -y install chromium-driver

WORKDIR /inkcheck 
COPY ./requirements.txt /inkcheck

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt 

COPY . /inkcheck

EXPOSE 8080
ENTRYPOINT ["python3", "main.py"]
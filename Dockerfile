FROM python:3.10.1-alpine

WORKDIR /opt
COPY . /opt/

RUN pip install -r requirements.txt

CMD [ "python3", "/opt/app.py"]
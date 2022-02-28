FROM python:3.10.1-alpine

WORKDIR /opt
COPY . /opt/

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:fast_api", "--host", "0.0.0.0", "--port", "5000"]
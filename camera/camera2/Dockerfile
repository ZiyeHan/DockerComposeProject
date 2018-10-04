FROM python:3.4-alpine

RUN mkdir code

ADD . /code

WORKDIR /code

RUN pip install -U pip 
RUN pip install -r requirements-camera.txt

CMD ["python", "camera2.py"] 

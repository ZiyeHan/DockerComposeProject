FROM python:2.7.9

RUN mkdir code

ADD . /code

WORKDIR /code

RUN pip install -U pip
RUN pip uninstall -y setuptools
RUN pip install 'setuptools<20.2' 
RUN pip install -r requirements-server.txt

CMD ["python", "app.py"]  
 
EXPOSE 5000
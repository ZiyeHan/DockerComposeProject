FROM python:3.4-alpine

RUN mkdir web

ADD . /web

WORKDIR /web

CMD ["python", "-m", "http.server", "8000"]   

EXPOSE 8000
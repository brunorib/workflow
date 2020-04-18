FROM python:3

WORKDIR /app

COPY . /app

RUN python setup.py install

EXPOSE 5000

CMD [ "./docker_entrypoint.sh" ]
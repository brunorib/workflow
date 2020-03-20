FROM python:3

WORKDIR /app

COPY . /app

RUN python setup.py install

RUN . ./.env

ENTRYPOINT [ "python" ]

EXPOSE 5000

CMD [ "manage.py", "run" ]
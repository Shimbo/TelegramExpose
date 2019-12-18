FROM python:3

WORKDIR /usr/src/app

RUN pip install flask
RUN pip install telethon

COPY . .

EXPOSE 5432
CMD [ "python", "./service.py" ]
FROM python:3.8-slim-buster

WORKDIR /chat_app_versie_zonder_login_styeem

LABEL Author="Rafaelorr"

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "app.py"]
# initialize image
FROM python:3.8.2

WORKDIR /flask-store-app

ADD . /flask-store-app

RUN pip install -r requirements.txt

RUN export FLASK_APP=app.py

RUN export FLASK_ENV=development

CMD [ "flask", "run", "--host=0.0.0.0" ]
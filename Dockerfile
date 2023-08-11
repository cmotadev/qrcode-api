FROM python:3.10-alpine

ARG SERVER_PORT=8080

WORKDIR /usr/src/app

COPY . .

RUN python -m pip install -r requirements.txt

EXPOSE ${SERVER_PORT}

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080" ]

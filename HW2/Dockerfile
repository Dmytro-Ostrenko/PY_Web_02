FROM python:3.11


WORKDIR /app

COPY . /app

RUN python -m venv /venv

RUN pip install --upgrade pip


EXPOSE 5000

ENV NAME Bot

ENTRYPOINT ["python", "main.py"]
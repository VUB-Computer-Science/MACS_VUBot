FROM python:3.9-slim-buster

RUN pip install poetry

COPY . .
RUN poetry install

CMD ["poetry", "run", "python3", "main.py"]

FROM python:3.12-slim

WORKDIR /code

COPY ./requirements.txt ./
RUN pip install --no-cache-dir --timeout=1000 --verbose -r requirements.txt

COPY ./src ./src

ENV PYTHONPATH=/code/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
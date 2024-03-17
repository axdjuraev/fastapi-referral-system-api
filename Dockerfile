FROM python:3.10.6-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt
RUN python3 -m alembic upgrade head

EXPOSE 8080

ENTRYPOINT ["sh", "-c"]
CMD ["python3 -m uvicorn --factory src.main:create_app --host='0.0.0.0' --port=8080"]

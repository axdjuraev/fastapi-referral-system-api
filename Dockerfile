FROM python:3.10.6-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN python3 -m alebmic upgrade head

EXPOSE 8080

ENTRYPOINT ["sh", "-c"]
CMD ["python3 src/main/web.py"]
